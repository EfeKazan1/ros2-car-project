
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Konusan(Node):

    def __init__(self):
        #TODO:#BASE i KUR
        super().__init__("konusan_publisher")
        
        #TODO:publisher olustur

        self.publisher_=self.create_publisher(String,'alabalik',10)

        #TODO:1snlik timer kur

        timer_period=2

        timer_period2=5
        self.timer1=self.create_timer(timer_period,self.dongu)

        self.timer2=self.create_timer(timer_period2,self.callback2)

        self.sayac=0

        self.sayac2=0

    def dongu(self):

        #TODO:bir String() mesmesi yap
        msg=String()

        #TODO:.data alanına bir yazı koy içine self.sayacı kat
        msg.data='Selamlar: %d' % self.sayac
        #TODO:publisher ile publish et
        self.publisher_.publish(msg)

        #TODO:self.get_logger().info ile ekrana bas
        self.get_logger().info('Publishing: "%s"' % msg.data)
        #TODO:sayacı bir arttır
        self.sayac +=1

        pass

    def callback2(self):
        msg=String()

        msg.data='Bu Timer2 %d' %self.sayac2

        self.publisher_.publish(msg)

        self.get_logger().info('Publishing "%s"' % msg.data)

        self.sayac2 +=1


def main():
    rclpy.init()
    node=Konusan()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()