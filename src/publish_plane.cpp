#include <geometry_msgs/msg/point.hpp>
#include <geometry_msgs/msg/point32.hpp>
#include <geometry_msgs/msg/polygon.hpp>
#include <rclcpp/rclcpp.hpp>
#include <rviz_visual_tools/rviz_visual_tools.hpp>
#include <stretch_seeing_eye_msgs/srv/feature.hpp>

#define SIZE 0.2

namespace rvt = rviz_visual_tools;

rvt::RvizVisualToolsPtr visual_tools_;

enum rvt::Colors COLORS[] = {
    rvt::YELLOW,
    rvt::ORANGE,
    rvt::RED,
};

void publish_plane(const std::shared_ptr<rmw_request_id_t> request_header,
                   const std::shared_ptr<stretch_seeing_eye_msgs::srv::Feature::Request> req, 
                   std::shared_ptr<stretch_seeing_eye_msgs::srv::Feature::Response> res) {
    (void)request_header; // To avoid unused parameter warning
    (void)res; // To avoid unused parameter warning

    RCLCPP_DEBUG(rclcpp::get_logger("rclcpp"), "Publishing plane");

    if (req->points.size() < 3) {
        for (const auto &point : req->points) {
            geometry_msgs::msg::Point p1, p2;
            p1.x = point.x - SIZE;
            p1.y = point.y - SIZE;
            p1.z = 0.0;
            p2.x = point.x + SIZE;
            p2.y = point.y + SIZE;
            p2.z = SIZE;
            visual_tools_->publishCuboid(p1, p2, COLORS[req->detail_level]);
        }
    } else {
        geometry_msgs::msg::Polygon polygon;
        polygon.points = req->points;
        visual_tools_->publishPolygon(polygon, rvt::RED);
    }

    visual_tools_->trigger();
}

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("publish_plane");

    visual_tools_ = std::make_shared<rvt::RvizVisualTools>("map", "/visualization_marker_array", node);

    visual_tools_->loadMarkerPub();

    rclcpp::sleep_for(std::chrono::seconds(1));

    auto service = node->create_service<stretch_seeing_eye_msgs::srv::Feature>(
        "/stretch_seeing_eye/create_marker", &publish_plane);

    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
