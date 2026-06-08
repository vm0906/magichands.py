import cv2
import mediapipe as mp
import random
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Initialize the MediaPipe Tasks Hand Landmarker
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

# --- AUTOMATIC CAMERA SELECTOR ---
# Index 0, 1, or 2 la ethu active ah iruko athai automatic ah eduthukum
cap = None
for index in [0, 1, 2]:
    cap = cv2.VideoCapture(index)
    if cap.isOpened():
        print(f"=== SUCCESS: Camera connected on Port Index {index} ===")
        break
    cap.release()

if not cap or not cap.isOpened():
    print("\n[CRITICAL ERROR] Computer la camera ve track panna mudiyala!")
    print("Vera apps (Meet/Zoom/Teams) camera va use pannutha nu check panni completely close pannunga.\n")
    exit()

print("=== WITCH FIRE CODE INITIATED ===")
print("Press 'q' inside the camera view window to CLOSE.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        # Camera minor glitch aana loop ah cut pannama re-try pannum
        continue

    # Mirror effect
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    # Process frames using the MediaPipe structural image pipeline
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    
    # Detect hand landmarks
    detection_result = detector.detect(mp_image)
    all_hand_points = []

    if detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:
            for landmark in hand_landmarks:
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                all_hand_points.append((cx, cy))

        # Green Flame Magic Aura Effect Rendering Loop
        for (hx, hy) in all_hand_points:
            # Main tracking nodes
            cv2.circle(frame, (hx, hy), 4, (0, 255, 0), -1)
            
            # Upward Rising Witches Fire particles
            for _ in range(2): 
                fire_x = hx + random.randint(-20, 20)
                fire_y = hy - random.randint(12, 65)  # Subtract moves dots UP
                fire_radius = random.randint(2, 5)
                cv2.circle(frame, (fire_x, fire_y), fire_radius, (0, 255, 0), -1)

    cv2.imshow('Witch Green Fire Hands', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("=== PROGRAM CLOSED Safely ===")