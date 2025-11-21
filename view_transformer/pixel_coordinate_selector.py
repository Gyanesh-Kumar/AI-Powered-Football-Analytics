import cv2
import numpy as np
import matplotlib.pyplot as plt

class PixelCoordinateSelector:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        self.pixel_vertices = []

    def select_points(self):
        def get_points(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                # Record the selected point
                self.pixel_vertices.append((x, y))
                # Draw a small circle on the image to mark the selection
                cv2.circle(self.image, (x, y), 5, (0, 255, 0), -1)
                # Display the image using matplotlib
                plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
                plt.show()

        # Display the image using matplotlib
        plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        plt.show()

        cv2.setMouseCallback('Select Points', get_points)

        print("Click on the 4 corners of the court in the image. Press 'q' when done.")
        
        # Wait for the user to press 'q' to quit
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if len(self.pixel_vertices) == 4:
            print("Selected pixel coordinates:", self.pixel_vertices)
        else:
            print("Error: Please select exactly 4 points.")
        return np.array(self.pixel_vertices, dtype=np.float32)

# Example Usage:
selector = PixelCoordinateSelector(r'c:/Users/gykukuma/Desktop/MiniProject/input_videos/football-pitch-image.png')
pixel_vertices = selector.select_points()
