import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, \
    GroupAction, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    ros_gz_sim = get_package_share_directory("ros_gz_sim")
    return LaunchDescription([
        DeclareLaunchArgument(
            "location",
            default_value="",
            description="The directory name containing a map file \
                (leave blank to create a new one)"
        ),
        DeclareLaunchArgument(
            "simulation_world",
            default_value="",
            description="Set the Gazebo .world file to be launched (if using a simulation)"
        ),
        GroupAction(
            condition=IfCondition(
                PythonExpression(["'", LaunchConfiguration("simulation_world"), "' != ''"])
            ),
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        os.path.join(ros_gz_sim, "launch", "gz_sim.launch.py")
                    ),
                    launch_arguments={
                        "gz_args": ["-r -s -v4 ", LaunchConfiguration("simulation_world")],
                        "on_exit_shutdown": "true"
                    }.items()
                ),
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        os.path.join(ros_gz_sim, "launch", "gz_sim.launch.py")
                    ),
                    launch_arguments={"gz_args": "-g -v4 "}.items()
                )
            ]
        ),
        Node(
            package="stretch_seeing_eye_ros2",
            executable="robot_driver",
            name="robot_driver",
            output="screen"
        )
    ])
