import cv2
import time
import os

# INTEGRATION OF THE MODULES

from eye_movement import process_eye_movement
from head_pose import process_head_pose
from mobile_detection import process_mobile_detection

# Webcam 
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

calibrated_angles = None
start_time = time.time()

# Timers
head_misalignment_start_time = None
eye_misalignment_start_time = None
mobile_detection_start_time = None

# Default state
head_direction = "Looking at Screen"

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Eye tracking
        frame, gaze_direction = process_eye_movement(frame)
        cv2.putText(frame, f"Gaze Direction: {gaze_direction}", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Head Pose (with calibration for first 5 sec)
        if time.time() - start_time <= 5:
            cv2.putText(frame, "Calibrating... Keep your head straight", (50, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            if calibrated_angles is None:
                _, calibrated_angles = process_head_pose(frame, None)
        else:
            frame, head_direction = process_head_pose(frame, calibrated_angles)
            cv2.putText(frame, f"Head Direction: {head_direction}", (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Mobile detection
        frame, mobile_detected = process_mobile_detection(frame)
        cv2.putText(frame, f"Mobile Detected: {mobile_detected}", (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        timestamp = int(time.time())

        # Log head misalignment
        if head_direction != "Looking at Screen":
            if head_misalignment_start_time is None:
                head_misalignment_start_time = time.time()
            elif time.time() - head_misalignment_start_time >= 3:
                filename = os.path.join(log_dir, f"head_{head_direction}_{timestamp}.png")
                cv2.imwrite(filename, frame)
                print(f"[LOG] Saved: {filename}")
                head_misalignment_start_time = None
        else:
            head_misalignment_start_time = None

        # Log eye misalignment
        if gaze_direction != "Looking at Screen":
            if eye_misalignment_start_time is None:
                eye_misalignment_start_time = time.time()
            elif time.time() - eye_misalignment_start_time >= 3:
                filename = os.path.join(log_dir, f"eye_{gaze_direction}_{timestamp}.png")
                cv2.imwrite(filename, frame)
                print(f"[LOG] Saved: {filename}")
                eye_misalignment_start_time = None
        else:
            eye_misalignment_start_time = None

        # Log mobile detection
        if mobile_detected:
            if mobile_detection_start_time is None:
                mobile_detection_start_time = time.time()
            elif time.time() - mobile_detection_start_time >= 3:
                filename = os.path.join(log_dir, f"mobile_detected_{timestamp}.png")
                cv2.imwrite(filename, frame)
                print(f"[LOG] Saved: {filename}")
                mobile_detection_start_time = None
        else:
            mobile_detection_start_time = None

        # Show frame
        cv2.imshow("Malpractice Detection System", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            print("Exiting...")
            break

finally:
    #Release the camera and destroy windows
    cap.release()
    cv2.destroyAllWindows()
    print("Camera released and all windows closed.")
