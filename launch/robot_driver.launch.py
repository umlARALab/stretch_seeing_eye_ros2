from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, GroupAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
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
                ExecuteProcess(
                    cmd=["ign", "gazebo", LaunchConfiguration("simulation_world")],
                    output="screen"
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
