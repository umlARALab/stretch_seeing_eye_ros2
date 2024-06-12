from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='stretch_seeing_eye_ros2',
            executable='test_image_node',
            name='test_image_node',
            output='screen',
            # remappings=[('/image','/camera/color/image_raw')]
        )
    ])
