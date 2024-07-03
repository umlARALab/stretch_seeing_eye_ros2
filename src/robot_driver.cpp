#include <chrono>
#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"

using namespace std::chrono_literals;

class NavDriverNode : public rclcpp::Node {
public:
    NavDriverNode() : Node("nav_driver") {
        timer_ = this->create_wall_timer(
            500ms, std::bind(&NavDriverNode::timer_callback, this));
    }
private:
    rclcpp::TimerBase::SharedPtr timer_;

    void timer_callback() {
        timer_->cancel();
        // TODO: Figure out what's best to do here
    }
};

int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<NavDriverNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}