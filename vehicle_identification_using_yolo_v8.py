# -*- coding: utf-8 -*-
"""Vehicle Identification Using YOLO V8

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aPeuycq8KY6f_N-PY1uNNClf-XEIXmNb
"""

!pip install ultralytics
!pip install cvzone

from google.colab import files
uploaded = files.upload()

for filename in uploaded.keys():
    print(f'Uploaded file: {filename}')

import math

class Tracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0


    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 35:
                    self.center_points[id] = (cx, cy)
#                    print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids

"""YOLO V8 FOR IMAGES"""

from google.colab import files
uploaded = files.upload()

import cv2
import os
from ultralytics import YOLO
from google.colab.patches import cv2_imshow  # Import cv2_imshow for Colab

# Load YOLO model
model = YOLO('yolov8s.pt')

# Loop through the uploaded files and process them
for file_name in uploaded.keys():
    # Read the image file
    img = cv2.imread(file_name)

    # Perform inference
    results = model(img)

    # Initialize a list to store vehicle bounding boxes
    vehicles = []

    # Iterate over the results and filter for vehicles only
    for result in results[0].boxes:  # Access boxes from the result
        x, y, w, h = result.xywh[0]  # Access the x, y, width, height
        conf = result.conf[0]  # Access confidence score
        cls = int(result.cls[0])  # Access class id
        class_label = model.names[cls]  # Get class label from YOLO

        # Check if the detected object is a vehicle (car, bus, truck)
        if 'car' in class_label or 'bus' in class_label or 'truck' in class_label:
            x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)
            vehicles.append([x1, y1, x2, y2, conf, class_label])

    # Annotate the image with bounding boxes
    for bbox in vehicles:
        x1, y1, x2, y2, conf, label = bbox
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.putText(img, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Show the image with detections using cv2_imshow in Colab
    cv2_imshow(img)  # This will display the image in Colab

"""YOLO V8 FOR VIDEO"""

from google.colab import files
uploaded = files.upload()

# Function to print the mouse position in RGB window
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point)

# Initialize video capture with the video file
cap = cv2.VideoCapture('tf.mp4')

# Open the 'coco.txt' file containing class names and read its content
with open("coco.txt", "r") as my_file:
    class_list = my_file.read().split("\n")  # Split the content by newline to get a list of class names

# Initialize counters and trackers
count = 0
car_count = 0
bus_count = 0
truck_count = 0
tracker = Tracker()  # Ensure you have a Tracker class defined in tracker.py
cy1 = 184
cy2 = 209
offset = 8

# Start processing the video frame by frame
while True:
    ret, frame = cap.read()  # Read a frame from the video
    if not ret:  # If no frame is read (end of video), break the loop
        break
    count += 1  # Increment frame count
    if count % 3 != 0:  # Process every third frame
        continue
    frame = cv2.resize(frame, (1020, 500))  # Resize the frame for consistent processing

    # Predict objects in the frame using YOLO model
    results = model.predict(frame)
    detections = results[0].boxes.data
    px = pd.DataFrame(detections).astype("float")  # Convert the prediction results into a pandas DataFrame

    # Initialize a list to store bounding boxes for each vehicle type
    cars, buses, trucks = [], [], []

    # Iterate over the detection results and categorize them into cars, buses, or trucks
    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        if 'car' in c:
            cars.append([x1, y1, x2, y2])
        elif 'bus' in c:
            buses.append([x1, y1, x2, y2])
        elif 'truck' in c:
            trucks.append([x1, y1, x2, y2])

    # Update tracker for each vehicle type
    cars_boxes = tracker.update(cars)
    buses_boxes = tracker.update(buses)
    trucks_boxes = tracker.update(trucks)

    # Draw lines on the frame that the vehicles are supposed to cross
    cv2.line(frame, (1, cy1), (1018, cy1), (0, 255, 0), 2)
    cv2.line(frame, (3, cy2), (1016, cy2), (0, 0, 255), 2)

    # Check each car, bus, and truck
    for bbox in cars_boxes:
        cx = int((bbox[0] + bbox[2]) / 2)
        cy = int((bbox[1] + bbox[3]) / 2)
        if (cy > cy1 - offset) and (cy < cy1 + offset):
            car_count += 1

    for bbox in buses_boxes:
        cx = int((bbox[0] + bbox[2]) / 2)
        cy = int((bbox[1] + bbox[3]) / 2)
        if (cy > cy1 - offset) and (cy < cy1 + offset):
            bus_count += 1

    for bbox in trucks_boxes:
        cx = int((bbox[0] + bbox[2]) / 2)
        cy = int((bbox[1] + bbox[3]) / 2)
        if (cy > cy1 - offset) and (cy < cy1 + offset):
            truck_count += 1

    # Draw and annotate each vehicle
    for bbox in cars_boxes + buses_boxes + trucks_boxes:
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 255), 2)
        cvzone.putTextRect(frame, f'{bbox[4]}', (bbox[0], bbox[1]), 1, 1)

    # Use matplotlib to display the frame in Colab
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for correct display
    plt.axis('off')  # Hide the axes
    plt.show()

    # Break the loop if 'Esc' key is pressed (this doesn't work in Colab, but can be used in local environments)
    # if cv2.waitKey(1) & 0xFF == 27:
    #     break

# Print the total count for each vehicle type
print(f'Total car count: {car_count}')
print(f'Total bus count: {bus_count}')
print(f'Total truck count: {truck_count}')

# Release the video capture
cap.release()