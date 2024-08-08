import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription, LaunchContext
from launch.actions import IncludeLaunchDescription, OpaqueFunction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    nav2_bringup = os.path.join(
        get_package_share_directory("nav2_bringup"),
        "launch/bringup_launch.py"
    )
    nav2_params = os.path.join(
        get_package_share_directory("stretch_seeing_eye_ros2"),
        "config/nav2_params.yaml"
    )
    rviz_config_file = os.path.join(
        get_package_share_directory("stretch_seeing_eye_ros2"),
        "rviz/navigation_config.rviz"
    )

    # TODO: This is convoluted, but I cannot find a better way to convert
    #       a `LaunchConfiguration` to a `str` directly.
    #       If you find a better solution, please implement it.
    def format_map_yaml_path(context: LaunchContext, location):
        location_str = context.perform_substitution(location)
        map_yaml = os.path.join(
            get_package_share_directory("stretch_seeing_eye_ros2"),
            "map/%s/%s.yaml" % (location_str, location_str)
        )
        nav2_bringup_description = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(nav2_bringup),
            launch_arguments={
                "use_sim_time": LaunchConfiguration("use_sim_time"),
                "autostart": "true",
                "map": map_yaml,
                "params_file": nav2_params,
                "use_rviz": LaunchConfiguration("rviz")
            }.items()
        )
        return [nav2_bringup_description]

    return LaunchDescription([
        OpaqueFunction(function=format_map_yaml_path, args=[LaunchConfiguration("location")]),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="log",
            arguments=["-d", rviz_config_file],
            condition=IfCondition(LaunchConfiguration("rviz"))
        )
    ])
