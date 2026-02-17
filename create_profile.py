import cv2
import csv
import numpy as np
import os
from datetime import datetime

class GhostAuthProfile:
    def __init__(self, username):
        self.username = username
        self.typing_pattern = []
        self.face_encoding = None
        self.create_folder()
    
    def create_folder(self):
        if not os.path.exists(f"users/{self.username}"):
            os.makedirs(f"users/{self.username}")
    
    def add_typing_data(self, csv_file):
        """Extract typing features from CSV"""
        flight_times = []
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['event'] == 'PRESS' and row['flight_time']:
                    ft = float(row['flight_time'])
                    if ft > 0:
                        flight_times.append(ft)
        
        # Calculate typing fingerprint
        self.typing_pattern = {
            'avg_flight': np.mean(flight_times),
            'std_flight': np.std(flight_times),
            'min_flight': np.min(flight_times),
            'max_flight': np.max(flight_times),
            'typing_speed': len(flight_times) / sum(flight_times) * 60
        }
        print(f"✅ Typing profile created for {self.username}")
    
    def add_face_data(self, image_path):
        """Simple face detection"""
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_roi = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face_roi, (100, 100))
            self.face_encoding = face_resized.flatten()
            print(f"✅ Face profile created for {self.username}")
        else:
            print("❌ No face detected in image")
    
    def save_profile(self):
        """Save profile to file"""
        profile_data = {
            'username': self.username,
            'typing_pattern': self.typing_pattern,
            'created': str(datetime.now())
        }
        
        # Save typing profile
        with open(f"users/{self.username}/profile.txt", 'w') as f:
            f.write(str(profile_data))
        
        # Save face encoding if exists
        if self.face_encoding is not None:
            np.save(f"users/{self.username}/face.npy", self.face_encoding)
        
        print(f"💾 Profile saved for {self.username}")

# ===== RUN THIS =====
# Replace 'your_name' with your actual name
you = GhostAuthProfile("your_name")
you.add_typing_data("typing_data.csv")  # Your typing file
you.add_face_data("face_1771309583.1156054.jpg")  # Replace with your actual face photo filename
you.save_profile()
print("\n✅ Profile created! Check the 'users/your_name' folder")