from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from os.path import join

def generate_launch_description():
    # Define launch arguments
    location_arg = DeclareLaunchArgument(
        'location',
        default_value='default_location',
        description='Location argument for description file'
    )

    # Define parameter for description file
    description_param = DeclareLaunchArgument(
        'description_file',
        default_value=LaunchConfiguration('location'),
        description='Parameter for description file path'
    )

    # Define publish_plane_node
    publish_plane_node = Node(
        package='stretch_seeing_eye_ros2',
        executable='publish_plane',
        name='publish_plane',
        output='screen'
    )

    # Define detect_feature node
    detect_feature_node = Node(
        package='stretch_seeing_eye_ros2',
        executable='detect_feature.py',
        name='detect_feature',
        output='screen',
        parameters=['/home/hello-robot/ament_ws/src/stretch_seeing_eye_ros2/config/feature_detection.yaml']
        # parameters=[join(FindPackageShare('stretch_seeing_eye_ros2').find('stretch_seeing_eye_ros2'), 'config', LaunchConfiguration('location'), 'feature_detection.yaml')]
    )

    return LaunchDescription([
        location_arg,
        description_param,
        publish_plane_node,
        detect_feature_node,
        LogInfo(msg=["Launch file loaded successfully!"])
    ])
