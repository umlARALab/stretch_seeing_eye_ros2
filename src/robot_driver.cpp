#include <algorithm>
#include <chrono>
#include <functional>
#include <map>
#include <memory>
#include <sstream>
#include <string>
#include <vector>

#include "rclcpp/rclcpp.hpp"

using namespace std::chrono_literals;

// Call this if you plan on reusing the same string stream.
void clear_oss_buffer(std::ostringstream& oss) {
    oss.clear();
    oss.seekp(0);  // Moves pointer back to start. Prevents unecessary reallocation.
}

class RobotDriverNode : public rclcpp::Node {
public:
    RobotDriverNode() : Node("robot_driver") {
        timer_ = this->create_wall_timer(
            1s, std::bind(&RobotDriverNode::timer_callback, this)
        );
    }
private:
    rclcpp::TimerBase::SharedPtr timer_;

    std::vector<std::string> assert_published_topics() {
        auto topics_map = rclcpp::Node::get_topic_names_and_types();

        // This is not supposed to be an exhaustive list of stretch2 topics,
        // only the ones that are relevant.
        std::vector<std::string> topics = {"/seeing_eye/cmd_vel", "/seeing_eye/odom"};
        topics.erase(
            std::remove_if(
                topics.begin(), topics.end(),
                [topics_map](std::string s) { return topics_map.count(s) != 0; }
            ),
            topics.end()
        );
        return topics;
    }

    std::string form_missing_topics_error_message(std::vector<std::string> topics) {
        std::ostringstream oss;
        std::copy(
            topics.begin(), topics.end(),
            std::ostream_iterator<std::string>(oss, ", ")
        );
        int last_delim_length = 2;
        return "The following topics could not be found: "
            + oss.str().substr(0, oss.str().size() - last_delim_length);
    }

    void timer_callback() {
        timer_->cancel();
        std::vector<std::string> missing_topics = assert_published_topics();
        if (missing_topics.empty()) {
            RCLCPP_INFO(this->get_logger(), "All topics found");
        } else {
            std::string msg = form_missing_topics_error_message(missing_topics);
            RCLCPP_FATAL(this->get_logger(), msg.c_str());
            // TODO: Is exiting within the node OK, or do we want to exit from main?
            exit(1);
        }
    }
};

int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<RobotDriverNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}