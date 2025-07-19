import cv2

# Open the default laptop camera (0 is the default camera index)
cap = cv2.VideoCapture(0)

# Set resolution (optional)
cap.set(3, 640)  # width
cap.set(4, 480)  # height

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can use 'MJPG' or 'XVID'
out = cv2.VideoWriter('../dataset/raw_videos/output2.avi', fourcc, 20.0, (640, 480))

print("Recording... Press 'q' to stop.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Write the frame to the output file
    out.write(frame)

    # Show the frame live
    cv2.imshow('Recording', frame)

    # Press 'q' key to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Stopping recording...")
        break

# Release everything
cap.release()
out.release()
cv2.destroyAllWindows()
