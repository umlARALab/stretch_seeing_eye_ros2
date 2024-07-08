from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            "teleop_type",
            default_value="keyboard",
            description="how to teleop ('keyboard', 'joystick', or 'none')"
        ),
        DeclareLaunchArgument(
            "linear",
            default_value="0.04",
            description="linear speed (m/s)"
        ),
        DeclareLaunchArgument(
            "angular",
            default_value="1.0",
            description="angular speed (rad/s)"
        ),
        DeclareLaunchArgument(
            "twist_topic",
            default_value="/stretch/cmd_vel",
            description="topic to command Twist messages"
        ),
        DeclareLaunchArgument(
            "joystick_port",
            default_value="/dev/input/js0",
            description="joystick USB device name"
        ),
        GroupAction(
            condition=IfCondition(
                PythonExpression([
                    "'", LaunchConfiguration("teleop_type"), "' == 'keyboard'"
                ])
            ),
            actions = [
                Node(
                    package="teleop_twist_keyboard",
                    executable="teleop_twist_keyboard",
                    name="teleop_twist_keyboard",
                    output="screen",
                    # teleop_twist_keyboard doesn't like running in the same terminal
                    # that it's launched in, so we create a new one.
                    prefix="xterm -e",
                    parameters=[{
                        "speed": LaunchConfiguration("linear"),
                        "turn": LaunchConfiguration("angular")
                    }],
                    remappings=[
                        ("/cmd_vel", LaunchConfiguration("twist_topic"))
                    ]
                )
            ]
        ),
        GroupAction(
            condition=IfCondition(
                PythonExpression([
                    "'", LaunchConfiguration("teleop_type"), "' == 'joystick'"
                ])
            ),
            actions = [
                Node(
                    package="joy",
                    executable="joy_node",
                    name="joy",
                    output="screen",
                    parameters=[{
                        "dev": LaunchConfiguration("joystick_port"),
                        "autorepeat_rate": "20",
                        "deadzone": "0.05"
                    }]
                ),
                Node(
                    package="teleop_twist_joy",
                    executable="teleop_node",
                    name="teleop_twist_joy",
                    output="screen",
                    parameters=[{
                        "enable_button": "0",
                        "scale_linear": LaunchConfiguration("linear"),
                        "scale_angular": LaunchConfiguration("angular")
                    }],
                    remappings=[
                        ("/cmd_vel", LaunchConfiguration("twist_topic"))
                    ]
                )
            ]
        )
    ])
