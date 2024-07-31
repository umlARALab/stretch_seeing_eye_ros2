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

    # TODO: This is convoluted as hell, but I cannot find a better way to convert
    #       a `LaunchConfiguration` to a `str` directly.
    #       If you find a better solution, please implement it.
    map_yaml = ""
    def format_map_yaml_path(context: LaunchContext, location):
        location_str = context.perform_substitution(location)
        nonlocal map_yaml
        map_yaml = os.path.join(
            get_package_share_directory("stretch_seeing_eye_ros2"),
            "map/%s/%s.yaml" % (location_str, location_str)
        )

    # TODO
    # rviz_config_file = os.path.join(
    #     get_package_share_directory("stretch_seeing_eye_ros2"),
    #     "rviz/navigation_config.rviz"
    # )
    return LaunchDescription([
        # See first TODO
        OpaqueFunction(function=format_map_yaml_path, args=[LaunchConfiguration("location")]),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(nav2_bringup),
            launch_arguments={
                "use_sim_time": LaunchConfiguration("use_sim_time"),
                "autostart": "true",
                "map": map_yaml,
                "params_file": nav2_params,
                "use_rviz": LaunchConfiguration("rviz")
            }.items()
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="log",
            # arguments=["-d", rviz_config_file],
            condition=IfCondition(LaunchConfiguration("rviz"))
        )
    ])
