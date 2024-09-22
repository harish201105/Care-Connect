import cv2

# Open the video file
cap = cv2.VideoCapture('../assets/bg.mp4')

# Read the first frame of the video
ret, frame = cap.read()

# Save the first frame as an image file
cv2.imwrite('../assets/bg.png', frame)

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
