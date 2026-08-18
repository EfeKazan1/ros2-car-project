import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class Dinleyen(Node):
    def __init__(self):
        super().__init__("dinleyen_node")
        self.subscription= self.create_subscription(
            String,
            'alabalik',
            self.dongu,
            10)
        self.subscription

    def dongu(self,msg):
        self.get_logger().info('I heard: "%s"' %msg.data)

def main():
    rclpy.init()
    node=Dinleyen()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    