#include <ros/ros.h>
#include <your_package/DroneState.h>
#include <map>

std::map<uint32_t, your_package::DroneState> drone_states;

void hunter1Callback(const your_package::DroneState::ConstPtr& msg) {
    drone_states[msg->id] = *msg;
}

// 为hunter2/3/4添加类似回调函数...

int main(int argc, char **argv) {
    ros::init(argc, argv, "swarm_broadcaster");
    ros::NodeHandle nh;

    // 订阅所有无人机状态
    ros::Subscriber sub1 = nh.subscribe("/hunter_1/drone_state", 10, hunter1Callback);
    ros::Subscriber sub2 = nh.subscribe("/hunter_2/drone_state", 10, hunter2Callback);
    ros::Subscriber sub3 = nh.subscribe("/hunter_3/drone_state", 10, hunter3Callback);
    ros::Subscriber sub4 = nh.subscribe("/hunter_4/drone_state", 10, hunter4Callback);
    ros::Subscriber sub5 = nh.subscribe("/runner/drone_state", 10, runnerCallback);
    

    // 创建全局状态发布者
    ros::Publisher global_pub = nh.advertise<your_package::DroneState>("/swarm/global_states", 10);

    ros::Rate rate(20);
    while (ros::ok()) {
        // 广播所有无人机状态
        for (auto& [id, state] : drone_states) {
            global_pub.publish(state);
        }
        rate.sleep();
        ros::spinOnce();
    }
    return 0;
}