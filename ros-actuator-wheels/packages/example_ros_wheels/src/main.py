#!/usr/bin/env python3

import time

import rospy
from duckietown_msgs.msg import WheelsCmdStamped

from dt_robot_utils import get_robot_name

# parameters
FORWARD_DURATION: float = 2.0
BACKWARD_DURATION: float = 2.0
SPEED: float = 0.25
PUBLISH_HZ: float = 10.0


def stop_wheels(publisher):
    publisher.publish(WheelsCmdStamped(vel_left=0.0, vel_right=0.0))
    time.sleep(1)


def drive_for_duration(publisher, left_speed: float, right_speed: float, duration: float, rate_hz: float):
    rate = rospy.Rate(rate_hz)
    t0 = time.time()
    while not rospy.is_shutdown() and (time.time() - t0) < duration:
        publisher.publish(WheelsCmdStamped(vel_left=left_speed, vel_right=right_speed))
        rate.sleep()


def driver():
    robot_name: str = get_robot_name()
    # initialize node
    rospy.init_node('driver', anonymous=True)
    # setup publisher
    publisher = rospy.Publisher(
        f"/{robot_name}/wheels_driver_node/wheels_cmd",
        WheelsCmdStamped,
        queue_size=1,
        tcp_nodelay=True,
    )
    # stop wheels when shutting down
    rospy.on_shutdown(lambda: stop_wheels(publisher))
    rospy.sleep(1.0)

    # basic movement demo: forward, stop, backward, stop
    rospy.loginfo("Driving forward for %.1f s", FORWARD_DURATION)
    drive_for_duration(publisher, SPEED, SPEED, FORWARD_DURATION, PUBLISH_HZ)

    rospy.loginfo("Stopping")
    stop_wheels(publisher)

    rospy.loginfo("Driving backward for %.1f s", BACKWARD_DURATION)
    drive_for_duration(publisher, -SPEED, -SPEED, BACKWARD_DURATION, PUBLISH_HZ)

    rospy.loginfo("Stopping")
    stop_wheels(publisher)


if __name__ == '__main__':
    driver()
