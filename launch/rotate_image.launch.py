import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    image_rotate_yaml = os.path.join(
        get_package_share_directory("stretch_seeing_eye_ros2"),
        "config", "rotate_image.yaml"
    )
    return LaunchDescription([
        Node(
            package="image_rotate",
            executable="image_rotate",
            output="screen",
            parameters=[image_rotate_yaml],
            remappings=[
                ("image", "/camera/color/image_raw"),
                ("camera_info", "/camera/color/camera_info")
            ]
        ),
        Node(
            package="image_rotate",
            executable="image_rotate",
            output="screen",
            parameters=[image_rotate_yaml],
            remappings=[
                ("image", "/camera/depth/image_rect_raw"),
                ("camera_info", "/camera/color/camera_info"),
                ("rotated/image", "/rotated/depth")
            ]
        ),
    ])
