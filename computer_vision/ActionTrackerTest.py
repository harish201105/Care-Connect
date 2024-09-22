import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.2, min_tracking_confidence=0.2)

cap = cv2.VideoCapture(0)  # Use 0 for default webcam, or provide the path to a video file

main_pose = None  # Variable to store the main pose

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        # Assuming you want to track the first detected pose
        main_pose = results.pose_landmarks[0]

        # Process main_pose
        # You can access landmarks like main_pose.landmark[0], main_pose.landmark[1], etc.

    # Draw landmarks for the main pose (if it exists)
    if main_pose:
        mp.solutions.drawing_utils.draw_landmarks(frame, main_pose, mp_pose.POSE_CONNECTIONS)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
