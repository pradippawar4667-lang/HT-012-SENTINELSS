import cv2
import csv
import numpy as np
import json
import os

class GhostAuth:
    def __init__(self, username):
        self.username = username
        self.load_profile()
    
    def load_profile(self):
        """प्रोफाइल लोड करा"""
        profile_path = f"users/{self.username}/profile.txt"
        with open(profile_path, 'r') as f:
            profile_str = f.read()
            # numpy चे float काढून टाका
            profile_str = profile_str.replace("np.float64(", "").replace(")", "")
            profile_str = profile_str.replace("np.float32(", "").replace(")", "")
            self.profile = eval(profile_str)
        
        # चेहऱ्याचा डेटा लोड करा
        face_path = f"users/{self.username}/face.npy"
        if os.path.exists(face_path):
            self.face_encoding = np.load(face_path)
            print("✅ चेहरा प्रोफाइल लोड झाला")
        else:
            self.face_encoding = None
            print("⚠️ चेहरा प्रोफाइल सापडला नाही")
    
    def check_typing(self, new_csv_file):
        """नवीन टायपिंग चेक करा"""
        flight_times = []
        try:
            with open(new_csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['event'] == 'PRESS' and row['flight_time']:
                        ft = float(row['flight_time'])
                        if ft > 0:
                            flight_times.append(ft)
        except:
            print("❌ टायपिंग फाइल वाचता आली नाही")
            return 0
        
        if len(flight_times) < 5:
            print("⚠️ पुरेसा टायपिंग डेटा नाही")
            return 0
        
        # आत्ताचे टायपिंग पॅटर्न काढा
        current = {
            'avg_flight': np.mean(flight_times),
            'std_flight': np.std(flight_times),
            'typing_speed': len(flight_times) / sum(flight_times) * 60
        }
        
        # प्रोफाइलशी तुलना करा
        profile = self.profile['typing_pattern']
        
        # स्कोअर काढा
        speed_diff = abs(current['typing_speed'] - profile['typing_speed'])
        rhythm_diff = abs(current['avg_flight'] - profile['avg_flight'])
        
        typing_score = 100 - (speed_diff * 2 + rhythm_diff * 200)
        typing_score = max(0, min(100, typing_score))
        
        return typing_score
    
    def check_face(self, new_image_path):
        """नवीन चेहरा चेक करा"""
        if self.face_encoding is None:
            return 0
        
        if not os.path.exists(new_image_path):
            print("❌ फोटो सापडला नाही")
            return 0
        
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        img = cv2.imread(new_image_path)
        if img is None:
            return 0
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            print("❌ फोटोमध्ये चेहरा दिसत नाही")
            return 0
        
        # चेहरा कापून घ्या
        x, y, w, h = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        face_resized = cv2.resize(face_roi, (100, 100))
        new_encoding = face_resized.flatten()
        
        # तुलना करा
        difference = np.mean(np.abs(new_encoding - self.face_encoding))
        face_score = max(0, 100 - difference / 8)
        
        return face_score
    
    def authenticate(self, typing_file, face_file=None):
        """यूजरला ओळखा"""
        typing_score = self.check_typing(typing_file)
        auth = GhostAuth("your_name")  # 'your_name' ऐवजी तुमचं नाव लिहा
        if face_file:
            face_score = self.check_face(face_file)
            total_score = (typing_score * 0.6) + (face_score * 0.4)
        else:
            face_score = 0
            total_score = typing_score
        
        print(f"\n🔐 ओळख पटवण्याचा निकाल")
        print("-" * 40)
        print(f"टायपिंग जुळणी: {typing_score:.1f}%")
        if face_file:
            print(f"चेहरा जुळणी: {face_score:.1f}%")
        print(f"एकूण विश्वास: {total_score:.1f}%")
        
        if total_score > 65:
            print("✅ परवानगी दिली - तुम्ही खरे यूजर आहात!")
            return True
        else:
            print("❌ परवानगी नाकारली - हे कोणीतरी दुसरे आहे!")
            return False

# ===== तुमची चाचणी करा =====
if __name__ == "__main__":
    print("🔍 तुमच्या डेटाची चाचणी होतेय:")
    
    # TODO: इथे तुमचं नाव लिहा (create_profile.py मध्ये वापरलं तेच)
    auth = GhostAuth("your_name")
    
    # तुमचा फोटो शोधा
    import glob
    face_files = glob.glob("face_*.jpg")
    if face_files:
        latest_face = max(face_files)  # सगळ्यात नवीन फोटो
        print(f"📸 वापरतोय फोटो: {latest_face}")
        auth.authenticate("typing_data.csv", latest_face)
    else:
        print("⚠️ फोटो सापडला नाही, फक्त टायपिंग चेक होईल")
        auth.authenticate("typing_data.csv", None)