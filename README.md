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
model is currently in use nor if it is/isn't being run in a simulation.
The only thing the source needs to worry about is if all topics are being
published.

### Launching the Simulation (WIP)
1. Launch the robot (or Gazebo simulation) intended to be used.
2. Ensure that topics are being published with `ros2 topic list`
3. Launch `robot_driver.launch.py` (*TODO: What happens here?*)
4. (*TODO: What should happen after the robot driver?*)