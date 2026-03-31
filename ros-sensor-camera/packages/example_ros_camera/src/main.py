#!/usr/bin/env python3

import cv2
import numpy as np
import rospy
from sensor_msgs.msg import CompressedImage
from turbojpeg import TurboJPEG

from dt_robot_utils import get_robot_name

# camera info
WIDTH: int = 640
HEIGHT: int = 480
SIZE_4MB: int = 4 * 1024 * 1024

# JPEG decoder
jpeg = TurboJPEG()

# create empty matplot window
window = "example-sensor-camera"
cv2.namedWindow(window, cv2.WINDOW_AUTOSIZE)

# log stats every N frames to keep output readable
LOG_EVERY_N_FRAMES: int = 30
frame_counter: int = 0


def callback(msg: CompressedImage):
    global frame_counter

    frame: np.ndarray = jpeg.decode(msg.data)

    # basic "sensor reading" example:
    # compute brightness and center pixel values from the camera image
    gray: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean_brightness: float = float(np.mean(gray))
    center_y: int = frame.shape[0] // 2
    center_x: int = frame.shape[1] // 2
    center_bgr = frame[center_y, center_x].tolist()

    frame_counter += 1
    if frame_counter % LOG_EVERY_N_FRAMES == 0:
        rospy.loginfo(
            "frame=%d brightness=%.1f center_bgr=%s",
            frame_counter,
            mean_brightness,
            center_bgr,
        )

    # display frame
    cv2.imshow(window, frame)
    cv2.waitKey(1)


def listener():
    robot_name: str = get_robot_name()
    # initialize node
    rospy.init_node('listener', anonymous=True)
    # setup camera listener
    rospy.Subscriber(
        f"/{robot_name}/camera_node/image/compressed",
        CompressedImage,
        callback,
        buff_size=SIZE_4MB,
        queue_size=1
    )
    # keep the node alive
    rospy.spin()


if __name__ == '__main__':
    listener()
