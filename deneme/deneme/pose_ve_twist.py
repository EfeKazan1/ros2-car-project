import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu,LaserScan
from rclpy.node import Node
from enum import IntEnum
import random
import math


class States(IntEnum):
    HEDEF_SEC=0
    DON=1
    HAREKET=2
    


class StateMachine:
    def __init__(self):
        self.current_state=States.HEDEF_SEC

    def update(self,x,y,theta,Kp,Kaci,lidar_min,lidar_sol,lidar_sag,threshold):

        v, w = 0.0, 0.0

        match self.current_state:
            case States.HEDEF_SEC:
                self.goal_x=random.randint(-5,5)
                self.goal_y=random.randint(-5,5)
                #BAKTIGIM YONE GORE NEREMDE KALIYOR
                dx=self.goal_x-x
                dy=self.goal_y-y
                self.hedef_yon=math.atan2(dy,dx)

                self.current_state=States.DON

            case States.DON:
                #Simdi secilen hedef ile bizim theta arasındaki açı farkına bakalım
            
                hata=self.hedef_yon - theta #AÇI FARKI BU RADYAN

                if hata > math.pi:
                    hata-=2 * math.pi
                elif hata < -math.pi:
                    hata+= 2* math.pi

                if(abs(hata)<0.01):
                    w=0.0
                    v= 0.0
                    self.current_state=States.HAREKET
                else:
                    w= max(-2.0, min(2.0, Kaci * hata))

                    v= 0.0

            case States.HAREKET:

                #dx dy yi hesaplar
                dx=self.goal_x-x
                dy=self.goal_y-y

                hata_konum=math.hypot(dx,dy)

                if(lidar_min is not None and lidar_min <threshold):

                    hata = threshold - lidar_min

                    yon = 1.0 if lidar_sol else -1.0

                    w = yon * Kaci * hata

                    v = 0.2


                elif abs(hata_konum)<0.05:
                    v=0.0
                    w=0.0
                    self.current_state=States.HEDEF_SEC
                else:
                    guncel_yon=math.atan2(dy,dx) #AÇI FARKI BU RADYAN

                    hata= guncel_yon  - theta

                    if hata > math.pi:
                        hata-=2 * math.pi
                    elif hata < -math.pi:
                        hata+= 2* math.pi

                    
                    v = min(Kp * hata_konum,1.0)
                    w = Kaci * hata
                

            



        return v,w

class Surucu(Node):

    def __init__(self):
        super().__init__("surucu_node")

        self.publisher_=self.create_publisher(Twist,"/cmd_vel",10)

        self.subscription= self.create_subscription(
            Odometry,
            '/model/arabam/odometry_with_covariance',
            self.callback_pose,
            10)
        
        self.subscription=self.create_subscription(
            Imu,
            '/imu',
            self.callback_imu,
            10)

        self.subscription=self.create_subscription(
            LaserScan,
            '/lidar',
            self.callback_laser,
            10
        )

        self.subscription

        self.x=0.0

        self.y=0.0

        self.theta=0.0

        timer=0.05

        self.timer=self.create_timer(timer,self.callback_publisher)

        self.fsm = StateMachine()

        self.son_yazilan=None

        self.lazer_sol=None

        self.lazer_sag=None

        self.threshold=1.8

        self.lidar_min = None


    def callback_pose(self,msg):

        self.x=msg.pose.pose.position.x

        self.y=msg.pose.pose.position.y
        
    def callback_imu(self,msg):

        q=msg.orientation

        sin_q=2.0 * (q.w * q.z + q.x * q.y)

        cos_q= 1.0 - 2.0 *(q.y * q.y + q.z * q.z)

        yaw_rad = math.atan2(sin_q,cos_q)

        self.theta=yaw_rad

    def callback_laser(self,msg):

        n=len(msg.ranges)

        orta = n // 2

        her_yone_isin_miktari=90

        on_dilim = msg.ranges[orta-her_yone_isin_miktari : orta+her_yone_isin_miktari]

        on_lidar=[on for on in on_dilim if on!=float("inf")]

        self.lidar_min = min(on_lidar) if on_lidar else float("inf")

        sol_lidar=[sol for sol in msg.ranges[n//2:] if sol!=float("inf")]

        sag_lidar=[sag for sag in msg.ranges[:n//2] if sag!=float("inf")]

        sag_agirlik=sum(sag_lidar)/len(sag_lidar) if sag_lidar else 999

        sol_agirlik=sum(sol_lidar)/len(sol_lidar) if sol_lidar else 999

        if sol_agirlik >= sag_agirlik:

            self.lazer_sol = True

            self.lazer_sag = False

        else:

            self.lazer_sol = False
            
            self.lazer_sag = True


    def callback_publisher(self):


        v, w = self.fsm.update(self.x, self.y, self.theta,0.2,2,self.lidar_min,self.lazer_sol,self.lazer_sag,self.threshold)

        yeni = (self.fsm.goal_x , self.fsm.goal_y)
        if yeni!=self.son_yazilan:
            self.get_logger().info(f'Yeni Hedef: ({yeni[0]:.2f}, {yeni[1]:.2f})')
            self.son_yazilan=yeni

        msg=Twist()

        msg.linear.x = v

        msg.angular.z= w

        self.publisher_.publish(msg)

        self.get_logger().info(
            f'\nIleri hiz : {msg.linear.x}'
            f'\nDonus hizi : {msg.angular.z}'
            f'\nHedef X: {self.fsm.goal_x}'
            f'\nHedef Y: {self.fsm.goal_y}'
            f'\nKonumum X: {self.x}'
            f'\nKonumum Y: {self.y}'
            f'\nYaw (Derece): {math.degrees(self.theta):.2f}'
            f'\nlidar_min: {self.lidar_min}'
        )

        

def main():
    rclpy.init()
    node=Surucu()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

