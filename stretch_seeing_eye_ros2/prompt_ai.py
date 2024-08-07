#! /usr/bin/env python3

import rclpy
from rclpy.node import Node 

from std_msgs.msg import String as ROSString
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import base64
import requests
import json

import speech_recognition as sr
import pyttsx3
import pyaudio
import wave
import numpy as np
import usb.core
import struct
import time
import os
import sys
from contextlib import contextmanager

import argparse

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np

@contextmanager
def ignore_stderr():
    devnull = None
    try:
        devnull = os.open(os.devnull, os.O_WRONLY)
        stderr = os.dup(2)
        sys.stderr.flush()
        os.dup2(devnull, 2)
        try:
            yield
        finally:
            os.dup2(stderr, 2)
            os.close(stderr)
    finally:
        if devnull is not None:
            os.close(devnull)


def get_respeaker_device_id():
    with ignore_stderr():
        p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    # print(num_devices)
    device_id = -1
    for i in range(num_devices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            if "ReSpeaker" in p.get_device_info_by_host_api_device_index(0, i).get('name'):
                device_id = i

    return device_id

# class CameraRotateNode(Node):
#     def __init__(self):
#         super().__init__("camera_info_rotate")
#         self.info_sub = self.create_subscription(
#             Image,
#             "rotated/image",
#             self.img_callback,
#             10
#         )
#         # self.info_pub = self.create_publisher(CameraInfo, "rotated/depth/camera_info", 10)

#         self.recognizer = sr.Recognizer()
#         print(get_respeaker_device_id())
#         self.mic = sr.Microphone(get_respeaker_device_id())
#         # engine = pyttsx3.init()




class SimplePubSub(Node):
    def __init__(self):
        super().__init__('base64_node')

        # self.publisher_ = self.create_publisher(ROSString, '/base_64' , 10)

        # self.cap = cv2.VideoCapture(0)
        self.br = CvBridge()
        self.recognizer = sr.Recognizer()
        self.get_logger().info(get_respeaker_device_id())
        self.mic = sr.Microphone(get_respeaker_device_id())
        # engine = pyttsx3.init()

        self.timer = self.create_timer(0.1, self.listen_for_commands)
        self.subscription = self.create_subscription(Image, 'rotated/image', self.img_listener_callback, 10)
        self.messages = []
        self.image_as_text = None
        # self.current_frame = None

    def listen_for_commands(self):
        with self.mic as source:
            self.get_logger().info("listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                audio = self.recognizer.listen(source)
                try:
                    command = self.recognizer.recognize_google(audio).lower()
                    self.get_logger().info(command)
                    self.get_logger().info("processed image") 
                    self.messages.append({"role": "user", 
                                    "content": command,
                                    "images": [self.image_as_text[2:-1]],
                                    })
                    # self.get_logger().info(self.messages)
                    message = self.chat(self.messages)
                    self.messages.append(message)
                    self.get_logger().info("\n\n")
                except sr.UnknownValueError:
                    self.get_logger().info("unknown value error")
                    # engine.runAndWait()
                except sr.RequestError:
                    self.get_logger().info("request error")

    def img_listener_callback(self, data):

        current_frame = self.br.imgmsg_to_cv2(data)
        retval, buffer = cv2.imencode('.png', current_frame)
        self.image_as_text = str(base64.b64encode(buffer))
        # self.get_logger().info(jpg_as_text)
        # f = open("img.txt", "w")
        # f.write(jpg_as_text[2:-1])
        # f.close()
        # exit(0)  
        # self.publisher_.publish(ROSString(jpg_as_text))

        # self.get_logger().info("processed image") 
        # self.messages.append({"role": "user", 
        #                  "content": "What is in this image?",
        #                  "images": [jpg_as_text[2:-1]],
        #                  })
        # # self.get_logger().info(self.messages)
        # message = self.chat(self.messages)
        # self.messages.append(message)
        # self.get_logger().info("\n\n")

    def chat(self, messages):
        r = requests.post(
            "http://localhost:3333/api/chat",
            json={"model": "llava", "messages": messages, "stream": False},
        stream=False
        )
        r.raise_for_status()
        output = ""
        self.get_logger().info("initiated response")
        for line in r.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(body["error"])
           
            message = body.get("message", "")
            content = message.get("content", "")
            output += content                

            if body.get("done", False):
                self.get_logger().info(output)
                message["content"] = output
                return message
            


def main(args=None):
    rclpy.init(args=args)
    simple_pub_sub = SimplePubSub()
    rclpy.spin(simple_pub_sub)
    simple_pub_sub.destroy_node()
    rclpy.shutdown()

  
if __name__ == '__main__':
  main()
