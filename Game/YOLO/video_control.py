import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import threading

class player_tracker(threading.Thread):

    def __init__(self):
        self.net = cv2.dnn.readNet("Game/YOLO/Yolo_reqs/yolov3-tiny.weights", "Game/YOLO/Yolo_reqs/yolov3-tiny.cfg")
        self.classes = []
        with open("Game/YOLO/Yolo_reqs/coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        threading.Thread.__init__(self)
        self.cap = cv2.VideoCapture(0)
        self.x_val = 0
        self.y_val = 0
        self.stopped = False

    def video_tracking(self):
        frame_id = 0
        font = cv2.FONT_HERSHEY_PLAIN
        _, frame = self.cap.read()
        frame_id += 1
        self.height, self.width, channels = frame.shape
        
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        class_ids = []
        self.confidences = []
        boxes = []
        self.y_coords = []
        self.x_coords = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    center_x = int(detection[0]*self.width)
                    center_y = int(detection[1]*self.height)
                    w = int(detection[2]*self.width)
                    h = int(detection[3]*self.height)

                    #position from 0 - 100
                    y_pos = round((h-self.height*3/4)*2/self.height *100)
                    x_pos = round((center_x - self.width / 2)/self.width *100)

                    x = int(center_x - w/2)
                    y = int(center_y - h/2)

                    boxes.append([x, y, w, h])
                    self.confidences.append(float(confidence))
                    class_ids.append(class_id)
                    self.y_coords.append(y_pos)
                    self.x_coords.append(x_pos)
        try:
            index = self.confidences.index(max(self.confidences))
            self.x_val = -self.x_coords[index]
            self.y_val = -self.y_coords[index] -25
        except:
            pass

    def display_location(self):
        base = np.zeros((100, 100))
        try:
            index = self.confidences.index(max(self.confidences))
            x_val = -self.x_coords[index]+50
            y_val = -self.y_coords[index]+50
            # print()
            cv2.rectangle(base, (x_val-1,y_val-1),(x_val+1,y_val+1),(255,255,255),thickness=-5)
        except:
            pass
        resized = cv2.resize(base,(500,500))
        cv2.imshow("position", resized)
            
    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            self.video_tracking()
            self.display_location()
            # print(self.x_val,self.y_val)
            key = cv2.waitKey(1)
            if key ==27:
                break
        self.cap.release()
        cv2.destroyAllWindows()
        

if __name__ == "__main__":
    yolo_obj = player_tracker()
    yolo_obj.start()

"""
To do:
while loop for the video portion in "run" of threading.thread
create 

"""