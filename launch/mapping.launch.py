import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    rviz_argument = "true"
    teleop_type_argument = "keyboard"
    teleop_twist_include = os.path.join(
        get_package_share_directory("stretch_core"),
        "launch/teleop_twist.launch"
    )
    mapping_params = os.path.join(
        get_package_share_directory("stretch_seeing_eye_ros2"),
        "config/move_base/mapping.yaml"
    )
    rviz_config_file = os.path.join(
        get_package_share_directory("stretch_navigation"),
        "rviz/mapping.rviz"
    )
    return LaunchDescription([
        DeclareLaunchArgument(
            "rviz",
            default_value=rviz_argument,
            description="Whether to show rviz"
        ),
        DeclareLaunchArgument(
            "teleop_type",
            default_value=teleop_type_argument,
            description="Set teleop controller ('keyboard', 'joystick', or 'none')"
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([teleop_twist_include]),
            launch_arguments={
                "teleop_type": LaunchConfiguration("teleop_type"),
                "linear": "0.04",
                "angular": "1.0",
                "twist_topic": "/stretch/cmd_vel"
            }.items()
        ),
        Node(
            package="slam_toolbox",
            executable="sync_slam_toolbox_node",
            name="slam_toolbox",
            output="screen",
            parameters=[mapping_params]
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="log",
            arguments=["-d", rviz_config_file],
            condition=IfCondition(LaunchConfiguration("rviz"))
        )
    ])
