import cv2 as cv

def read_video(video_url):
    cap = cv.VideoCapture(video_url)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    return frames

def save_video(video_frame, output_video_url):
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter(output_video_url, fourcc, 24, (video_frame[0].shape[1], video_frame[0].shape[0]))
    for f in video_frame:
        out.write(f)
    out.release()

        
