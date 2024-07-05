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

class NavDriverNode : public rclcpp::Node {
public:
    NavDriverNode() : Node("nav_driver") {
        timer_ = this->create_wall_timer(
            1s, std::bind(&NavDriverNode::timer_callback, this)
        );
    }
private:
    rclcpp::TimerBase::SharedPtr timer_;

    std::vector<std::string> assert_published_topics() {
        auto topics_map = rclcpp::Node::get_topic_names_and_types();
        std::ostringstream oss;

        oss << "Topics found: " << topics_map.size();
        RCLCPP_DEBUG(this->get_logger(), oss.str().c_str());

        // This is not supposed to be an exhaustive list of stretch2 topics,
        // only the ones that appear to be necessary or relevant.
        std::vector<std::string> topics = {"/cmd_vel", "/odom"};
        topics.erase(
            std::remove_if(
                topics.begin(), topics.end(),
                [topics_map](std::string s) { return topics_map.count("/seeing_eye" + s) != 0; }
            ),
            topics.end()
        );
        return topics;
    }

    void timer_callback() {
        timer_->cancel();
        std::vector<std::string> missing_topics = assert_published_topics();
        if (missing_topics.empty()) {
            RCLCPP_INFO(this->get_logger(), "All topics found");
        } else {
            std::ostringstream oss;
            std::copy(
                missing_topics.begin(), missing_topics.end(),
                std::ostream_iterator<std::string>(oss, ", ")
            );
            std::string msg =  "The following topics could not be found: " + oss.str();
            RCLCPP_FATAL(this->get_logger(), msg.c_str());
            // TODO: Is exiting within the node OK, or do we want to exit from main?
            exit(1);
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