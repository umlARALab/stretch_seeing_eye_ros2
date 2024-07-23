cmake_minimum_required(VERSION 3.8)
project(stretch_seeing_eye_ros2)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(slam_toolbox REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(stretch_seeing_eye_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_eigen REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(rviz_visual_tools REQUIRED)
find_package(OpenCV REQUIRED)
find_package(image_rotate)

add_executable(pub src/pub.cpp)
ament_target_dependencies(pub rclcpp std_msgs)

add_executable(sub src/sub.cpp)
ament_target_dependencies(sub rclcpp std_msgs)

add_executable(test_image_node src/image_test_node.cpp)
ament_target_dependencies(test_image_node rclcpp sensor_msgs cv_bridge OpenCV)

add_executable(publish_plane src/publish_plane.cpp)
ament_target_dependencies(publish_plane rclcpp std_msgs geometry_msgs stretch_seeing_eye_msgs tf2_ros rviz_visual_tools tf2_eigen)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(TARGETS
  pub
  sub
  test_image_node
  publish_plane
  DESTINATION lib/${PROJECT_NAME})

# Install Python scripts
ament_python_install_package(${PROJECT_NAME})
install(PROGRAMS
    stretch_seeing_eye_ros2/detect_feature.py
    stretch_seeing_eye_ros2/camera_info_rotate.py
    DESTINATION lib/${PROJECT_NAME}
)

# Install launch files.
install(DIRECTORY
launch
DESTINATION share/${PROJECT_NAME}/
)

install(DIRECTORY
  config
  DESTINATION share/${PROJECT_NAME}/
)

install(DIRECTORY
  world
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
