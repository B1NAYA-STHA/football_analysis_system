import cv2 as cv
from ultralytics import YOLO
from utils import read_video, save_video
from Tracker import Tracker

def main():

    model = YOLO("Football_analysis_system\Model\\best.pt")
<<<<<<< HEAD
    video_frames = read_video("Football_analysis_system\Videos\\1.mp4")
=======
    video_frames = read_video("Football_analysis_system\Videos\\2_cut.mp4")
>>>>>>> dea57d5257a8b6dd270d2d2c82ef7fb983a6692f
    
    tracker_obj = Tracker("Football_analysis_system\Model\\best.pt")
    tracks = tracker_obj.get_tracks(video_frames,
                                    read_from_stub=True,
                                    stub_path="Football_analysis_system\Stubs\\track_stub.pkl")

<<<<<<< HEAD
    output_video_frames = tracker_obj.draw_annotation(video_frames, tracks)
    #save video
    save_video(output_video_frames, "Football_analysis_system\Output\output2.avi")
=======
    # save_video(video_frames, "Football_analysis_system\Output\output3.avi")
>>>>>>> dea57d5257a8b6dd270d2d2c82ef7fb983a6692f

if __name__ == "__main__":
    main()
