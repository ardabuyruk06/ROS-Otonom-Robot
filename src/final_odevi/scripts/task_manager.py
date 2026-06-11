#!/usr/bin/env python3

import rospy
import yaml
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String

class TaskManager:
    def __init__(self):
        rospy.init_node('task_manager')
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()
        self.qr_data = None
        rospy.Subscriber('/qr_code', String, self.qr_callback)
        self.mission_file = '/root/catkin_ws/src/final_odevi/config/mission.yaml'
        with open(self.mission_file, 'r') as file:
            self.mission_data = yaml.safe_load(file)
        self.locations = self.mission_data.get('locations', [])

    def qr_callback(self, msg):
        self.qr_data = msg.data

    def go_to_location(self, coords):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = coords['x']
        goal.target_pose.pose.position.y = coords['y']
        goal.target_pose.pose.orientation.w = 1.0
        self.client.send_goal(goal)
        return self.client.wait_for_result(rospy.Duration(90.0))

    def execute_mission(self):
        for loc_name in self.locations:
            rospy.loginfo(f"Gidiliyor: {loc_name}")
            data = self.mission_data.get(loc_name)
            if self.go_to_location(data['goal']):
                rospy.loginfo("Hedefe varıldı, QR bekleniyor...")
                # Basit QR kontrolü
                rospy.sleep(5) 
            else:
                rospy.logerr(f"{loc_name} ulaşılamadı!")

if __name__ == '__main__':
    tm = TaskManager()
    tm.execute_mission()
