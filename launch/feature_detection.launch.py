from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import FindPackagePath, LaunchConfiguration
from launch_ros.actions import Node
from os.path import join

def generate_launch_description():
    # Define launch arguments
    location_arg = DeclareLaunchArgument(
        'location',
        default_value='default_location',
        description='Location argument for description file'
    )

    # Define parameter for description file
    description_param = DeclareLaunchArgument(
        'description_file',
        default_value=LaunchConfiguration('location'),
        description='Parameter for description file path'
    )

    # Define publish_plane_node
    publish_plane_node = Node(
        package='stretch_seeing_eye',
        executable='publish_plane_node',
        name='publish_plane_node',
        output='screen'
    )

    # Define detect_feature node
    detect_feature_node = Node(
        package='stretch_seeing_eye',
        executable='detect_feature.py',
        name='detect_feature',
        output='screen',
        parameters=[join(FindPackagePath('stretch_seeing_eye_ros2'), 'config', LaunchConfiguration('location'), 'feature_detection.yaml')]
    )

    return LaunchDescription([
        location_arg,
        description_param,
        publish_plane_node,
        detect_feature_node,
        LogInfo(msg=["Launch file loaded successfully!"])
    ])
