import json
import time
import numpy as np  # Numpy for advanced math
from flask import Flask, render_template_string, request, jsonify

# --- CONFIGURATION ---
app = Flask(__name__)
# In a real laptop, this would be the user's actual password
TARGET_PHRASE = "ghost auth is the future"

# --- HTML/CSS/JS UI (HACKER LAPTOP LOGIN) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GHOST-OS | ULTRA SECURE</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@500;700;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #050505;
            --neon-blue: #00f3ff;
            --neon-red: #ff2a6d;
            --neon-green: #05d5fa;
            --glass-border: 1px solid rgba(0, 243, 255, 0.2);
        }
        
        * { box-sizing: border-box; }

        body {
            margin: 0;
            height: 100vh;
            background-color: var(--bg-dark);
            color: white;
            font-family: 'Orbitron', sans-serif;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* --- SCI-FI BACKGROUND --- */
        .bg-grid {
            position: absolute;
            top: 0; left: 0; width: 200%; height: 200%;
            background-image: 
                linear-gradient(rgba(0, 243, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px);
            background-size: 40px 40px;
            transform: perspective(500px) rotateX(60deg) translateY(-100px) translateZ(-200px);
            animation: gridMove 20s linear infinite;
            z-index: -2;
        }
        @keyframes gridMove { 0% { transform: perspective(500px) rotateX(60deg) translateY(0); } 100% { transform: perspective(500px) rotateX(60deg) translateY(40px); } }

        /* Dark Vignette */
        body::after {
            content: ''; position: absolute; inset: 0;
            background: radial-gradient(circle, transparent 40%, #000 90%);
            z-index: -1;
        }

        /* --- LOGIN PANEL --- */
        #login-screen {
            position: relative;
            width: 450px;
            padding: 40px;
            background: rgba(10, 15, 20, 0.7);
            border: var(--glass-border);
            backdrop-filter: blur(10px);
            box-shadow: 0 0 50px rgba(0, 243, 255, 0.1);
            text-align: center;
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            align-items: center;
            animation: slideUp 0.8s ease-out;
        }
        
        @keyframes slideUp { from { opacity: 0; transform: translateY(50px); } to { opacity: 1; transform: translateY(0); } }

        /* Holographic Border Effect */
        #login-screen::before {
            content: ''; position: absolute; inset: -2px;
            background: conic-gradient(transparent, var(--neon-blue), transparent 30%);
            z-index: -1; border-radius: 17px;
            animation: rotateBorder 4s linear infinite;
        }
        #login-screen::after {
            content: ''; position: absolute; inset: 2px;
            background: rgba(10, 15, 20, 0.9);
            border-radius: 13px; z-index: -1;
        }
        @keyframes rotateBorder { 100% { transform: rotate(360deg); } }

        /* Avatar / Camera */
        .avatar-box {
            position: relative;
            width: 140px; height: 140px;
            margin-bottom: 20px;
        }
        .avatar-img {
            width: 100%; height: 100%;
            border-radius: 50%;
            border: 2px solid var(--neon-blue);
            background: url('https://api.dicebear.com/7.x/bottts/svg?seed=Ghost') center/cover;
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.3);
        }
        .cam-feed {
            position: absolute; top: 0; left: 0;
            width: 100%; height: 100%;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid var(--neon-red);
            display: none; /* Hidden until activated */
        }
        .face-scanner {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            border-radius: 50%;
            border-top: 2px solid var(--neon-blue);
            animation: spinScan 2s linear infinite;
            display: none;
        }
        @keyframes spinScan { 100% { transform: rotate(360deg); } }

        h1 { margin: 0 0 5px 0; font-size: 1.5rem; letter-spacing: 2px; text-shadow: 0 0 10px var(--neon-blue); }
        p { margin: 0 0 30px 0; font-size: 0.8rem; color: #aaa; font-family: 'JetBrains Mono'; }

        /* Input Field */
        .input-group { position: relative; width: 100%; margin-bottom: 20px; }
        
        input {
            width: 100%;
            padding: 15px;
            background: rgba(0,0,0,0.5);
            border: 1px solid #333;
            color: var(--neon-blue);
            text-align: center;
            font-family: 'JetBrains Mono';
            font-size: 1.1rem;
            outline: none;
            border-radius: 5px;
            transition: 0.3s;
        }
        input:focus { border-color: var(--neon-blue); box-shadow: 0 0 15px rgba(0, 243, 255, 0.2); }
        
        .scan-bar {
            height: 2px; width: 0%;
            background: var(--neon-blue);
            margin: 0 auto;
            transition: width 0.1s;
            box-shadow: 0 0 10px var(--neon-blue);
        }

        .status-msg {
            font-size: 0.75rem; color: #666; margin-top: 10px; font-family: 'JetBrains Mono';
            height: 20px;
        }

        /* Controls */
        .controls {
            display: flex; gap: 10px; margin-top: 20px;
        }
        .btn {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.2);
            color: #ccc; padding: 8px 12px; font-size: 0.7rem; cursor: pointer;
            transition: 0.3s; font-family: 'Orbitron';
        }
        .btn:hover { background: var(--neon-blue); color: #000; box-shadow: 0 0 15px var(--neon-blue); }
        .btn.active { border-color: var(--neon-blue); color: var(--neon-blue); }

        /* --- DESKTOP VAULT (HIDDEN) --- */
        #desktop-screen {
            display: none;
            width: 100%; height: 100%;
            background: radial-gradient(circle at center, #1a2a3a 0%, #000 100%);
            flex-direction: column;
            align-items: center;
            justify-content: center;
            animation: fadeIn 1.5s ease;
        }
        
        @keyframes fadeIn { from { opacity: 0; transform: scale(1.1); } to { opacity: 1; transform: scale(1); } }

        .vault-title {
            font-size: 3rem; color: var(--neon-green); text-shadow: 0 0 30px var(--neon-green);
            margin-bottom: 10px;
        }
        
        .folder-grid {
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; margin-top: 50px;
        }
        
        .folder {
            width: 160px; height: 140px;
            border: 2px solid var(--neon-green);
            background: rgba(0, 255, 157, 0.05);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            cursor: pointer; transition: 0.3s;
            position: relative;
        }
        .folder::before {
            content: ''; position: absolute; top: -5px; left: -5px; width: 10px; height: 10px;
            border-top: 2px solid var(--neon-green); border-left: 2px solid var(--neon-green);
        }
        .folder::after {
            content: ''; position: absolute; bottom: -5px; right: -5px; width: 10px; height: 10px;
            border-bottom: 2px solid var(--neon-green); border-right: 2px solid var(--neon-green);
        }
        
        .folder:hover {
            transform: translateY(-10px);
            box-shadow: 0 10px 40px rgba(0, 255, 157, 0.2);
            background: rgba(0, 255, 157, 0.1);
        }
        
        .folder-icon { font-size: 3rem; margin-bottom: 10px; }
        .folder-name { font-size: 0.8rem; color: var(--neon-green); letter-spacing: 1px; }

        .logout-btn {
            position: absolute; top: 30px; right: 30px;
            background: transparent; border: 1px solid var(--neon-red); color: var(--neon-red);
            padding: 10px 20px; cursor: pointer; transition: 0.3s;
        }
        .logout-btn:hover { background: var(--neon-red); color: #000; box-shadow: 0 0 20px var(--neon-red); }

        .shake { animation: shake 0.4s ease-in-out; border-color: var(--neon-red) !important; }
        @keyframes shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-10px)} 75%{transform:translateX(10px)} }

    </style>
</head>
<body>

    <div class="bg-grid"></div>

    <!-- LOGIN SCREEN -->
    <div id="login-screen">
        <div class="avatar-box">
            <div class="avatar-img" id="avatar-img"></div>
            <video id="cam-feed" class="cam-feed" autoplay muted playsinline></video>
            <div class="face-scanner" id="face-scanner"></div>
        </div>

        <h1>GHOST-OS</h1>
        <p>SECURE TERMINAL ACCESS</p>

        <div class="input-group">
            <input type="text" id="password-input" placeholder="ENTER PASSPHRASE" autocomplete="off">
            <div class="scan-bar" id="scan-bar"></div>
        </div>

        <div class="status-msg" id="status-msg">SYSTEM LOCKED. AWAITING INPUT.</div>

        <div class="controls">
            <div class="btn" id="btn-cam" onclick="toggleCamera()">📸 FACE ID</div>
            <div class="btn active" id="btn-train" onclick="setMode('train')">TRAIN</div>
            <div class="btn" id="btn-verify" onclick="setMode('verify')">LOGIN</div>
            <div class="btn" style="color:var(--neon-red); border-color:var(--neon-red);" onclick="simulateBot()">🤖 HACK</div>
        </div>
    </div>

    <!-- SECRET DESKTOP (UNLOCKED) -->
    <div id="desktop-screen">
        <button class="logout-btn" onclick="location.reload()">🔒 LOCK SYSTEM</button>
        
        <div class="vault-title">ACCESS GRANTED</div>
        <div style="font-family: 'JetBrains Mono'; color: #aaa;">WELCOME COMMANDER. DECRYPTING FILES...</div>

        <div class="folder-grid">
            <div class="folder">
                <div class="folder-icon">☢️</div>
                <div class="folder-name">LAUNCH_CODES</div>
            </div>
            <div class="folder">
                <div class="folder-icon">🛸</div>
                <div class="folder-name">AREA_51_LOGS</div>
            </div>
            <div class="folder">
                <div class="folder-icon">₿</div>
                <div class="folder-name">SWISS_BANK_KEYS</div>
            </div>
            <div class="folder">
                <div class="folder-icon">🕵️</div>
                <div class="folder-name">AGENT_ROSTER</div>
            </div>
            <div class="folder">
                <div class="folder-icon">📡</div>
                <div class="folder-name">SAT_CONTROL</div>
            </div>
            <div class="folder">
                <div class="folder-icon">💾</div>
                <div class="folder-name">BLACK_BOX</div>
            </div>
        </div>
    </div>

    <script>
        let mode = 'train';
        let flightTimes = [];
        let holdTimes = [];
        let keyDownMap = {};
        let lastKeyUpTime = 0;
        let phrase = "{{ phrase }}";
        let isModelTrained = false;
        let isCameraActive = false;

        const pwdInput = document.getElementById('password-input');
        const scanBar = document.getElementById('scan-bar');
        const statusMsg = document.getElementById('status-msg');
        const loginScreen = document.getElementById('login-screen');
        const desktopScreen = document.getElementById('desktop-screen');

        pwdInput.placeholder = `TYPE: "${phrase}"`;

        function setMode(m) {
            mode = m;
            resetUI();
            document.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
            
            if(m === 'train') {
                document.getElementById('btn-train').classList.add('active');
                statusMsg.innerText = "TRAINING MODE: TYPE NATURALLY TO ENROLL.";
                statusMsg.style.color = "var(--neon-blue)";
                pwdInput.placeholder = `ENROLL: "${phrase}"`;
            } else {
                if(!isModelTrained) { alert("⚠️ SYSTEM ERROR: MODEL NOT TRAINED."); setMode('train'); return; }
                document.getElementById('btn-verify').classList.add('active');
                statusMsg.innerText = "LOGIN MODE: AUTHENTICATE YOURSELF.";
                statusMsg.style.color = "#fff";
                pwdInput.placeholder = "ENTER PASSPHRASE";
            }
        }

        function toggleCamera() {
            if(!isCameraActive) {
                navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    const vid = document.getElementById('cam-feed');
                    vid.srcObject = stream;
                    vid.style.display = 'block';
                    document.getElementById('face-scanner').style.display = 'block';
                    isCameraActive = true;
                    document.getElementById('btn-cam').classList.add('active');
                    statusMsg.innerText = "OPTICAL SENSORS ACTIVE.";
                })
                .catch(e => alert("CAMERA ACCESS DENIED"));
            }
        }

        function resetUI() {
            flightTimes = [];
            holdTimes = [];
            keyDownMap = {};
            lastKeyUpTime = 0;
            pwdInput.classList.remove('shake');
            scanBar.style.width = '0%';
            pwdInput.value = "";
            pwdInput.disabled = false;
            pwdInput.focus();
        }

        // --- TYPING LOGIC ---
        pwdInput.addEventListener('keydown', e => {
            if(e.key === 'Enter') return;
            if(!keyDownMap[e.code]) keyDownMap[e.code] = Date.now();
        });

        pwdInput.addEventListener('keyup', e => {
            let now = Date.now();
            let progress = (pwdInput.value.length / phrase.length) * 100;
            scanBar.style.width = `${progress}%`;

            if(keyDownMap[e.code]) {
                holdTimes.push(now - keyDownMap[e.code]);
                delete keyDownMap[e.code];
            }
            if(lastKeyUpTime !== 0) {
                flightTimes.push(now - lastKeyUpTime);
            }
            lastKeyUpTime = now;

            if(pwdInput.value.length >= phrase.length) {
                pwdInput.disabled = true;
                statusMsg.innerText = "PROCESSING BIOMETRIC VECTORS...";
                setTimeout(processData, 600);
            }
        });

        async function processData() {
            if(pwdInput.value !== phrase) {
                loginFail("INVALID PASSPHRASE");
                return;
            }

            const res = await fetch('/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    mode: mode === 'bot' ? 'verify' : mode,
                    flight_times: flightTimes,
                    hold_times: holdTimes,
                    is_bot_simulation: mode === 'bot',
                    camera_active: isCameraActive
                })
            });
            const data = await res.json();
            
            if(data.status === 'trained') {
                isModelTrained = true;
                alert("✅ ENROLLMENT COMPLETE.\\nSYSTEM LOCKED. PROCEED TO LOGIN.");
                setMode('verify');
            } else if (data.status === 'verified') {
                loginSuccess(data.score);
            } else {
                loginFail(data.reason);
            }
        }

        function loginSuccess(score) {
            statusMsg.innerText = `IDENTITY CONFIRMED. TRUST SCORE: ${score}%`;
            statusMsg.style.color = "var(--neon-green)";
            pwdInput.style.borderColor = "var(--neon-green)";
            
            setTimeout(() => {
                loginScreen.style.display = 'none';
                desktopScreen.style.display = 'flex';
            }, 1000);
        }

        function loginFail(reason) {
            pwdInput.classList.add('shake');
            statusMsg.innerText = `⛔ ACCESS DENIED: ${reason}`;
            statusMsg.style.color = "var(--neon-red)";
            setTimeout(resetUI, 2000);
        }

        function simulateBot() {
            if(!isModelTrained) { alert("TRAIN FIRST!"); return; }
            setMode('verify');
            mode = 'bot';
            
            statusMsg.innerText = "⚠️ DETECTED: BOT INJECTION ATTACK...";
            statusMsg.style.color = "var(--neon-red)";
            pwdInput.disabled = true;

            let chars = phrase.split('');
            let i = 0;
            let intv = setInterval(() => {
                if(i < chars.length) {
                    pwdInput.value += chars[i];
                    flightTimes.push(50); 
                    holdTimes.push(80);
                    i++;
                } else {
                    clearInterval(intv);
                    processData();
                }
            }, 50);
        }
    </script>
</body>
</html>
"""

# --- PYTHON BACKEND LOGIC (Advanced) ---
user_profile = {
    "trained": False,
    "flight_avg": [],
    "flight_std": 0,
    "hold_avg": [],
    "hold_std": 0
}

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, phrase=TARGET_PHRASE)

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