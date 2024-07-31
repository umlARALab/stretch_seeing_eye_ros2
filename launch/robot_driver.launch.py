import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression


def generate_launch_description():
    ros_gz_sim = os.path.join(
        get_package_share_directory("ros_gz_sim"),
        "launch", "gz_sim.launch.py"
    )
    stretch_driver = os.path.join(
        get_package_share_directory("stretch_core"),
        "launch", "stretch_driver.launch.py"
    )
    rplidar = os.path.join(
        get_package_share_directory("stretch_seeing_eye_ros2"),
        "launch", "rplidar_mod.launch.py"
    )
    navigation = os.path.join(
        get_package_share_directory("stretch_seeing_eye_ros2"),
        "launch", "navigation.launch.py"
    )
    mapping = os.path.join(
        get_package_share_directory("stretch_seeing_eye_ros2"),
        "launch", "mapping.launch.py"
    )
    teleop_twist_include = os.path.join(
        get_package_share_directory("stretch_seeing_eye_ros2"),
        "launch/teleop_twist.launch.py"
    )
    simulation_world_set = PythonExpression(
        ["'", LaunchConfiguration("simulation_world"), "' != ''"]
    )
    location_set = PythonExpression(
        ["'", LaunchConfiguration("location"), "' != ''"]
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
        DeclareLaunchArgument(
            "rviz",
            default_value="true",
            description="Whether to show rviz"
        ),
        DeclareLaunchArgument(
            "teleop_type",
            default_value="keyboard",
            description="Set teleop controller ('keyboard', 'joystick', or 'none')"
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
                    PythonLaunchDescriptionSource(stretch_driver),
                    launch_arguments={
                        "mode": "navigation",
                        "broadcast_odom_tf": "True"
                    }.items()
                ),
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(rplidar)
                )
            ]
        ),
        GroupAction(
            condition=IfCondition(location_set),
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(navigation),
                    launch_arguments={
                        "rviz": LaunchConfiguration("rviz"),
                        "location": LaunchConfiguration("location"),
                        "use_sim_time": simulation_world_set
                    }.items()
                ),
            ]
        ),
        GroupAction(
            condition=UnlessCondition(location_set),
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(mapping),
                    launch_arguments={
                        "rviz": LaunchConfiguration("rviz")
                    }.items()
                ),
            ]
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([teleop_twist_include]),
            launch_arguments={
                "teleop_type": LaunchConfiguration("teleop_type"),
                "linear": "0.04",
                "angular": "1.0",
                "twist_topic": "cmd_vel"
            }.items()
        )
    ])
