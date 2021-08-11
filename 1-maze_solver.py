#Marcelo dos Santos
#Matheus Buratti Zagonel
#Raphael Kaviak Machnicki

import rclpy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def scan_callback(msg):
    global scan
    scan = msg.ranges
#Define as velocidades lineares e angulares
LIN_SPEED = 0.3
ANG_SPEED = 0.6

#Encontra parede
def find_wall():
    msg = Twist()
    msg.linear.x = LIN_SPEED
    msg.angular.z = -ANG_SPEED
    return msg
    
#Vira esquerda
def turn_left():
    msg = Twist()
    msg.angular.z = ANG_SPEED
    return msg
    
#Segue em frente
def follow_the_wall():    
    msg = Twist()
    msg.linear.x = LIN_SPEED
    return msg
    
def timer_callback():
    msg = Twist()
    
    #Divide em faixas de 36 graus
    #faixa1 = scan[270:306]
    faixa2 = scan[307:342]
    faixa3 = scan[343:]+scan[:18]
    faixa4 = scan[19:54]
    #faixa5 = scan[55:90]
    
    
    #Distância minima nas faixas
    #right = min(faixa1)   
    fright = min(faixa2)
    front = min(faixa3)
    fleft = min(faixa4)
    #left = min(faixa5)

    #print(distance_ahead)
    #Distancia para o robo tomar as decisoes.
    #Depende do tamanho do robo e do tamanho dos corredores
    d = 0.5

    if front > d and fleft > d and fright > d:
        print( 'case 1 - find wall')
        msg=find_wall()
    elif front < d and fleft > d and fright > d:
        print( 'case 2 - turn left')
        msg=turn_left()
    elif front > d and fleft > d and fright < d:
        print( 'case 3 - follow the wall')
        msg=follow_the_wall()
    elif front > d and fleft < d and fright > d:
        print( 'case 4 - turn right')
        msg=find_wall()
    elif front < d and fleft > d and fright < d:
        print( 'case 5 - turn left')
        msg=turn_left()
    elif front < d and fleft < d and fright > d:
        print( 'case 6 - turn left')
        msg=turn_left()
    elif front < d and fleft < d and fright < d:
        print( 'case 7 - turn left')
        msg=turn_left()
    elif front > d and fleft < d and fright < d:
        print( 'case 8 - turn right')
        msg=find_wall()
    else:
        print( 'unknown case')

    #publica os valores das velocidades
    publisher.publish(msg)


def main(args=None):

    global scan
    scan = []

    rclpy.init(args=args)

    global node
    node = rclpy.create_node('wanderbot')

    global publisher
    publisher = node.create_publisher(Twist, 'cmd_vel', rclpy.qos.qos_profile_system_default)
    sub = node.create_subscription(LaserScan, 'scan', scan_callback, rclpy.qos.qos_profile_sensor_data)
    sub

    timer = node.create_timer(0.5, timer_callback)
    timer

    rclpy.spin(node)
        
    node.destroy_node()
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()
