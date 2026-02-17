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
    <title>GHOST-AUTH | Elite Cyber Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --neon-blue: #00f3ff;
            --neon-pink: #ff0055;
            --neon-purple: #bc13fe;
            --neon-green: #00ff9d;
            --bg-dark: #030305;
            --panel-bg: rgba(10, 15, 25, 0.7);
            --border-color: rgba(0, 243, 255, 0.2);
            --glass-border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        * { box-sizing: border-box; }

        body {
            background-color: var(--bg-dark);
            background-image: 
                linear-gradient(rgba(0, 243, 255, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 243, 255, 0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            color: #fff;
            font-family: 'JetBrains Mono', monospace;
            margin: 0;
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            animation: bgScroll 20s linear infinite;
        }

        @keyframes bgScroll {
            0% { background-position: 0 0; }
            100% { background-position: 40px 40px; }
        }

        /* --- HEADER --- */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 40px;
            background: rgba(3, 3, 5, 0.8);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border-color);
            z-index: 10;
        }
        
        .logo {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.2rem;
            font-weight: 900;
            letter-spacing: 4px;
            background: linear-gradient(90deg, #fff, var(--neon-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(0, 243, 255, 0.5);
        }
        
        .sys-status {
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--neon-green);
            font-size: 0.8rem;
            letter-spacing: 1px;
        }
        .status-dot {
            width: 8px; height: 8px;
            background: var(--neon-green);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--neon-green);
            animation: pulseDot 2s infinite;
        }

        /* --- DASHBOARD --- */
        .dashboard {
            display: grid;
            grid-template-columns: 280px 1fr 300px;
            gap: 25px;
            padding: 30px;
            height: 100%;
            flex-grow: 1;
            position: relative;
        }

        .panel {
            background: var(--panel-bg);
            border: var(--glass-border);
            border-radius: 16px;
            padding: 25px;
            position: relative;
            backdrop-filter: blur(15px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .panel:hover {
            box-shadow: 0 10px 40px rgba(0, 243, 255, 0.05);
            border-color: rgba(0, 243, 255, 0.4);
        }

        .panel-title {
            font-family: 'Orbitron', sans-serif;
            color: var(--neon-blue);
            font-size: 0.9rem;
            font-weight: 700;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 2px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .panel-title::before {
            content: '';
            width: 4px; height: 16px;
            background: var(--neon-blue);
            box-shadow: 0 0 10px var(--neon-blue);
        }

        /* --- CENTER CONSOLE --- */
        .console-screen {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            position: relative;
        }
        
        /* Hexagon Background Effect for Center */
        .console-screen::before {
            content: '';
            position: absolute;
            width: 600px; height: 600px;
            background: radial-gradient(circle, rgba(0, 243, 255, 0.03) 0%, transparent 70%);
            z-index: -1;
            pointer-events: none;
        }

        .phrase-container {
            margin-bottom: 40px;
            position: relative;
        }
        
        .phrase-label {
            font-size: 0.8rem;
            color: #666;
            letter-spacing: 2px;
            margin-bottom: 10px;
            text-transform: uppercase;
        }

        .phrase-highlight {
            font-size: 2rem;
            color: #fff;
            text-shadow: 0 0 15px rgba(255,255,255,0.3);
            letter-spacing: 3px;
            font-weight: bold;
            position: relative;
            display: inline-block;
        }

        input[type="text"] {
            background: rgba(0, 0, 0, 0.6);
            border: 1px solid var(--border-color);
            color: var(--neon-blue);
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.8rem;
            padding: 20px;
            width: 100%;
            max-width: 600px;
            text-align: center;
            outline: none;
            transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
            border-radius: 12px;
            letter-spacing: 1px;
        }
        input:focus {
            box-shadow: 0 0 40px rgba(0, 243, 255, 0.15);
            border-color: var(--neon-blue);
            transform: scale(1.02);
        }

        /* --- VISUALIZER --- */
        .visualizer-container {
            display: flex;
            justify-content: center;
            align-items: flex-end;
            height: 80px;
            gap: 6px;
            margin: 40px 0;
            width: 100%;
            max-width: 600px;
            padding: 0 20px;
        }
        .bar {
            width: 8px;
            background: var(--neon-blue);
            height: 4px;
            border-radius: 4px;
            transition: height 0.1s ease, background-color 0.2s;
            box-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
            opacity: 0.8;
        }

        /* --- BUTTONS --- */
        .controls {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 20px;
        }
        
        .cyber-btn {
            background: rgba(0, 243, 255, 0.05);
            border: 1px solid var(--neon-blue);
            color: var(--neon-blue);
            padding: 16px 32px;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.9rem;
            font-weight: 700;
            cursor: pointer;
            transition: 0.3s;
            text-transform: uppercase;
            letter-spacing: 2px;
            position: relative;
            overflow: hidden;
            clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
        }
        
        .cyber-btn::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 243, 255, 0.2), transparent);
            transition: 0.5s;
        }
        
        .cyber-btn:hover::before { left: 100%; }
        
        .cyber-btn:hover {
            background: rgba(0, 243, 255, 0.15);
            text-shadow: 0 0 10px var(--neon-blue);
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.2);
            transform: translateY(-2px);
        }
        
        .btn-bot {
            border-color: var(--neon-pink);
            color: var(--neon-pink);
            background: rgba(255, 0, 85, 0.05);
        }
        .btn-bot:hover {
            background: rgba(255, 0, 85, 0.15);
            box-shadow: 0 0 20px rgba(255, 0, 85, 0.2);
            text-shadow: 0 0 10px var(--neon-pink);
        }
        
        .btn-bot::before { background: linear-gradient(90deg, transparent, rgba(255, 0, 85, 0.2), transparent); }

        /* --- TERMINAL --- */
        .terminal {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: #aaa;
            overflow-y: auto;
            height: 100%;
            text-align: left;
            padding-right: 5px;
        }
        /* Custom Scrollbar */
        .terminal::-webkit-scrollbar { width: 5px; }
        .terminal::-webkit-scrollbar-thumb { background: #333; border-radius: 2px; }
        
        .log-entry { margin-bottom: 8px; border-left: 2px solid transparent; padding-left: 8px; transition: 0.3s; }
        .log-entry:hover { border-left-color: var(--neon-blue); background: rgba(255,255,255,0.02); }
        .log-time { color: #555; font-size: 0.7rem; margin-right: 8px; }
        .log-info { color: var(--neon-blue); }
        .log-warn { color: var(--neon-pink); }
        .log-success { color: var(--neon-green); }

        /* --- STATS --- */
        .stat-card {
            background: rgba(255,255,255,0.03);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .stat-label { font-size: 0.8rem; color: #888; }
        .stat-val { font-family: 'Orbitron', sans-serif; color: #fff; font-size: 1.1rem; }
        .stat-highlight { color: var(--neon-blue); text-shadow: 0 0 10px rgba(0, 243, 255, 0.5); }

        /* --- RESULT OVERLAY --- */
        #result-overlay {
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%) scale(0.9);
            background: rgba(5, 5, 10, 0.95);
            border: 1px solid var(--neon-blue);
            padding: 50px;
            text-align: center;
            z-index: 100;
            display: none;
            box-shadow: 0 0 100px rgba(0, 0, 0, 0.9);
            border-radius: 20px;
            min-width: 450px;
            backdrop-filter: blur(20px);
            opacity: 0;
            transition: 0.3s ease;
        }
        
        #result-overlay.active {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
        }

        .res-icon { font-size: 4rem; margin-bottom: 20px; display: block; }
        
        @keyframes pulseDot { 0% { opacity: 0.5; } 50% { opacity: 1; box-shadow: 0 0 15px var(--neon-green); } 100% { opacity: 0.5; } }
    </style>
</head>
<body>

    <header>
        <div class="logo">GHOST<span>-AUTH</span></div>
        <div class="sys-status">
            <div class="status-dot"></div>
            SYSTEM SECURE
        </div>
    </header>

    <div class="dashboard">
        
        <!-- LEFT PANEL: STATS -->
        <div class="panel">
            <div class="panel-title">LIVE METRICS</div>
            
            <div class="stat-card">
                <span class="stat-label">SUBJECT</span>
                <span class="stat-val">USER-X</span>
            </div>
            
            <div class="stat-card">
                <span class="stat-label">STATUS</span>
                <span class="stat-val" id="model-status" style="color: #666;">OFFLINE</span>
            </div>
            
            <div style="margin: 20px 0; height: 1px; background: rgba(255,255,255,0.1);"></div>
            
            <div class="stat-card">
                <span class="stat-label">FLIGHT VECTORS</span>
                <span class="stat-val stat-highlight" id="flight-count">0</span>
            </div>
            
            <div class="stat-card">
                <span class="stat-label">DWELL VECTORS</span>
                <span class="stat-val stat-highlight" id="dwell-count">0</span>
            </div>
            
            <div style="margin-top: auto; text-align: center; opacity: 0.5; font-size: 0.7rem;">
                SECURE CONNECTION ESTABLISHED<br>
                ENC: AES-256
            </div>
        </div>

        <!-- CENTER PANEL: CONSOLE -->
        <div class="panel">
            <div class="panel-title" id="mode-display">AWAITING COMMAND...</div>
            
            <div class="console-screen">
                <div class="phrase-container">
                    <div class="phrase-label">AUTHENTICATION PASSPHRASE</div>
                    <div class="phrase-highlight">{{ phrase }}</div>
                </div>

                <input type="text" id="input-box" placeholder="CLICK TRAIN TO START" autocomplete="off">
                
                <div class="visualizer-container" id="visualizer">
                    <!-- JS will fill bars -->
                </div>
            </div>

            <div class="controls">
                <button class="cyber-btn" onclick="setMode('train')">1. Initialize Training</button>
                <button class="cyber-btn" onclick="attemptVerify()">2. Verify Identity</button>
                <button class="cyber-btn btn-bot" onclick="attemptBot()">3. Inject Bot Script</button>
            </div>
        </div>

        <!-- RIGHT PANEL: LOGS -->
        <div class="panel">
            <div class="panel-title">TERMINAL</div>
            <div class="terminal" id="terminal-logs">
                <div class="log-entry"><span class="log-time">SYS</span> <span class="log-info">Ghost-Auth Engine v2.0 Loaded.</span></div>
                <div class="log-entry"><span class="log-time">SYS</span> <span class="log-info">Numpy Accelerators Active.</span></div>
                <div class="log-entry"><span class="log-time">SYS</span> <span class="log-info">Waiting for user enrollment...</span></div>
            </div>
        </div>

    </div>

    <!-- RESULT POPUP -->
    <div id="result-overlay">
        <span id="res-icon" class="res-icon">🔒</span>
        <h1 id="res-title" style="margin: 0; font-family: 'Orbitron'; letter-spacing: 2px;">ACCESS DENIED</h1>
        <p id="res-desc" style="color: #888; margin-top: 5px;">Biometric Mismatch Detected</p>
        
        <div style="margin: 30px 0; position: relative; height: 4px; background: #333; border-radius: 2px;">
            <div id="score-bar" style="width: 0%; height: 100%; background: var(--neon-green); border-radius: 2px; transition: width 1s ease;"></div>
        </div>
        
        <h2 id="res-score" style="font-size: 4rem; margin: 0; font-family: 'Orbitron'; line-height: 1;">0%</h2>
        <div style="font-size: 0.8rem; color: #666; margin-bottom: 30px;">TRUST SCORE</div>
        
        <button class="cyber-btn" onclick="closeResult()">ACKNOWLEDGE</button>
    </div>

    <script>
        // ... (JS Logic remains mostly same, just updating UI classes)
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
        for(let i=0; i<30; i++){
            let d = document.createElement('div');
            d.className = 'bar';
            visualizer.appendChild(d);
        }

        function log(msg, type='info') {
            const now = new Date();
            const timeStr = now.toLocaleTimeString([], {hour12: false});
            const div = document.createElement('div');
            div.className = 'log-entry';
            let colorClass = type === 'warn' ? 'log-warn' : (type === 'success' ? 'log-success' : 'log-info');
            div.innerHTML = `<span class="log-time">${timeStr}</span> <span class="${colorClass}">${msg}</span>`;
            term.prepend(div);
        }

        function setMode(m) {
            mode = m;
            resetUI();
            if (m === 'train') {
                modeDisplay.innerText = ">> MODE: TRAINING SEQUENCE";
                modeDisplay.style.color = "var(--neon-blue)";
                inputBox.placeholder = "TYPE THE PHRASE...";
                log("Training Sequence Initiated.", "info");
            } else if (m === 'verify') {
                modeDisplay.innerText = ">> MODE: IDENTITY VERIFICATION";
                modeDisplay.style.color = "var(--neon-green)";
                inputBox.placeholder = "PROVE YOUR IDENTITY...";
                log("Verification Sensors Active.", "success");
            }
        }

        function attemptVerify() {
            if(!isModelTrained) { alert("⚠️ ERROR: Model Untrained. Run Step 1."); return; }
            setMode('verify');
        }

        function attemptBot() {
            if(!isModelTrained) { alert("⚠️ ERROR: Model Untrained. Run Step 1."); return; }
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
            document.querySelectorAll('.bar').forEach(b => {
                b.style.height = '4px';
                b.style.background = 'var(--neon-blue)';
                b.style.boxShadow = '0 0 10px rgba(0,243,255,0.5)';
            });
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
                log("Input sequence complete. analyzing...", "info");
                processData();
            }
        });

        function updateVis(val) {
            const bars = document.querySelectorAll('.bar');
            for(let i=0; i<bars.length-1; i++) {
                bars[i].style.height = bars[i+1].style.height;
                bars[i].style.boxShadow = bars[i+1].style.boxShadow;
                bars[i].style.background = bars[i+1].style.background;
            }
            let last = bars[bars.length-1];
            let h = Math.min(val * 1.5, 70);
            last.style.height = Math.max(h, 4) + 'px';
            
            let color = mode === 'bot' ? 'var(--neon-pink)' : 'var(--neon-blue)';
            last.style.background = color;
            last.style.boxShadow = `0 0 15px ${color}`;
        }

        async function processData() {
            if(inputBox.value !== phrase) {
                log("ERROR: Phrase Mismatch detected.", "warn");
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
                modelStatus.style.textShadow = "0 0 10px var(--neon-green)";
                document.getElementById('flight-count').innerText = data.details.flight_points;
                document.getElementById('dwell-count').innerText = data.details.hold_points;
                log("Biometric Profile Created Successfully.", "success");
                alert("✅ TRAINING COMPLETE.\\nNow click '2. Verify Identity' to test.");
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
            const icon = document.getElementById('res-icon');
            const bar = document.getElementById('score-bar');

            overlay.classList.add('active');
            overlay.style.display = 'block';
            
            if(data.status === 'verified') {
                title.innerText = "ACCESS GRANTED";
                title.style.color = "var(--neon-green)";
                overlay.style.borderColor = "var(--neon-green)";
                overlay.style.boxShadow = "0 0 50px rgba(0, 255, 157, 0.2)";
                score.style.color = "var(--neon-green)";
                icon.innerText = "🔓";
                bar.style.background = "var(--neon-green)";
                log(`Identity Verified. Trust Score: ${data.score}%`, "success");
            } else {
                title.innerText = "ACCESS DENIED";
                title.style.color = "var(--neon-pink)";
                overlay.style.borderColor = "var(--neon-pink)";
                overlay.style.boxShadow = "0 0 50px rgba(255, 0, 85, 0.2)";
                score.style.color = "var(--neon-pink)";
                icon.innerText = "🛡️";
                bar.style.background = "var(--neon-pink)";
                log(`Security Alert: ${data.reason}`, "warn");
            }
            desc.innerText = data.reason || "Biometric Match Confirmed";
            score.innerText = data.score + "%";
            
            // Animate bar
            setTimeout(() => {
                bar.style.width = data.score + "%";
            }, 100);
        }

        function closeResult() {
            const overlay = document.getElementById('result-overlay');
            overlay.classList.remove('active');
            setTimeout(() => {
                overlay.style.display = 'none';
                document.getElementById('score-bar').style.width = '0%';
            }, 300);
            resetUI();
        }

        function simulateBot() {
            mode = 'bot';
            resetUI();
            modeDisplay.innerText = ">> ALERT: BOT SCRIPT DETECTED";
            modeDisplay.style.color = "var(--neon-pink)";
            log("WARNING: Automated Script Injection detected...", "warn");
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
        
        # Compare Patterns (More Forgiving: Score = 100 - (Diff / 2))
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
        
        elif final_score > 45: # Relaxed threshold for humans
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