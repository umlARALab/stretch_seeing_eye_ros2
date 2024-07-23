#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo
import numpy as np

class CameraRotateNode(Node):
    def __init__(self):
        super().__init__("camera_info_rotate")
        self.info_sub = self.create_subscription(
            CameraInfo,
            "camera/depth/camera_info",
            self.info_callback,
            10
        )
        self.info_pub = self.create_publisher(CameraInfo, "rotated/depth/camera_info", 10)

    def info_callback(self, msg):
        rotated_info = CameraInfo()
        rotated_info.header = msg.header
        rotated_info.height = msg.width
        rotated_info.width = msg.height
        rotated_info.distortion_model = msg.distortion_model
        rotated_info.d = msg.d

        # Rotate the intrinsic matrix K
        K = np.array(msg.k).reshape(3, 3)
        K_rot = np.array([
            [K[1, 1], 0, msg.height - K[1, 2]],
            [0, K[0, 0], K[0, 2]],
            [0, 0, 1]
        ])
        rotated_info.k = K_rot.flatten().tolist()

        # Rotate the projection matrix P
        P = np.array(msg.p).reshape(3, 4)
        P_rot = np.array([
            [P[1, 1], 0, msg.height - P[1, 2], P[1, 3]],
            [0, P[0, 0], P[0, 2], P[0, 3]],
            [0, 0, 1, 0]
        ])
        rotated_info.p = P_rot.flatten().tolist()

        self.info_pub.publish(rotated_info)

def main(args=None):
    rclpy.init(args=args)
    node = CameraRotateNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
