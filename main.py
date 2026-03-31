import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge

# These custom messages come from the dt-core environment
from duckietown_msgs.msg import WheelsCmdStamped
from sensor_msgs.msg import CompressedImage

class DuckieController:
    def __init__(self, vehicle_name):
        self.vehicle_name = vehicle_name
        self.bridge = CvBridge()
        
        # 1. The Wheels (Actuator from ./ros-actuator-wheels)
        self.pub_wheels = rospy.Publisher(
            f"/{self.vehicle_name}/wheels_driver_node/wheels_cmd", 
            WheelsCmdStamped, 
            queue_size=1
        )
        
        # 2. The Camera (Perception from ./ros-sensor-camera)
        self.sub_camera = rospy.Subscriber(
            f"/{self.vehicle_name}/camera_node/image/compressed", 
            CompressedImage, 
            self.camera_callback,
            queue_size=1
        )

    def camera_callback(self, msg):
        # Convert the compressed ROS image stream into a standard OpenCV array
        cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        
        # -> This is where your synthetic data pipeline or segmentation model will live <-
        # For now, let's just display what the robot sees:
        cv2.imshow("Duckie Vision", cv_image)
        cv2.waitKey(1)

    def move(self, left_speed, right_speed):
        # Speeds are floats between -1.0 (full reverse) and 1.0 (full forward)
        msg = WheelsCmdStamped()
        msg.header.stamp = rospy.Time.now()
        msg.vel_left = left_speed
        msg.vel_right = right_speed
        self.pub_wheels.publish(msg)

    def stop(self):
        # Emergency brake
        self.move(0.0, 0.0)

if __name__ == "__main__":
    # Initialize the ROS node
    rospy.init_node("basic_perception_and_movement", anonymous=True)
    
    # Replace 'robot_name' with the actual name of your Duckiebot
    bot = DuckieController("robot_name")
    
    # Wait a moment for ROS publishers to establish connection
    rospy.sleep(1) 
    
    print("Moving Forward...")
    bot.move(0.5, 0.5) 
    rospy.sleep(2)     # Drive forward for 2 seconds
    
    print("Moving Backward...")
    bot.move(-0.5, -0.5) 
    rospy.sleep(2)     # Drive backward for 2 seconds
    
    print("Stopping...")
    bot.stop()
    
    # Keep the script alive so the camera_callback continues to receive frames
    rospy.spin()