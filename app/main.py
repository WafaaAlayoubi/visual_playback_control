import cv2
from ultralytics import YOLO
import pyautogui
import time
import numpy as np

model = YOLO("./weights/best.pt")

cap = cv2.VideoCapture(0)

prev_state = None
last_click_time = 0
click_delay = 1.5  # seconds delay to avoid too many clicks

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, imgsz=640, verbose=False)[0]

    headphone_detected = None
    if len(results.boxes) > 0:
        # Find highest confidence box
        confidences = [box.conf.item() for box in results.boxes]
        max_idx = np.argmax(confidences)

        box = results.boxes[max_idx]
        cls_id = int(box.cls)
        label = results.names[cls_id]

        if label == "headphones_on":
            headphone_detected = True
        elif label == "headphones_off":
            headphone_detected = False

    if headphone_detected is True:
        state_text = "Headphones: ON"
        color = (0, 255, 0)       # Green
    elif headphone_detected is False:
        state_text = "Headphones: OFF"
        color = (0, 0, 255)       # Red
    else:
        state_text = "Headphones: UNKNOWN"
        color = (0, 255, 255)     # Yellow

    annotated_frame = results.plot()
    cv2.putText(annotated_frame, state_text, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

    cv2.imshow("Headphone Detection", annotated_frame)
    cv2.moveWindow("Headphone Detection", 0, 100)

    current_time = time.time()
    if headphone_detected != prev_state and current_time - last_click_time > click_delay:
        print(state_text)
        pyautogui.click()
        last_click_time = current_time
        prev_state = headphone_detected

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
