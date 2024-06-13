import rclpy
from rclpy.node import Node
import tf2_ros
import tf2_geometry_msgs
import math as Math

from enum import Enum
from std_msgs.msg import String
from geometry_msgs.msg import Point32, Point, PointStamped
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry.polygon import Polygon as ShapelyPolygon
from nav_msgs.srv import GetPlan, GetPlan_Request, GetPlan_Response

from stretch_seeing_eye.feature import Feature
from stretch_seeing_eye.srv import Feature as FeatureService, Feature_Request
from stretch_seeing_eye.msg import Door

MARKER_TOPIC = '/stretch_seeing_eye/create_marker'

class DetailLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class DetectFeature(Node):
    def __init__(self):
        super().__init__('detect_feature')
        
        self.declare_parameters(
            namespace='',
            parameters=[
                ('detect_feature/Feature_Detection/door_distance', None),
                ('detect_feature/Feature_Detection/door_detection_cone', None),
                ('detect_feature/Feature_Detection/feature_distance', None),
                ('detect_feature/Feature_Detection/detail_level', None),
                ('/description_file', None)
            ]
        )
        
        self.set_detail_level_sub = self.create_subscription(String, '/stretch_seeing_eye/set_detail_level', self.set_detail_level_callback, 1)
        self.publish_feature = self.create_publisher(Door, '/stretch_seeing_eye/feature', 1)

        self.create_feature_marker = self.create_client(FeatureService, MARKER_TOPIC)
        while not self.create_feature_marker.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

        self.make_plan_service = self.create_client(GetPlan, '/move_base/NavfnROS/make_plan')
        while not self.make_plan_service.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Make plan service not available, waiting again...')

        self.tf_buffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.parameters = {
            'door_distance': self.get_parameter('detect_feature/Feature_Detection/door_distance').get_parameter_value().double_value,
            'door_detection_cone': self.get_parameter('detect_feature/Feature_Detection/door_detection_cone').get_parameter_value().double_value,
            'feature_distance': self.get_parameter('detect_feature/Feature_Detection/feature_distance').get_parameter_value().double_value,
        }

        self.features = {}
        self.previous_feature = None
        self.detail_level: DetailLevel = getattr(DetailLevel, self.get_parameter('detect_feature/Feature_Detection/detail_level').get_parameter_value().string_value)
        
        self.import_features(self.get_parameter('/description_file').get_parameter_value().string_value)

    def import_features(self, file: str):
        self.features = {}
        for key in DetailLevel:
            self.features[key.value] = {}

        with open(file, 'r') as f:
            data = f.read().split('---\n')[1].split('\n')
            for line in data:
                if line == "":
                    continue
                f = Feature(line.strip())
                self.features[f.detail_level][f.name] = f
                req = Feature_Request(points=f.points, detail_level=f.detail_level - 1)
                self.create_feature_marker.call_async(req)

    def set_detail_level_callback(self, msg: String):
        self.detail_level = getattr(DetailLevel, msg.data)
        self.get_logger().debug(f'Set detail level to {self.detail_level}')

    def check_feature_point(self, key: str, feature: Feature):
        try:
            point = PointStamped(point=Point(x=feature.points[0].x, y=feature.points[0].y, z=feature.points[0].z))
            point.header.frame_id = 'map'
            point = self.tf_buffer.transform(point, 'base_link')
            transform = self.tf_buffer.lookup_transform('map', 'base_link', rclpy.time.Time())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            return
        request = GetPlan_Request()
        request.start.header.frame_id = 'map'
        request.start.pose.position.x = transform.transform.translation.x
        request.start.pose.position.y = transform.transform.translation.y
        request.start.pose.orientation.w = 1.0
        request.goal = feature.getPoseStamped()

        future = self.make_plan_service.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            plan = future.result()
        else:
            return

        length = 0
        for i, el in enumerate(plan.plan.poses):
            if i == 0:
                continue
            length += Math.sqrt((el.pose.position.x - plan.plan.poses[i-1].pose.position.x)**2 + (el.pose.position.y - plan.plan.poses[i-1].pose.position.y)**2)

        if point.point.x > 0 and length < 5:
            self.get_logger().debug(f'Found feature: {key}')
            self.get_logger().debug(f'\t Angle: {Math.degrees(Math.atan2(point.point.y, point.point.x))}')
            self.publish_feature.publish(Door(description=feature.description, degree=int(Math.degrees(Math.atan2(point.point.y, point.point.x)))))
            self.previous_feature = key
    
    def check_feature_polygon(self, key: str, feature: Feature):
        try:
            transform = self.tf_buffer.lookup_transform('map', 'base_link', rclpy.time.Time())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            self.get_logger().debug('No transform found')
            return
        points = [ShapelyPoint(point.x, point.y) for point in feature.points]
        polygon = ShapelyPolygon(points)
        if polygon.distance(ShapelyPoint(transform.transform.translation.x, transform.transform.translation.y)) <= self.parameters['feature_distance']:
            self.get_logger().debug(f'Found feature: {feature.name}')
            self.publish_feature.publish(feature.description)
            self.previous_feature = key

    def check_range(self):
        for detail_level in DetailLevel:
            if detail_level.value > self.detail_level.value:
                break
            for key, value in self.features[detail_level.value].items():
                assert isinstance(value, Feature)
                if len(value.points) == 1 and self.previous_feature != key:
                    self.check_feature_point(key, value)
                elif len(value.points) == 4 and self.previous_feature != key:
                    self.check_feature_polygon(key, value)

    
    def start(self):
        rate = self.create_rate(10)
        self.previous_feature = None
        while rclpy.ok():
            self.check_range()
            rate.sleep()


def main(args=None):
    rclpy.init(args=args)
    detect_feature = DetectFeature()
    detect_feature.start()
    detect_feature.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
