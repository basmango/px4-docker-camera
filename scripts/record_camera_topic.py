import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        
        self.subscription = self.create_subscription(
            Image,
            '/processed_image',  # Update to '/camera'
            self.image_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()
        self.video_writer = None

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            if self.video_writer is None:
                height, width, channels = cv_image.shape
                video_filename = 'output_video.avi'  # Replace 'output_video.avi' with desired video file name
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                self.video_writer = cv2.VideoWriter(video_filename, fourcc, 40.0, (width, height))

            self.video_writer.write(cv_image)

        except Exception as e:
            self.get_logger().info(f"Error processing image: {e}")

def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    if image_subscriber.video_writer is not None:
        image_subscriber.video_writer.release()
    image_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
