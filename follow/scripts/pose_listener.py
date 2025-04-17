#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped, TwistStamped
from std_msgs.msg import Float64

# 回调函数，处理每个无人机的位置信息
def position_callback(data, drone_id):
    # 发布位置信息（位置的每个坐标 x, y, z）
    rospy.loginfo(f"无人机 {drone_id} 的位置: x={data.pose.position.x}, y={data.pose.position.y}, z={data.pose.position.z}")
    pub_position_x.publish(data.pose.position.x)
    pub_position_y.publish(data.pose.position.y)
    pub_position_z.publish(data.pose.position.z)

# 回调函数，处理每个无人机的速度信息
def velocity_callback(data, drone_id):
    # 发布速度信息（速度的每个分量 vx, vy, vz）
    rospy.loginfo(f"无人机 {drone_id} 的速度: vx={data.twist.linear.x}, vy={data.twist.linear.y}, vz={data.twist.linear.z}")
    pub_velocity_x.publish(data.twist.linear.x)
    pub_velocity_y.publish(data.twist.linear.y)
    pub_velocity_z.publish(data.twist.linear.z)

def listener():
    # 初始化 ROS 节点
    rospy.init_node('multi_drone_position_velocity_listener', anonymous=True)

    # 定义无人机的命名空间（根据你的 launch 文件的配置）
    drone_ids = ['hunter_1', 'hunter_2', 'hunter_3', 'hunter_4']

    # 创建发布者用于发布位置和速度
    global pub_position_x, pub_position_y, pub_position_z
    global pub_velocity_x, pub_velocity_y, pub_velocity_z
    pub_position_x = rospy.Publisher('/multi_drone/position_x', Float64, queue_size=10)
    pub_position_y = rospy.Publisher('/multi_drone/position_y', Float64, queue_size=10)
    pub_position_z = rospy.Publisher('/multi_drone/position_z', Float64, queue_size=10)

    pub_velocity_x = rospy.Publisher('/multi_drone/velocity_x', Float64, queue_size=10)
    pub_velocity_y = rospy.Publisher('/multi_drone/velocity_y', Float64, queue_size=10)
    pub_velocity_z = rospy.Publisher('/multi_drone/velocity_z', Float64, queue_size=10)

    # 为每个无人机订阅位置和速度话题
    for drone_id in drone_ids:
        position_topic = f'/{drone_id}/mavros/local_position/pose'
        velocity_topic = f'/{drone_id}/mavros/local_position/velocity_local'
        rospy.Subscriber(position_topic, PoseStamped, position_callback, drone_id)
        rospy.Subscriber(velocity_topic, TwistStamped, velocity_callback, drone_id)

    # 保持节点运行，直到 ROS 被关闭
    rospy.spin()

if __name__ == '__main__':
    listener()
