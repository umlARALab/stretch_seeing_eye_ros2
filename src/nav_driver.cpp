#include <chrono>
#include <functional>
#include <map>
#include <string>

#include "rclcpp/rclcpp.hpp"

using namespace std::chrono_literals;

class NavDriverNode : public rclcpp::Node {
public:
    NavDriverNode() : Node("nav_driver") {
        this->declare_parameter("use_gazebo", false);
        this->declare_parameter("robot_model_filename", "stretch.sdf");
        timer_ = this->create_wall_timer(
            500ms, std::bind(&NavDriverNode::timer_callback, this));
    }
private:
    rclcpp::TimerBase::SharedPtr timer_;

    void timer_callback() {
        timer_->cancel();
        bool use_gazebo = this->get_parameter("use_gazebo").as_bool();
        if (use_gazebo) {
            RCLCPP_INFO(this->get_logger(), "Gazebo set to true!");
        } else {
            RCLCPP_INFO(this->get_logger(), "Gazebo set to false!");
        }
    }
};

int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<NavDriverNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}