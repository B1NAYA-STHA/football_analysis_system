from ultralytics import YOLO
import cv2 as cv

cap = cv.VideoCapture("Football_analysis_system\Videos\\2_cut.mp4")
model = YOLO("yolov8n.pt")

#Testing for photos
# result = model("Football_analysis_system\Photos\\3.jpg", show=True)
# result[0].show()

# result = model.predict("Football_analysis_system\Videos\\2_cut.mp4", save=True)
# print(result[0])

while True:
    ret, img = cap.read()
    frame = cv.resize(img, (1240, 720))
    result = model(frame, stream=True)

    for r in result:
        frame = r.plot()

    cv.imshow("Football", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release
cv.destroyAllWindows
