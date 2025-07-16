from ultralytics import YOLO
import supervision as sv
import pickle
import os

class Tracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()
    
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
        