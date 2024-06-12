#include <rclcpp/rclcpp.hpp>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/msg/image.hpp>

#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using std::vector;
using std::placeholders::_1;

void loadImages(vector<cv_bridge::CvImage>& arr, const vector<std::string>& paths) {
    for (size_t i = 0; i < paths.size(); i++) {
        arr[i] = cv_bridge::CvImage();
        arr[i].image = cv::imread(paths[i]);
        arr[i].encoding = "bgr8";
    }
}

class ImagePublisher : public rclcpp::Node {
public:
    ImagePublisher()
        : Node("test_image_node"), i_(0) {
        pub_ = this->create_publisher<sensor_msgs::msg::Image>("/image", 10);

        // Add paths to your images
        paths_ = {"/home/hello-robot/Downloads/Photo1.jpg"};

        images_.resize(paths_.size());
        loadImages(images_, paths_);

        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(200), 
            std::bind(&ImagePublisher::timerCallback, this)
        );
    }

private:
    void timerCallback() {
        pub_->publish(*images_[i_].toImageMsg());
        i_ = (i_ + 1) % images_.size();
    }

    rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub_;
    rclcpp::TimerBase::SharedPtr timer_;
    vector<std::string> paths_;
    vector<cv_bridge::CvImage> images_;
    size_t i_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ImagePublisher>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}