import cv2 as cv
from ultralytics import YOLO
from utils import read_video, save_video
from Tracker import Tracker

def main():

    model = YOLO("Football_analysis_system\Model\\best.pt")
    video_frames = read_video("Football_analysis_system\Videos\\2_cut.mp4")
    
    tracker_obj = Tracker("Football_analysis_system\Model\\best.pt")
    tracks = tracker_obj.get_tracks(video_frames,
                                    read_from_stub=True,
                                    stub_path="Football_analysis_system\Stubs\\track_stub.pkl")

    # save_video(video_frames, "Football_analysis_system\Output\output3.avi")

if __name__ == "__main__":
    main()
