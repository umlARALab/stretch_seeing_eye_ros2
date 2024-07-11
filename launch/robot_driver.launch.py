import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    ros_gz_sim = os.path.join(
        get_package_share_directory("ros_gz_sim"),
        "launch", "gz_sim.launch.py"
    )
    stretch_driver_remapped = os.path.join(
        get_package_share_directory("stretch_seeing_eye_ros2"),
        "launch", "stretch_driver_remapped.launch.py"
    )
    simulation_world_set = PythonExpression(
        ["'", LaunchConfiguration("simulation_world"), "' != ''"]
    )
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
            condition=IfCondition(simulation_world_set),
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(ros_gz_sim),
                    launch_arguments={
                        "gz_args": ["-r -s -v3 ", LaunchConfiguration("simulation_world")],
                        "on_exit_shutdown": "true",
                        "use_sim_time": "true"
                    }.items()
                ),
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(ros_gz_sim),
                    launch_arguments={
                        "gz_args": "-g -v3 ",
                        "use_sim_time": "true"
                    }.items()
                )
            ]
        ),
        GroupAction(
            condition=UnlessCondition(simulation_world_set),
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(stretch_driver_remapped),
                ),
            ]
        )
        # Node(
        #     package="stretch_seeing_eye_ros2",
        #     executable="robot_driver",
        #     name="robot_driver",
        #     output="screen",
        #     parameters=[{"use_simulation": IfCondition(simulation_world_set)}]
        # )
    ])
