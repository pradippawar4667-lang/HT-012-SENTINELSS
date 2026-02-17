import cv2
import time

# Open laptop camera
cam = cv2.VideoCapture(0)

print("Camera opened! Press SPACE to capture, ESC to exit")

while True:
    ret, frame = cam.read()
    cv2.imshow('Ghost-Auth Camera', frame)
    
    key = cv2.waitKey(1)
    if key == 32:  # SPACE key
        # Save image with timestamp
        filename = f"face_{time.time()}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")
    elif key == 27:  # ESC key
        break

cam.release()
cv2.destroyAllWindows()