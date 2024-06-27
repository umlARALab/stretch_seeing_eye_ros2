import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """Launch the physical stretch2 robot, a simulaton of the stretch2,
       or a simulation of another robot remapped to stretch2 for navigation."""
    nav_driver_params = os.path.join(
        get_package_share_directory("stretch_seeing_eye_ros2"),
        "config/nav_driver_params.yaml"
    )
    return LaunchDescription([
        Node(
            package="stretch_seeing_eye_ros2",
            executable="nav_driver",
            name="nav_driver",
            output="screen",
            parameters=[nav_driver_params]
        )
    ])
