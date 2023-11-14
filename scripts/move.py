#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class MoveRobotNode(Node):
    def __init__(self):
        super().__init__('move_robot_node')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        time.sleep(1)  # Wait for the publisher to be established
        self.move_robot()

    def move_robot(self):
        msg = Twist()
        msg.linear.x = 1.0  # Set linear speed (m/s)
        duration = 5  # Duration in seconds to achieve 5 meters at 1 m/s

        end_time = self.get_clock().now() + rclpy.duration.Duration(seconds=duration)
        while self.get_clock().now() < end_time:
            self.publisher_.publish(msg)

        # Stop the robot
        msg.linear.x = 0.0
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    move_robot_node = MoveRobotNode()
    rclpy.spin(move_robot_node)
    move_robot_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
