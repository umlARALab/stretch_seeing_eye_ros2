import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    scan_filter_params = os.path.join(
        get_package_share_directory("stretch_seeing_eye_ros2"),
        "config", "rplidar_mod.yaml"
    )
    return LaunchDescription([
        Node(
            package="sllidar_ros2",
            executable="sllidar_node",
            name="lidar_node",
            output="screen",
            parameters=[
                {"serial_port": "/dev/hello-lrf"},
                {"serial_baudrate": 115200},
                {"frame_id": "laser"},
                {"inverted": False},
                {"angle_compensate": True},
                {"scan_mode": "Boost"}
            ]
        ),
        Node(
            package="laser_filters",
            executable="scan_to_scan_filter_chain",
            name="laser_filter",
            namespace="scan_filter_chain",
            parameters=[scan_filter_params]
        )
    ])
