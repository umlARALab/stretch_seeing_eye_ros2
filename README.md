# Seeing-Eye Stretch

## Launching the Robot

### CHANGE THIS TODO

#### Launch nav
```shell
$ ros2 launch stretch_nav2 navigation.launch.py map:=${HELLO_FLEET_PATH}/maps/<map_name>.yaml use_rviz:=false teleop_type:=none
$ ros2 launch nav2_bringup rviz_launch.py
```
launch these in separate terminal
#### Launch mapping
```shell
$ ros2 launch stretch_nav2 offline_mapping.launch.py use_rviz:=false teleop_type:=none
$ ros2 launch nav2_bringup rviz_launch.py
```
save using:
```shell
$ ros2 run nav2_map_server map_saver_cli -f ${HELLO_FLEET_PATH}/maps/<map_name>
```

### Real Robot Generating Map
```shell
$ ros2 launch stretch_seeing_eye_ros2 robot_driver.launch.py
```

### Real Robot with Map
```shell
$ ros2 launch stretch_seeing_eye_ros2 robot_driver.launch.py location:=[map directory name]
```

### Gazebo Simulation with Map
> See [Gazebo Inter-op](#gazebo-inter-op) for more details.
```shell
# Shell 1
$ ros2 launch stretch_seeing_eye_ros2 robot_driver.launch.py location:=[map directory name] simulation_world:=[Gazebo world file]

# Shell 2
# Launch your remapped robot model
```

### Gazebo Simulation Generating Map
```shell
# Shell 1
$ ros2 launch stretch_seeing_eye_ros2 robot_driver.launch.py simulation_world:=[Gazebo world file]

# Shell 2
# Launch your remapped robot model
```

## Gazebo Inter-op

### Prerequisites
- Gazebo Fortress (LTS)
- ROS2 Humble
- The `ros_gz` package
([More info](https://gazebosim.org/docs/fortress/ros_installation))

### Setup
All robot models intended to be used with Seeing-Eye Stretch should have their
topics remapped to `/seeing_eye/topic_name_here` to prevent topic name
conflicts with other robots, as well as to remove any confusion when working
with robot models.

Quite a few robot models with Gazebo Fortress integration usually come
pre-configured in their own ROS package. If this is the case, all that needs to
be done is to redirect the ros-gz-bridge params file present in the cloned
package to instead publish to the `/seeing_eye` namespace. For robot models
that aren't the stretch2, this would also involve remapping the topics of the
original model to bind with whatever the stretch2 equivalent would be.

To make Gazebo `.world` files visible to the server, simply copy the desired
files over to the `world` directory located in the `stretch_seeing_eye_ros2`
package.
