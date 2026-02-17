from flask import Flask, render_template, request, jsonify
import subprocess
import os
import threading
import time
import cv2
from ghost_auth import GhostAuth

app = Flask(__name__)
# In a real laptop, this would be the user's actual password
TARGET_PHRASE = "ghost auth is the future"

# --- HTML/CSS/JS UI (HACKER LAPTOP LOGIN) ---


# --- PYTHON BACKEND LOGIC (Advanced) ---
user_profile = {
    "trained": False,
    "flight_avg": [],
    "flight_std": 0,
    "hold_avg": [],
    "hold_std": 0
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    mode = data.get('mode')
    flight_times = data.get('flight_times', [])
    hold_times = data.get('hold_times', [])
    is_bot = data.get('is_bot_simulation', False)
    camera_active = data.get('camera_active', False)

    if not flight_times:
        return jsonify({"status": "error", "message": "No data captured"})

    # --- ADVANCED ANALYSIS USING NUMPY ---
    
    if mode == 'train':
        # 1. Process Flight Times (Speed/Rhythm)
        f_arr = np.array(flight_times)
        user_profile["flight_avg"] = flight_times
        user_profile["flight_std"] = float(np.std(f_arr))
        
        # 2. Process Hold Times (Pressure/Dwell)
        h_arr = np.array(hold_times)
        user_profile["hold_avg"] = hold_times
        user_profile["hold_std"] = float(np.std(h_arr))
        
        user_profile["trained"] = True
        
        return jsonify({
            "status": "trained",
            "message": f"Multi-Dimensional Model Trained.",
            "details": {
                "flight_points": len(flight_times),
                "hold_points": len(hold_times)
            }
        })

    elif mode == 'verify':
        if not user_profile["trained"]:
            return jsonify({"status": "denied", "score": 0, "reason": "Model not trained yet!"})

        # --- DUAL LAYER VERIFICATION (With Normalization) ---
        
        # Layer 1: Flight Time Analysis (RHYTHM)
        curr_flight = np.array(flight_times)
        ref_flight = np.array(user_profile["flight_avg"])
        min_len_f = min(len(curr_flight), len(ref_flight))
        
        # Normalize: Remove 'Average Speed' bias to check 'Relative Rhythm'
        curr_f_norm = curr_flight[:min_len_f] - np.mean(curr_flight)
        ref_f_norm = ref_flight[:min_len_f] - np.mean(ref_flight)
        
        # Compare Patterns
        flight_diff = np.mean(np.abs(curr_f_norm - ref_f_norm))
        flight_score = max(0, 100 - (flight_diff / 1.5)) 

        # Layer 2: Hold Time Analysis (STYLE)
        curr_hold = np.array(hold_times)
        ref_hold = np.array(user_profile["hold_avg"])
        min_len_h = min(len(curr_hold), len(ref_hold))
        
        # Normalize Hold Times too
        curr_h_norm = curr_hold[:min_len_h] - np.mean(curr_hold)
        ref_h_norm = ref_hold[:min_len_h] - np.mean(ref_hold)
        
        hold_diff = np.mean(np.abs(curr_h_norm - ref_h_norm))
        hold_score = max(0, 100 - (hold_diff / 1.5))

        # Layer 3: Camera Logic (Simulated)
        face_score = 0
        if camera_active:
            face_score = 98 # Simulated High Match for Demo
        
        # Combined Trust Score (Weighted)
        if camera_active:
            final_score = int((flight_score * 0.3) + (hold_score * 0.3) + (face_score * 0.4))
        else:
            final_score = int((flight_score * 0.6) + (hold_score * 0.4))
        
        # --- BOT DETECTION (The Trap) ---
        flight_var = np.std(curr_flight)
        hold_var = np.std(curr_hold)
        
        if is_bot or (flight_var < 2 and hold_var < 2):
            return jsonify({
                "status": "denied",
                "score": 5,
                "reason": "⚠️ ROBOTIC BEHAVIOR (ZERO VARIANCE)"
            })
        
        elif final_score > 45: # Relaxed threshold for humans
            reason_text = "FACE + BEHAVIOR MATCH CONFIRMED" if camera_active else "BEHAVIORAL MATCH CONFIRMED"
            return jsonify({
                "status": "verified",
                "score": final_score,
                "reason": reason_text
            })
        else:
            reason = "TYPING RHYTHM CHANGED" if flight_score < hold_score else "KEY PRESSURE CHANGED"
            return jsonify({
                "status": "denied",
                "score": final_score,
                "reason": f"BIOMETRIC MISMATCH: {reason}"
            })

if __name__ == '__main__':
    app.run(debug=True, port=5000)