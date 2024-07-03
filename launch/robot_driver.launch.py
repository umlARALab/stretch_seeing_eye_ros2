from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package="stretch_seeing_eye_ros2",
            executable="nav_driver",
            name="nav_driver",
            output="screen"
        )
    ])
