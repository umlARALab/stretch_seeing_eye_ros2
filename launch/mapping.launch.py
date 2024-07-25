import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    mapping_params = os.path.join(
        get_package_share_directory("stretch_seeing_eye_ros2"),
        "config/mapping.yaml"
    )
    # NOTE: This is not going to work. The stretch_navigation pkg assumes that Rviz1 is being
    #       used, not Rviz2.
    # rviz_config_file = os.path.join(
    #     get_package_share_directory("stretch_navigation"),
    #     "rviz/mapping.rviz"
    # )
    return LaunchDescription([
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
            # arguments=["-d", rviz_config_file], | TODO: Create new rviz2 config file
            condition=IfCondition(LaunchConfiguration("rviz"))
        )
    ])
