import numpy as np
import matplotlib.pyplot as plt
import rospy
import message_filters
from  message_filters import ApproximateTimeSynchronizer
from std_msgs.msg import String
from fs_msgs.msg import Track, Cone
from geometry_msgs.msg import Point
from pose_msgs.msg import Cone_Points
from nav_msgs.msg import Odometry
from std_msgs.msg import Int8
from localization_test.msg import data
import time
import math
import fsds #fsds client
#this node is used to send info of the Python API to ROS so it can be used for Lidar motion compensation

# connect to the AirSim simulator
client = fsds.FSDSClient()

# Check network connection
client.confirmConnection()



print("yes")
msg = data()
pub = rospy.Publisher('/data', data, queue_size=10)
rospy.init_node('data_pub', anonymous=True)
rate = rospy.Rate(250) #250 hz 
while not rospy.is_shutdown():
    imu = client.getImuData()
    print("angular velocity: ", imu.angular_velocity)
    state = client.getCarState()
    print("linear velocity x", state.kinematics_estimated.linear_velocity.x_val)
    print("linear velocity y", state.kinematics_estimated.linear_velocity.y_val)
    print("linear velocity z", state.kinematics_estimated.linear_velocity.z_val)
    msg.speed = abs(state.kinematics_estimated.linear_velocity.x_val)
    msg.angular_velocity = imu.angular_velocity.z_val
    pub.publish(msg)
    rate.sleep()
