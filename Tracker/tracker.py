from ultralytics import YOLO
import supervision as sv
import pickle
<<<<<<< HEAD
import cv2 as cv
import os
import numpy as np
import pandas as pd
import sys
sys.path.append('../')
from utils import get_center_of_bbox, get_bbox_width
=======
import os
>>>>>>> dea57d5257a8b6dd270d2d2c82ef7fb983a6692f

class Tracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()
<<<<<<< HEAD
   
=======
    
>>>>>>> dea57d5257a8b6dd270d2d2c82ef7fb983a6692f
    def detector(self, frames):
        #detect frames in batch size of 20 at a time
        batch_size = 20
        detections = []
        for i in range(0, len(frames), batch_size):
            detection_batch = self.model.predict(frames[i:i+batch_size], conf=0.1)
            detections += detection_batch
        return detections
    
    def get_tracks(self, frames, read_from_stub = False, stub_path = None):
        #load pickle file
        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                tracks = pickle.load(f)
            return tracks

        detections = self.detector(frames)
        tracks = {
            'player': [],
            'referee': [],
            'ball': []
        }

        for frame_num, detection in enumerate(detections):
            cls_names = detection.names
            cls_names_inv = {v:k for k,v in cls_names.items()}

            #convert to supervision detection format
            detection_supervision = sv.Detections.from_ultralytics(detection)

            #convert goalkeeper to player
            for id_num, cls_id in enumerate(detection_supervision.class_id):
                if cls_names[cls_id] == 'goalkeeper':
                    detection_supervision.class_id[id_num] = cls_names_inv['player']

            tracks_supervision = self.tracker.update_with_detections(detection_supervision)

            tracks['player'].append({})
            tracks['referee'].append({})
            tracks['ball'].append({})

            #for player and referee
            for frame_detection in tracks_supervision:
                bbox = frame_detection[0].tolist()
                cls_id = frame_detection[3]
                track_id = frame_detection[4]

                if cls_id == cls_names_inv['player']:
                    tracks['player'][frame_num][track_id] = {"bbox": bbox}

                if cls_id == cls_names_inv['referee']:
                    tracks['referee'][frame_num][track_id] = {"bbox": bbox}

            #for ball
            for frame_detection in detection_supervision:
                bbox = frame_detection[0].tolist()
                cls_id = frame_detection[3]

                if cls_id == cls_names_inv['ball']:
                    tracks['ball'][frame_num][1] = {"bbox": bbox}

        #create pickle file for future use
        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(tracks, f)
        
        return tracks
<<<<<<< HEAD
    
    def draw_ellipse(self, frame, bbox, color, track_id=None):
        y2 = int(bbox[3])
        center_x, _ = get_center_of_bbox(bbox)
        width = get_bbox_width(bbox)
        cv.ellipse(frame, 
                   center=(center_x, y2),
                   axes=(int(width), int(0.35*width)),
                   angle=0,
                   startAngle=-45,
                   endAngle=235,
                   color= color,
                   thickness=2,
                   lineType= cv.LINE_4
                   )
        
        #draw rectangle for the track id
        rectangle_width = 40
        rectangle_height=20
        x1_rect = center_x - rectangle_width//2
        x2_rect = center_x + rectangle_width//2
        y1_rect = (y2 - rectangle_height//2) +15
        y2_rect = (y2 + rectangle_height//2) +15

        if track_id is not None:
            cv.rectangle(frame,
                          (int(x1_rect),int(y1_rect) ),
                          (int(x2_rect),int(y2_rect)),
                          color,
                          cv.FILLED)
        
            x1_text = x1_rect+12
            if track_id > 99:
                x1_text -=10
            
            cv.putText(frame,
                f"{track_id}",
                (int(x1_text),int(y1_rect+15)),
                cv.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,0,0),
                2
            )
        return frame
    
    def draw_traingle(self,frame,bbox,color):
        y= int(bbox[1])
        x,_ = get_center_of_bbox(bbox)

        triangle_points = np.array([
            [x,y],
            [x-10,y-20],
            [x+10,y-20],
        ])
        cv.drawContours(frame, [triangle_points],0,color, cv.FILLED)
        cv.drawContours(frame, [triangle_points],0,(0,0,0), 2)

        return frame
    
    def draw_annotation(self, frames, tracks):
        output_video_frame = []
        for frame_num, frame in enumerate(frames):
            frame = frame.copy()

            player_dict = tracks['player'][frame_num]
            referee_dict = tracks['referee'][frame_num]
            ball_dict = tracks['ball'][frame_num]

            #draw player
            for track_id, player in player_dict.items():
                frame = self.draw_ellipse(frame, player['bbox'], (0,0,255), track_id)
            
            #draw referee
            for track_id, referee in referee_dict.items():
                 frame = self.draw_ellipse(frame, referee['bbox'], (0,255,255))
                
            #draw ball
            for track_id, ball in ball_dict.items():
                 frame = self.draw_traingle(frame, ball['bbox'], (0,255,255))

            output_video_frame.append(frame)
        
        return output_video_frame
=======
        
>>>>>>> dea57d5257a8b6dd270d2d2c82ef7fb983a6692f
