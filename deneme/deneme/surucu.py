import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class Surucu(Node):

    def __init__(self):

        super().__init__("surucu_node")

        self.publisher_=self.create_publisher(Twist,"/turtle1/cmd_vel",10)

        timer=3 #sn de bir

        self.timer=self.create_timer(timer,self.callback_publisher)

    def callback_publisher(self):

        msg=Twist()

        msg.linear.x=0.5

        msg.angular.z=0.3

        self.publisher_.publish(msg)

        self.get_logger().info(f'Ileri hiz : {msg.linear.x} Donus hizi: {msg.angular.z}')

def main():
    rclpy.init()
    node=Surucu()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
