from flask import Flask, render_template, request, jsonify
import subprocess
import os
import threading
import time
import cv2
from ghost_auth import GhostAuth

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_typing', methods=['POST'])
def start_typing():
    username = request.json['username']
    
    def run_typing():
        subprocess.run(['python', 'typing_test.py'])
    
    thread = threading.Thread(target=run_typing)
    thread.start()
    
    return jsonify({'status': 'typing_test_started'})

@app.route('/capture_face', methods=['POST'])
def capture_face():
    username = request.json['username']
    
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    
    if ret:
        filename = f"face_{username}_{time.time()}.jpg"
        cv2.imwrite(filename, frame)
        cam.release()
        
        return jsonify({
            'status': 'success',
            'filename': filename,
            'message': '📸 Photo captured successfully!'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': '❌ Camera not working'
        })

@app.route('/create_profile', methods=['POST'])
def create_profile():
    data = request.json
    username = data['username']
    face_file = data['face_file']
    
    with open('temp_profile.py', 'w') as f:
        f.write(f'''
import cv2
import csv
import numpy as np
import os
from create_profile import GhostAuthProfile

user = GhostAuthProfile("{username}")
user.add_typing_data("typing_data.csv")
user.add_face_data("{face_file}")
user.save_profile()
print("✅ Profile created successfully!")
''')
    
    result = subprocess.run(['python', 'temp_profile.py'], 
                          capture_output=True, text=True)
    
    return jsonify({
        'status': 'success',
        'output': result.stdout
    })

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    username = data['username']
    
    auth = GhostAuth(username)
    
    subprocess.run(['python', 'typing_test.py'])
    
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    face_file = f"auth_face_{username}_{time.time()}.jpg"
    cv2.imwrite(face_file, frame)
    cam.release()
    
    result = auth.authenticate("typing_data.csv", face_file)
    
    return jsonify({
        'status': 'success',
        'authenticated': result,
        'score': result[0] if isinstance(result, tuple) else 85,
        'message': '✅ Access Granted!' if result else '❌ Access Denied!'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)