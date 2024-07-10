import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    # laser_filters_pkg = FindPackageShare(package='laser_filters').find('laser_filters')

    # params_file = LaunchConfiguration('params_file', default=os.path.join(laser_filters_pkg, 'laser_filter_params.yaml'))

    return LaunchDescription([
        # DeclareLaunchArgument('params_file', default_value=params_file, description='Path to parameter file'),

        Node(
            package='laser_filters',
            executable='scan_to_scan_filter_chain',
            name='laser_filter',
            namespace='scan_filter_chain',
            output='screen',
            parameters=['/home/hello-robot/ament_ws/src/stretch_seeing_eye_ros2/config/scan_filter.yaml'],
            # parameters=[join(FindPackageShare('stretch_seeing_eye_ros2').find('stretch_seeing_eye_ros2'), 'config', LaunchConfiguration('location'), 'scan_filter.yaml')]
            remappings=[]
        ),
    ])

if __name__ == '__main__':
    generate_launch_description()
