import json
import time
import numpy as np  # Numpy for advanced math
from flask import Flask, render_template_string, request, jsonify

# --- CONFIGURATION ---
app = Flask(__name__)
TARGET_PHRASE = "ghost auth is the future"

# --- HTML/CSS/JS UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GHOST-AUTH | Advanced Core</title>
    <style>
        :root {
            --primary: #00f3ff;
            --secondary: #7000ff;
            --bg: #050510;
            --panel: #0a0a1a;
            --danger: #ff0055;
            --success: #00ff9d;
        }
        body {
            background-color: var(--bg);
            color: #fff;
            font-family: 'Courier New', monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            overflow-x: hidden;
        }
        .container {
            width: 90%;
            max-width: 900px;
            text-align: center;
        }
        h1 {
            font-size: 3rem;
            text-shadow: 0 0 20px var(--primary);
            margin-bottom: 10px;
        }
        h1 span { color: var(--primary); }
        .subtitle { color: #888; margin-bottom: 40px; }
        
        .card {
            background: var(--panel);
            border: 1px solid #333;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 0 40px rgba(0, 243, 255, 0.05);
            position: relative;
            overflow: hidden;
        }
        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 5px;
            background: linear-gradient(90deg, var(--danger), var(--primary), var(--secondary), var(--success));
        }

        input[type="text"] {
            width: 100%;
            background: #000;
            border: 2px solid #333;
            color: var(--primary);
            font-size: 1.5rem;
            padding: 15px;
            text-align: center;
            border-radius: 8px;
            margin-top: 20px;
            outline: none;
            transition: 0.3s;
            font-family: 'Courier New', monospace;
            letter-spacing: 2px;
        }
        input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.2);
        }

        .btn-group { margin-top: 30px; display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; }
        button {
            padding: 12px 24px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            border: none;
            border-radius: 5px;
            transition: 0.3s;
            text-transform: uppercase;
            position: relative;
            overflow: hidden;
        }
        .btn-train { background: linear-gradient(45deg, var(--secondary), var(--primary)); color: #000; }
        .btn-verify { background: transparent; border: 2px solid var(--primary); color: var(--primary); }
        .btn-bot { background: var(--danger); color: #fff; box-shadow: 0 0 15px var(--danger); }
        
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.5); }

        #status { margin-top: 20px; font-weight: bold; min-height: 25px; letter-spacing: 1px; }
        
        /* Advanced Visualizer */
        .metrics-container {
            display: flex;
            justify-content: space-between;
            margin-top: 30px;
            gap: 10px;
        }
        .metric-box {
            background: rgba(255,255,255,0.05);
            padding: 10px;
            border-radius: 8px;
            width: 48%;
        }
        .metric-title { font-size: 0.8rem; color: #888; margin-bottom: 5px; text-transform: uppercase; }
        
        .visualizer {
            display: flex;
            align-items: flex-end;
            justify-content: center;
            height: 50px;
            gap: 2px;
        }
        .bar { width: 4px; background: #333; transition: height 0.1s; border-radius: 2px; }

        #result-area {
            display: none;
            margin-top: 30px;
            padding: 20px;
            border-radius: 10px;
            animation: fadeIn 0.5s ease;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        .success { background: rgba(0, 255, 157, 0.1); border: 1px solid var(--success); color: var(--success); }
        .fail { background: rgba(255, 0, 85, 0.1); border: 1px solid var(--danger); color: var(--danger); }
        
        .tag {
            font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; border: 1px solid #555; color: #aaa;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>GHOST<span>-AUTH</span> <span style="font-size: 1rem; vertical-align: middle; color: #fff; border: 1px solid #fff; padding: 2px 5px; border-radius: 4px;">PRO</span></h1>
        <p class="subtitle">Multi-Dimensional Behavioral Biometrics Engine</p>

        <div class="card">
            <div id="instruction-text" style="color: #aaa; margin-bottom: 10px;">
                STEP 1: Train the Python Model
            </div>
            
            <div style="font-size: 1.2rem; margin-bottom: 5px;">Type this phrase:</div>
            <h2 id="target-phrase" style="letter-spacing: 2px; color: #fff;">{{ phrase }}</h2>

            <input type="text" id="input-box" placeholder="Type here..." autocomplete="off">
            
            <div class="metrics-container">
                <div class="metric-box">
                    <div class="metric-title">Flight Dynamics (Speed)</div>
                    <div class="visualizer" id="vis-flight"></div>
                </div>
                <div class="metric-box">
                    <div class="metric-title">Dwell Dynamics (Hold Time)</div>
                    <div class="visualizer" id="vis-hold"></div>
                </div>
            </div>

            <div id="status"></div>

            <div class="btn-group">
                <button class="btn-train" onclick="setMode('train')">1. Train Pattern</button>
                <button class="btn-verify" onclick="attemptVerify()">2. Verify Identity</button>
                <button class="btn-bot" onclick="attemptBot()">3. Bot Attack Simulation</button>
            </div>

            <div id="result-area"></div>
        </div>
    </div>

    <script>
        let mode = 'train';
        let flightTimes = [];
        let holdTimes = [];
        let lastKeyUpTime = 0;
        let keyDownMap = {}; // Tracks when a key was pressed
        let phrase = "{{ phrase }}";
        let isModelTrained = false; 
        
        const inputBox = document.getElementById('input-box');
        const visFlight = document.getElementById('vis-flight');
        const visHold = document.getElementById('vis-hold');
        const status = document.getElementById('status');
        const resultArea = document.getElementById('result-area');
        const instrText = document.getElementById('instruction-text');

        // Setup Bars for both visualizers
        function createBars(container) {
            container.innerHTML = '';
            for(let i=0; i<30; i++) {
                let bar = document.createElement('div');
                bar.className = 'bar';
                bar.style.height = '4px';
                container.appendChild(bar);
            }
        }
        createBars(visFlight);
        createBars(visHold);

        function attemptVerify() {
            if (!isModelTrained) {
                alert("⚠️ Please TRAIN the model first! (Click Step 1)");
                return;
            }
            setMode('verify');
        }

        function attemptBot() {
            if (!isModelTrained) {
                alert("⚠️ Please TRAIN the model first! (Click Step 1)");
                return;
            }
            simulateBot();
        }

        function setMode(newMode) {
            mode = newMode;
            resetUI();
            if(mode === 'train') instrText.innerText = "STEP 1: Train your unique pattern (Type naturally)";
            if(mode === 'verify') instrText.innerText = "STEP 2: Verify Identity (Type again)";
            status.innerText = mode.toUpperCase() + " MODE ACTIVE";
            status.style.color = mode === 'train' ? 'var(--primary)' : '#fff';
        }

        function resetUI() {
            inputBox.value = '';
            inputBox.disabled = false;
            flightTimes = [];
            holdTimes = [];
            lastKeyUpTime = 0;
            keyDownMap = {};
            resultArea.style.display = 'none';
            inputBox.focus();
            document.querySelectorAll('.bar').forEach(b => {
                b.style.height = '4px'; 
                b.style.background = '#333';
            });
        }

        // --- ADVANCED KEYSTROKE CAPTURE LOGIC ---
        inputBox.addEventListener('keydown', (e) => {
            if(e.key === 'Enter') {
                processData();
                return;
            }
            // Record press time for Dwell calculation
            if (!keyDownMap[e.code]) {
                keyDownMap[e.code] = Date.now();
            }
        });

        inputBox.addEventListener('keyup', (e) => {
            let currTime = Date.now();
            
            // 1. Calculate Dwell Time (Hold Time)
            if (keyDownMap[e.code]) {
                let holdTime = currTime - keyDownMap[e.code];
                holdTimes.push(holdTime);
                updateVisualizer(visHold, holdTime, 2.0); // Visualize Hold
                delete keyDownMap[e.code];
            }

            // 2. Calculate Flight Time (Latency between keys)
            if (lastKeyUpTime !== 0) {
                let flightTime = currTime - lastKeyUpTime;
                flightTimes.push(flightTime);
                updateVisualizer(visFlight, flightTime, 1.0); // Visualize Flight
            }
            lastKeyUpTime = currTime;
            
            if (inputBox.value.length === phrase.length) {
                setTimeout(processData, 200);
            }
        });

        function updateVisualizer(container, val, scale) {
            const bars = container.querySelectorAll('.bar');
            for(let i=0; i<bars.length-1; i++) {
                bars[i].style.height = bars[i+1].style.height;
                bars[i].style.background = bars[i+1].style.background;
            }
            let lastBar = bars[bars.length-1];
            let h = Math.min(val * scale, 45);
            lastBar.style.height = Math.max(h, 4) + 'px';
            lastBar.style.background = mode === 'train' ? 'var(--primary)' : (mode === 'bot' ? 'var(--danger)' : '#fff');
        }

        async function processData() {
            if (inputBox.value !== phrase) {
                status.innerText = "❌ TYPO DETECTED! Type exactly as shown.";
                status.style.color = "var(--danger)";
                return;
            }

            status.innerText = "⏳ Processing Multi-Dimensional Vectors...";
            
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    mode: mode === 'bot' ? 'verify' : mode, 
                    flight_times: flightTimes,
                    hold_times: holdTimes,
                    is_bot_simulation: mode === 'bot'
                })
            });
            
            const data = await response.json();
            showResult(data);
        }

        function showResult(data) {
            resultArea.style.display = 'block';
            if (data.status === 'trained') {
                isModelTrained = true; 
                resultArea.className = 'success';
                resultArea.innerHTML = `<h3>✅ BIO-PROFILE CREATED</h3><p>${data.message}</p>
                <div style="margin-top:10px; font-size:0.8rem; opacity:0.8">
                    <span class="tag">Flight Vectors: ${data.details.flight_points}</span>
                    <span class="tag">Dwell Vectors: ${data.details.hold_points}</span>
                </div>`;
                setTimeout(() => setMode('verify'), 2000);
            } else if (data.status === 'verified') {
                resultArea.className = 'success';
                resultArea.innerHTML = `<h1>🔓 ACCESS GRANTED</h1>
                <p>Trust Score: <b>${data.score}%</b></p>
                <div style="font-size:0.8rem; margin-top:5px; color:#aaa">
                    Rhythm Match: High | Pressure Match: High
                </div>`;
            } else {
                resultArea.className = 'fail';
                resultArea.innerHTML = `<h1>🔒 ACCESS DENIED</h1>
                <p>Trust Score: <b>${data.score}%</b></p>
                <p style="background:rgba(0,0,0,0.3); padding:5px; border-radius:4px;">REASON: ${data.reason}</p>`;
            }
        }

        function simulateBot() {
            mode = 'bot';
            resetUI();
            instrText.innerText = "⚠️ SIMULATION: Advanced Script Injection...";
            status.innerText = "BOT ATTACK INITIATED...";
            
            let chars = phrase.split('');
            let i = 0;
            inputBox.disabled = true;
            
            let botInterval = setInterval(() => {
                if (i < chars.length) {
                    inputBox.value += chars[i];
                    
                    // Bot Behavior: Perfectly constant speed AND perfectly constant hold time
                    flightTimes.push(50); 
                    holdTimes.push(80); // Bots hold keys for exact same duration
                    
                    updateVisualizer(visFlight, 50, 1.0);
                    updateVisualizer(visHold, 80, 2.0);
                    i++;
                } else {
                    clearInterval(botInterval);
                    processData();
                }
            }, 50); // Fast typing speed
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

        # --- DUAL LAYER VERIFICATION ---
        
        # Layer 1: Flight Time Analysis
        curr_flight = np.array(flight_times)
        ref_flight = np.array(user_profile["flight_avg"])
        min_len_f = min(len(curr_flight), len(ref_flight))
        
        flight_diff = np.mean(np.abs(curr_flight[:min_len_f] - ref_flight[:min_len_f]))
        flight_score = max(0, 100 - flight_diff)

        # Layer 2: Hold Time Analysis
        curr_hold = np.array(hold_times)
        ref_hold = np.array(user_profile["hold_avg"])
        min_len_h = min(len(curr_hold), len(ref_hold))
        
        hold_diff = np.mean(np.abs(curr_hold[:min_len_h] - ref_hold[:min_len_h]))
        hold_score = max(0, 100 - hold_diff)

        # Combined Trust Score (Weighted)
        final_score = int((flight_score * 0.6) + (hold_score * 0.4))
        
        # --- BOT DETECTION (The Trap) ---
        # Check variance of BOTH dimensions. Bots are too stable.
        flight_var = np.std(curr_flight)
        hold_var = np.std(curr_hold)
        
        if is_bot or (flight_var < 5 and hold_var < 5):
            return jsonify({
                "status": "denied",
                "score": 2,
                "reason": "⚠️ BOT DETECTED: Typing is too perfect (Robotic Behavior)."
            })
        
        elif final_score > 60:
            return jsonify({
                "status": "verified",
                "score": final_score
            })
        else:
            reason = "Typing Speed/Rhythm changed" if flight_score < hold_score else "Key Hold Time (Pressure) changed"
            return jsonify({
                "status": "denied",
                "score": final_score,
                "reason": f"IDENTITY MISMATCH: Your {reason}"
            })

if __name__ == '__main__':
    app.run(debug=True, port=5000)