import cv2 as cv
from ultralytics import YOLO
from utils import read_video, save_video

def main():

    model = YOLO("Football_analysis_system\Model\\best.pt")
    video_frames = read_video("Football_analysis_system\Videos\\2_cut.mp4")
    for f in video_frames:
        frame = model(f, stream=True)
        

    save_video(video_frames, "Football_analysis_system\Output\output2.avi")

if __name__ == "__main__":
    main()
