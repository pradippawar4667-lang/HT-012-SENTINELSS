import json
import time
import numpy as np  # Numpy for advanced math
from flask import Flask, render_template_string, request, jsonify

# --- CONFIGURATION ---
app = Flask(__name__)
TARGET_PHRASE = "ghost auth is the future"

# --- HTML/CSS/JS UI (CREATIVE DASHBOARD) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GHOST-AUTH | Cyber Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --neon-blue: #00f3ff;
            --neon-pink: #ff0055;
            --neon-green: #00ff9d;
            --bg-dark: #050505;
            --panel-bg: rgba(10, 20, 30, 0.85);
            --border-color: rgba(0, 243, 255, 0.3);
        }
        
        * { box-sizing: border-box; }

        body {
            background-color: var(--bg-dark);
            background-image: 
                linear-gradient(rgba(0, 243, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px);
            background-size: 30px 30px;
            color: #fff;
            font-family: 'Share Tech Mono', monospace;
            margin: 0;
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        /* --- HEADER --- */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 30px;
            border-bottom: 2px solid var(--border-color);
            background: rgba(0,0,0,0.8);
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.1);
        }
        
        .logo {
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            letter-spacing: 3px;
            text-shadow: 0 0 10px var(--neon-blue);
        }
        .logo span { color: var(--neon-blue); }
        
        .sys-status {
            color: var(--neon-green);
            font-size: 0.9rem;
            border: 1px solid var(--neon-green);
            padding: 5px 15px;
            border-radius: 20px;
            text-shadow: 0 0 5px var(--neon-green);
            animation: blink 2s infinite;
        }

        /* --- MAIN DASHBOARD LAYOUT --- */
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 2fr 1fr;
            gap: 20px;
            padding: 20px;
            height: 100%;
            flex-grow: 1;
        }

        .panel {
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 20px;
            position: relative;
            backdrop-filter: blur(5px);
            display: flex;
            flex-direction: column;
        }
        
        .panel::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 2px;
            background: linear-gradient(90deg, transparent, var(--neon-blue), transparent);
        }

        .panel-title {
            font-family: 'Orbitron', sans-serif;
            color: var(--neon-blue);
            font-size: 1.1rem;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 10px;
        }

        /* --- CENTER CONSOLE --- */
        .console-screen {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }

        .phrase-display {
            font-size: 1.5rem;
            margin-bottom: 30px;
            color: #aaa;
        }
        .phrase-highlight {
            color: #fff;
            text-shadow: 0 0 10px #fff;
            letter-spacing: 2px;
        }

        input[type="text"] {
            background: rgba(0,0,0,0.5);
            border: 2px solid var(--border-color);
            color: var(--neon-blue);
            font-family: 'Share Tech Mono', monospace;
            font-size: 2rem;
            padding: 15px;
            width: 100%;
            text-align: center;
            outline: none;
            transition: 0.3s;
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.1);
            border-radius: 5px;
        }
        input:focus {
            box-shadow: 0 0 30px rgba(0, 243, 255, 0.3);
            border-color: var(--neon-blue);
        }

        /* --- VISUALIZER --- */
        .visualizer-container {
            display: flex;
            justify-content: center;
            align-items: flex-end;
            height: 60px;
            gap: 4px;
            margin: 30px 0;
            width: 100%;
        }
        .bar {
            width: 6px;
            background: var(--neon-blue);
            height: 5px;
            transition: height 0.1s ease;
            box-shadow: 0 0 5px var(--neon-blue);
        }

        /* --- BUTTONS --- */
        .controls {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 20px;
        }
        
        .cyber-btn {
            background: transparent;
            border: 1px solid var(--neon-blue);
            color: var(--neon-blue);
            padding: 15px 30px;
            font-family: 'Orbitron', sans-serif;
            font-size: 1rem;
            cursor: pointer;
            transition: 0.3s;
            text-transform: uppercase;
            letter-spacing: 2px;
            position: relative;
            overflow: hidden;
        }
        
        .cyber-btn:hover {
            background: var(--neon-blue);
            color: #000;
            box-shadow: 0 0 20px var(--neon-blue);
        }
        
        .btn-bot {
            border-color: var(--neon-pink);
            color: var(--neon-pink);
        }
        .btn-bot:hover {
            background: var(--neon-pink);
            color: #fff;
            box-shadow: 0 0 20px var(--neon-pink);
        }

        /* --- RIGHT PANEL: TERMINAL --- */
        .terminal {
            font-size: 0.8rem;
            color: #aaa;
            overflow-y: auto;
            height: 100%;
            text-align: left;
        }
        .log-entry { margin-bottom: 5px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 2px; }
        .log-time { color: var(--neon-blue); margin-right: 10px; }
        .log-info { color: var(--neon-green); }
        .log-warn { color: var(--neon-pink); }

        /* --- LEFT PANEL: STATS --- */
        .stat-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            font-size: 0.9rem;
        }
        .stat-val { color: var(--neon-blue); font-weight: bold; }

        /* --- RESULT OVERLAY --- */
        #result-overlay {
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.95);
            border: 2px solid var(--neon-blue);
            padding: 40px;
            text-align: center;
            z-index: 100;
            display: none;
            box-shadow: 0 0 50px rgba(0,0,0,0.8);
            border-radius: 10px;
            min-width: 400px;
        }
        
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }

    </style>
</head>
<body>

    <header>
        <div class="logo">GHOST<span>-AUTH</span></div>
        <div class="sys-status">SYSTEM ONLINE</div>
    </header>

    <div class="dashboard">
        
        <!-- LEFT PANEL: BIOMETRIC STATS -->
        <div class="panel">
            <div class="panel-title">BIO-METRICS</div>
            <div class="stat-row">
                <span>Subject ID:</span>
                <span class="stat-val">USER-01</span>
            </div>
            <div class="stat-row">
                <span>Model Status:</span>
                <span class="stat-val" id="model-status" style="color: #555;">UNTRAINED</span>
            </div>
            <div class="stat-row">
                <span>Flight Vectors:</span>
                <span class="stat-val" id="flight-count">0</span>
            </div>
            <div class="stat-row">
                <span>Dwell Vectors:</span>
                <span class="stat-val" id="dwell-count">0</span>
            </div>
            
            <div style="margin-top: auto; border: 1px solid #333; padding: 10px; text-align: center;">
                <div style="font-size: 0.7rem; color: #555;">SECURITY LEVEL</div>
                <div style="font-size: 2rem; color: var(--neon-green);">A+</div>
            </div>
        </div>

        <!-- CENTER PANEL: INTERACTION CONSOLE -->
        <div class="panel">
            <div class="panel-title" id="mode-display">MODE: TRAINING</div>
            
            <div class="console-screen">
                <div class="phrase-display">
                    Passphrase Required:<br>
                    <span class="phrase-highlight">{{ phrase }}</span>
                </div>

                <input type="text" id="input-box" placeholder="AWAITING INPUT..." autocomplete="off">
                
                <div class="visualizer-container" id="visualizer">
                    <!-- JS will fill bars -->
                </div>
            </div>

            <div class="controls">
                <button class="cyber-btn" onclick="setMode('train')">Initialize / Train</button>
                <button class="cyber-btn" onclick="attemptVerify()">Verify Identity</button>
                <button class="cyber-btn btn-bot" onclick="attemptBot()">Simulate Hack</button>
            </div>
        </div>

        <!-- RIGHT PANEL: LIVE LOGS -->
        <div class="panel">
            <div class="panel-title">SYSTEM LOGS</div>
            <div class="terminal" id="terminal-logs">
                <div class="log-entry"><span class="log-time">10:00:01</span> System Boot Sequence...</div>
                <div class="log-entry"><span class="log-time">10:00:02</span> Loading Numpy Core...</div>
                <div class="log-entry"><span class="log-time">10:00:03</span> Ready for Enrollment.</div>
            </div>
        </div>

    </div>

    <!-- RESULT POPUP -->
    <div id="result-overlay">
        <h1 id="res-title" style="margin: 0 0 10px 0;">ACCESS GRANTED</h1>
        <p id="res-desc" style="color: #aaa;">Identity Verified Successfully</p>
        <h2 id="res-score" style="font-size: 3rem; margin: 20px 0; color: var(--neon-green);">98%</h2>
        <button class="cyber-btn" onclick="closeResult()">CLOSE</button>
    </div>

    <script>
        let mode = 'train';
        let flightTimes = [];
        let holdTimes = [];
        let keyDownMap = {};
        let lastKeyUpTime = 0;
        let phrase = "{{ phrase }}";
        let isModelTrained = false;

        const inputBox = document.getElementById('input-box');
        const visualizer = document.getElementById('visualizer');
        const term = document.getElementById('terminal-logs');
        const modeDisplay = document.getElementById('mode-display');
        const modelStatus = document.getElementById('model-status');
        
        // Init Visualizer
        for(let i=0; i<40; i++){
            let d = document.createElement('div');
            d.className = 'bar';
            visualizer.appendChild(d);
        }

        function log(msg, type='info') {
            const now = new Date();
            const timeStr = now.toLocaleTimeString();
            const div = document.createElement('div');
            div.className = 'log-entry';
            let colorClass = type === 'warn' ? 'log-warn' : 'log-info';
            div.innerHTML = `<span class="log-time">${timeStr}</span> <span class="${colorClass}">${msg}</span>`;
            term.prepend(div);
        }

        function setMode(m) {
            mode = m;
            resetUI();
            if (m === 'train') {
                modeDisplay.innerText = "MODE: TRAINING (ENROLLMENT)";
                modeDisplay.style.color = "var(--neon-blue)";
                log("Switched to Training Mode. Please type the phrase.");
            } else if (m === 'verify') {
                modeDisplay.innerText = "MODE: VERIFICATION (ACTIVE)";
                modeDisplay.style.color = "var(--neon-green)";
                log("Verification Mode Active. Waiting for user input.");
            }
        }

        function attemptVerify() {
            if(!isModelTrained) { alert("Train the model first!"); return; }
            setMode('verify');
        }

        function attemptBot() {
            if(!isModelTrained) { alert("Train the model first!"); return; }
            simulateBot();
        }

        function resetUI() {
            inputBox.value = '';
            inputBox.disabled = false;
            flightTimes = [];
            holdTimes = [];
            lastKeyUpTime = 0;
            keyDownMap = {};
            inputBox.focus();
            document.querySelectorAll('.bar').forEach(b => b.style.height = '5px');
        }

        // --- INPUT LOGIC ---
        inputBox.addEventListener('keydown', e => {
            if(e.key === 'Enter') return;
            if(!keyDownMap[e.code]) keyDownMap[e.code] = Date.now();
        });

        inputBox.addEventListener('keyup', e => {
            let now = Date.now();
            
            // Hold Time
            if(keyDownMap[e.code]) {
                let hold = now - keyDownMap[e.code];
                holdTimes.push(hold);
                updateVis(hold);
                delete keyDownMap[e.code];
            }

            // Flight Time
            if(lastKeyUpTime !== 0) {
                let flight = now - lastKeyUpTime;
                flightTimes.push(flight);
            }
            lastKeyUpTime = now;

            if(inputBox.value.length === phrase.length) {
                log("Phrase complete. Processing...", "info");
                processData();
            }
        });

        function updateVis(val) {
            const bars = document.querySelectorAll('.bar');
            for(let i=0; i<bars.length-1; i++) {
                bars[i].style.height = bars[i+1].style.height;
                bars[i].style.boxShadow = bars[i+1].style.boxShadow;
            }
            let last = bars[bars.length-1];
            let h = Math.min(val * 2, 55);
            last.style.height = h + 'px';
            
            let color = mode === 'bot' ? 'var(--neon-pink)' : 'var(--neon-blue)';
            last.style.background = color;
            last.style.boxShadow = `0 0 10px ${color}`;
        }

        async function processData() {
            if(inputBox.value !== phrase) {
                log("Typo Detected. Resetting...", "warn");
                resetUI();
                return;
            }

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
            handleResult(data);
        }

        function handleResult(data) {
            if(data.status === 'trained') {
                isModelTrained = true;
                modelStatus.innerText = "ACTIVE";
                modelStatus.style.color = "var(--neon-green)";
                document.getElementById('flight-count').innerText = data.details.flight_points;
                document.getElementById('dwell-count').innerText = data.details.hold_points;
                log("Model Trained Successfully.", "info");
                alert("Model Trained! Now click 'Verify Identity'");
                setMode('verify');
            } else {
                showOverlay(data);
            }
        }

        function showOverlay(data) {
            const overlay = document.getElementById('result-overlay');
            const title = document.getElementById('res-title');
            const desc = document.getElementById('res-desc');
            const score = document.getElementById('res-score');

            overlay.style.display = 'block';
            
            if(data.status === 'verified') {
                title.innerText = "ACCESS GRANTED";
                title.style.color = "var(--neon-green)";
                overlay.style.borderColor = "var(--neon-green)";
                score.style.color = "var(--neon-green)";
                log(`Access Granted. Score: ${data.score}%`);
            } else {
                title.innerText = "ACCESS DENIED";
                title.style.color = "var(--neon-pink)";
                overlay.style.borderColor = "var(--neon-pink)";
                score.style.color = "var(--neon-pink)";
                log(`Access Denied. Reason: ${data.reason}`, "warn");
            }
            desc.innerText = data.reason || "Biometric Match Confirmed";
            score.innerText = data.score + "%";
        }

        function closeResult() {
            document.getElementById('result-overlay').style.display = 'none';
            resetUI();
        }

        function simulateBot() {
            mode = 'bot';
            resetUI();
            modeDisplay.innerText = "ALERT: BOT ATTACK IN PROGRESS";
            modeDisplay.style.color = "var(--neon-pink)";
            log("Bot Script Injected...", "warn");
            inputBox.disabled = true;

            let chars = phrase.split('');
            let i = 0;
            let intv = setInterval(() => {
                if(i < chars.length) {
                    inputBox.value += chars[i];
                    flightTimes.push(50);
                    holdTimes.push(80);
                    updateVis(80);
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
        # Formula: Vector - Mean(Vector)
        curr_f_norm = curr_flight[:min_len_f] - np.mean(curr_flight)
        ref_f_norm = ref_flight[:min_len_f] - np.mean(ref_flight)
        
        # Compare Patterns
        flight_diff = np.mean(np.abs(curr_f_norm - ref_f_norm))
        flight_score = max(0, 100 - flight_diff)

        # Layer 2: Hold Time Analysis (STYLE)
        curr_hold = np.array(hold_times)
        ref_hold = np.array(user_profile["hold_avg"])
        min_len_h = min(len(curr_hold), len(ref_hold))
        
        # Normalize Hold Times too
        curr_h_norm = curr_hold[:min_len_h] - np.mean(curr_hold)
        ref_h_norm = ref_hold[:min_len_h] - np.mean(ref_hold)
        
        hold_diff = np.mean(np.abs(curr_h_norm - ref_h_norm))
        hold_score = max(0, 100 - hold_diff)

        # Combined Trust Score (Weighted)
        final_score = int((flight_score * 0.6) + (hold_score * 0.4))
        
        # --- BOT DETECTION (The Trap) ---
        # Check variance of BOTH dimensions. Bots are too stable.
        flight_var = np.std(curr_flight)
        hold_var = np.std(curr_hold)
        
        if is_bot or (flight_var < 2 and hold_var < 2):
            return jsonify({
                "status": "denied",
                "score": 5,
                "reason": "⚠️ Robotic Behavior Detected (Zero Variance)"
            })
        
        elif final_score > 55: # Slightly relaxed threshold for normalization
            return jsonify({
                "status": "verified",
                "score": final_score
            })
        else:
            reason = "Typing Speed/Rhythm changed" if flight_score < hold_score else "Key Hold Time (Pressure) changed"
            return jsonify({
                "status": "denied",
                "score": final_score,
                "reason": f"IDENTITY MISMATCH: {reason}"
            })

if __name__ == '__main__':
    app.run(debug=True, port=5000)