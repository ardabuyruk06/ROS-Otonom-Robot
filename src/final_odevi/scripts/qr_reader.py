#!/usr/bin/env python3
import rospy
import cv2
from pyzbar.pyzbar import decode
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError

class QRReader:
    def __init__(self):
        rospy.init_node('qr_reader', anonymous=True)
        self.bridge = CvBridge()
        self.pub = rospy.Publisher('/qr_code', String, queue_size=10)
        self.sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.image_callback)
        rospy.loginfo("QR Reader düğümü başlatıldı, görüntü bekleniyor...")

    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(f"CvBridge hatası: {e}")
            return

        # QR kodu çöz
        decoded_objs = decode(cv_image)
        for obj in decoded_objs:
            qr_data = obj.data.decode('utf-8')
            rospy.loginfo(f"QR Tespit Edildi: {qr_data}")
            self.pub.publish(qr_data)
            # Okumayı hızlandırmak için kısa bir mola
            rospy.sleep(1.0)

if __name__ == '__main__':
    try:
        reader = QRReader()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
