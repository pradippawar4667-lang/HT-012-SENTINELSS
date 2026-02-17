import json
import time
import numpy as np  # Numpy for advanced math
from flask import Flask, render_template_string, request, jsonify

# --- CONFIGURATION ---
app = Flask(__name__)
# This is the password for the demo
TARGET_PHRASE = "ghost auth is the future"

# --- HTML/CSS/JS UI (GHOST-OS LOGIN) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GHOST-OS | Secure Login</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --primary: #38bdf8;
            --success: #4ade80;
            --danger: #f87171;
            --text-main: #f1f5f9;
            --text-sub: #94a3b8;
        }
        
        * { box-sizing: border-box; }

        body {
            margin: 0;
            height: 100vh;
            background: radial-gradient(circle at center, #1e293b 0%, #020617 100%);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }

        /* --- BACKGROUND MESH --- */
        .bg-mesh {
            position: absolute;
            width: 100%; height: 100%;
            background-image: 
                linear-gradient(rgba(56, 189, 248, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(56, 189, 248, 0.05) 1px, transparent 1px);
            background-size: 50px 50px;
            z-index: -1;
            animation: float 20s linear infinite;
        }
        @keyframes float { from { transform: translateY(0); } to { transform: translateY(50px); } }

        /* --- LOGIN CARD --- */
        .login-card {
            width: 400px;
            padding: 40px;
            background: var(--card-bg);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 24px;
            backdrop-filter: blur(20px);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            text-align: center;
            position: relative;
            transition: transform 0.3s;
        }

        .avatar {
            width: 96px; height: 96px;
            background: linear-gradient(135deg, var(--primary), #818cf8);
            border-radius: 50%;
            margin: 0 auto 20px;
            display: flex; align-items: center; justify-content: center;
            font-size: 32px; font-weight: bold; color: white;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
            position: relative;
        }
        
        .avatar::after {
            content: ''; position: absolute; inset: -5px;
            border-radius: 50%; border: 2px solid transparent;
            border-top-color: var(--primary);
            animation: spin 3s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        h1 { margin: 0; font-size: 1.5rem; font-weight: 600; letter-spacing: -0.5px; }
        p { color: var(--text-sub); font-size: 0.9rem; margin-top: 5px; margin-bottom: 30px; }

        /* --- INPUT AREA --- */
        .input-group { position: relative; margin-bottom: 20px; }
        
        input {
            width: 100%;
            padding: 16px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            color: white;
            font-family: 'JetBrains Mono', monospace;
            font-size: 1rem;
            text-align: center;
            outline: none;
            transition: 0.3s;
        }
        input:focus { border-color: var(--primary); box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.1); }
        input::placeholder { color: rgba(255,255,255,0.2); }

        /* Biometric Visualizer Bar */
        .bio-bar {
            height: 4px; width: 0%;
            background: var(--primary);
            border-radius: 2px;
            margin: 10px auto;
            transition: width 0.1s;
            box-shadow: 0 0 10px var(--primary);
        }

        .status-text {
            font-size: 0.8rem; color: var(--text-sub); height: 20px;
            font-family: 'JetBrains Mono';
        }

        /* --- CONTROLS --- */
        .controls {
            display: flex; gap: 10px; justify-content: center; margin-top: 30px;
        }
        .btn {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            color: var(--text-sub);
            padding: 8px 16px; border-radius: 8px;
            font-size: 0.8rem; cursor: pointer; transition: 0.2s;
        }
        .btn:hover { background: rgba(255,255,255,0.1); color: white; }
        .btn.active { background: var(--primary); color: #0f172a; border-color: var(--primary); font-weight: 600; }
        
        .btn-hack { color: var(--danger); border-color: rgba(248, 113, 113, 0.3); }
        .btn-hack:hover { background: rgba(248, 113, 113, 0.1); }

        /* --- SECURE VAULT (UNLOCKED SCREEN) --- */
        #vault-screen {
            display: none;
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: #0f172a;
            flex-direction: column; align-items: center; justify-content: center;
            z-index: 10;
            animation: fadeIn 0.5s ease;
        }
        
        .folder-grid {
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; margin-top: 40px;
        }
        .folder {
            width: 120px; height: 100px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            cursor: pointer; transition: 0.3s;
        }
        .folder:hover { background: rgba(56, 189, 248, 0.1); border-color: var(--primary); transform: translateY(-5px); }
        
        .folder-icon { font-size: 2rem; margin-bottom: 8px; }
        .folder-name { font-size: 0.75rem; color: var(--text-sub); }

        .shake { animation: shake 0.4s ease-in-out; border-color: var(--danger) !important; }
        @keyframes shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-10px)} 75%{transform:translateX(10px)} }
        @keyframes fadeIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }

    </style>
</head>
<body>

    <div class="bg-mesh"></div>

    <!-- LOGIN SCREEN -->
    <div class="login-card" id="login-card">
        <div class="avatar">G</div>
        <h1>Ghost-OS</h1>
        <p>Behavioral Biometric Login</p>

        <div class="input-group">
            <input type="text" id="pwd-input" placeholder="Enter Password" autocomplete="off">
            <div class="bio-bar" id="bio-bar"></div>
        </div>

        <div class="status-text" id="status-text">System Locked.</div>

        <div class="controls">
            <button class="btn active" id="btn-train" onclick="setMode('train')">1. Train</button>
            <button class="btn" id="btn-login" onclick="setMode('verify')">2. Login</button>
            <button class="btn btn-hack" onclick="simulateHack()">3. Hack</button>
        </div>
    </div>

    <!-- SECURE VAULT -->
    <div id="vault-screen">
        <h1 style="color: var(--success); font-size: 2.5rem;">ACCESS GRANTED</h1>
        <p>Welcome to the Secure Vault</p>
        
        <div class="folder-grid">
            <div class="folder">
                <div class="folder-icon">☢️</div>
                <div class="folder-name">Nuclear Codes</div>
            </div>
            <div class="folder">
                <div class="folder-icon">🏦</div>
                <div class="folder-name">Swiss Accounts</div>
            </div>
            <div class="folder">
                <div class="folder-icon">📂</div>
                <div class="folder-name">Project X</div>
            </div>
        </div>

        <button class="btn btn-hack" style="margin-top: 50px;" onclick="location.reload()">LOGOUT</button>
    </div>

    <script>
        let mode = 'train';
        let flightTimes = [];
        let holdTimes = [];
        let keyDownMap = {};
        let lastKeyUpTime = 0;
        let phrase = "{{ phrase }}";
        let isModelTrained = false;

        const pwdInput = document.getElementById('pwd-input');
        const bioBar = document.getElementById('bio-bar');
        const statusText = document.getElementById('status-text');
        const loginCard = document.getElementById('login-card');
        const vaultScreen = document.getElementById('vault-screen');

        // Set initial placeholder
        pwdInput.placeholder = `Type: "${phrase}"`;

        function setMode(m) {
            mode = m;
            resetUI();
            
            // Toggle Buttons
            document.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
            
            if(m === 'train') {
                document.getElementById('btn-train').classList.add('active');
                statusText.innerText = "Training: Type naturally to learn pattern.";
                statusText.style.color = "var(--primary)";
                pwdInput.placeholder = `Type: "${phrase}"`;
            } else {
                if(!isModelTrained) { 
                    alert("⚠️ First TRAIN the model!"); 
                    setMode('train'); 
                    return; 
                }
                document.getElementById('btn-login').classList.add('active');
                statusText.innerText = "Secure Login: Enter password.";
                statusText.style.color = "var(--text-sub)";
                pwdInput.placeholder = "Enter Password";
            }
        }

        function resetUI() {
            pwdInput.value = '';
            pwdInput.disabled = false;
            pwdInput.classList.remove('shake');
            flightTimes = [];
            holdTimes = [];
            keyDownMap = {};
            lastKeyUpTime = 0;
            bioBar.style.width = '0%';
            pwdInput.focus();
        }

        // --- KEYSTROKE CAPTURE ---
        pwdInput.addEventListener('keydown', e => {
            if(e.key === 'Enter') return;
            if(!keyDownMap[e.code]) keyDownMap[e.code] = Date.now();
        });

        pwdInput.addEventListener('keyup', e => {
            let now = Date.now();
            
            // Visual Progress
            let progress = (pwdInput.value.length / phrase.length) * 100;
            bioBar.style.width = `${progress}%`;

            // Hold Time
            if(keyDownMap[e.code]) {
                holdTimes.push(now - keyDownMap[e.code]);
                delete keyDownMap[e.code];
            }

            // Flight Time
            if(lastKeyUpTime !== 0) {
                flightTimes.push(now - lastKeyUpTime);
            }
            lastKeyUpTime = now;

            // Auto-Submit on completion
            if(pwdInput.value.length >= phrase.length) {
                pwdInput.disabled = true;
                statusText.innerText = "Analyzing Biometric Signature...";
                setTimeout(processData, 600);
            }
        });

        async function processData() {
            // Step 1: Check Password Text
            if(pwdInput.value !== phrase) {
                loginFail("Incorrect Password");
                return;
            }

            // Step 2: Send Vectors to Python
            const res = await fetch('/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    mode: mode === 'bot' ? 'verify' : mode,
                    flight_times: flightTimes,
                    hold_times: holdTimes,
                    is_bot_simulation: mode === 'bot'
                })
            });
            const data = await res.json();

            if(data.status === 'trained') {
                isModelTrained = true;
                alert("✅ Pattern Learned! Now switch to LOGIN mode.");
                setMode('verify');
            } else if (data.status === 'verified') {
                loginSuccess();
            } else {
                loginFail(data.reason);
            }
        }

        function loginSuccess() {
            statusText.innerText = "Access Granted.";
            statusText.style.color = "var(--success)";
            pwdInput.style.borderColor = "var(--success)";
            
            setTimeout(() => {
                loginCard.style.display = 'none';
                vaultScreen.style.display = 'flex';
            }, 800);
        }

        function loginFail(reason) {
            pwdInput.classList.add('shake');
            pwdInput.style.borderColor = "var(--danger)";
            statusText.innerText = `⛔ Denied: ${reason}`;
            statusText.style.color = "var(--danger)";
            
            setTimeout(() => {
                resetUI();
                pwdInput.style.borderColor = "rgba(255,255,255,0.1)";
                statusText.style.color = "var(--text-sub)";
                statusText.innerText = "Try Again.";
            }, 2000);
        }

        function simulateHack() {
            if(!isModelTrained) { alert("Train first!"); return; }
            setMode('verify');
            mode = 'bot';
            
            statusText.innerText = "⚠️ Bot Attack Detected...";
            statusText.style.color = "var(--danger)";
            pwdInput.disabled = true;

            let chars = phrase.split('');
            let i = 0;
            let intv = setInterval(() => {
                if(i < chars.length) {
                    pwdInput.value += chars[i];
                    flightTimes.push(50); // Perfect robotic timing
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

# --- PYTHON BACKEND LOGIC (CORE GHOST-AUTH) ---
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

    if not flight_times:
        return jsonify({"status": "error", "message": "No data captured"})

    # --- NUMPY ANALYSIS ---
    
    if mode == 'train':
        # Create Profile
        f_arr = np.array(flight_times)
        h_arr = np.array(hold_times)
        
        user_profile["flight_avg"] = flight_times
        user_profile["flight_std"] = float(np.std(f_arr))
        user_profile["hold_avg"] = hold_times
        user_profile["hold_std"] = float(np.std(h_arr))
        user_profile["trained"] = True
        
        return jsonify({"status": "trained"})

    elif mode == 'verify':
        if not user_profile["trained"]:
            return jsonify({"status": "denied", "score": 0, "reason": "Model Untrained"})

        # Normalize & Compare (Relative Rhythm)
        curr_flight = np.array(flight_times)
        ref_flight = np.array(user_profile["flight_avg"])
        
        min_len = min(len(curr_flight), len(ref_flight))
        
        # Calculate Difference (Manhattan Distance)
        flight_diff = np.mean(np.abs(curr_flight[:min_len] - ref_flight[:min_len]))
        
        # Trust Score Calculation (Simple Logic)
        score = max(0, 100 - flight_diff)

        # Bot Detection (Variance Check)
        flight_var = np.std(curr_flight)
        
        if is_bot or flight_var < 5:
            return jsonify({
                "status": "denied",
                "score": 5,
                "reason": "Robotic Behavior (Zero Variance)"
            })
        
        elif score > 50:
            return jsonify({"status": "verified", "score": int(score)})
        else:
            return jsonify({
                "status": "denied",
                "score": int(score),
                "reason": "Typing Pattern Mismatch"
            })

if __name__ == '__main__':
    app.run(debug=True, port=5000).