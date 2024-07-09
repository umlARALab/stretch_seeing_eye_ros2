# Seeing-Eye Stretch

## Gazebo Inter-op

> NOTE: This section is currently a WIP, with this primarily functioning more
like a proposal.

### Prerequisites (WIP)
- Gazebo Fortress (LTS)
- ROS2 Humble
- The `ros_gz` package
([More info](https://gazebosim.org/docs/fortress/ros_installation))

All robot models (physical or simulation) intended to be used with
Seeing-Eye Stretch should have their topics remapped to
`/seeing_eye/topic_name_here` to prevent topic name conflicts with other
robots, as well as to remove any confusion when working with robot models.

Quite a few robot models with Gazebo Fortress integration usually come
pre-configured in their own ROS package. As such, it may be more efficient to
redirect the ros-gz-bridge config file present in the cloned package
to instead publish to the `/seeing_eye` namespace, rather than trying to store
and launch the .sdf models within the stretch_seeing_eye_ros2 package itself.

For robot models that aren't the stretch2, this would also involve remapping
the topics of the original model to bind with whatever the stretch2 equivalent
would be.

This way, the Seeing-Eye Stretch source code does not need to know about which
model is currently in use. The only thing the source needs to worry about is if
all topics are being published.

### Gazebo Simulation with Map (WIP)
```shell
# Shell 1
$ ros2 launch stretch_seeing_eye_ros2 robot_driver.launch.py location:=[map directory name] simulation_world:=[Gazebo world file]

# Shell 2
# Launch your remapped robot model
```

### Real Robot Generating Map (WIP)
**TODO**

### Real Robot with Map (WIP)
**TODO**