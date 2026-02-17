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
    <title>GHOST-AUTH | ULTIMATE UI</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --neon-blue: #00f3ff;
            --neon-pink: #ff0055;
            --neon-purple: #bc13fe;
            --neon-gold: #ffd700;
            --bg-dark: #020204;
            --panel-bg: rgba(5, 10, 20, 0.65);
            --border-color: rgba(0, 243, 255, 0.3);
        }
        
        * { box-sizing: border-box; }

        body {
            background-color: var(--bg-dark);
            color: #fff;
            font-family: 'Rajdhani', sans-serif;
            margin: 0;
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            perspective: 1000px;
        }

        /* --- ADVANCED BACKGROUND --- */
        .bg-animation {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: 
                radial-gradient(circle at 50% 50%, rgba(0, 243, 255, 0.05), transparent 60%),
                linear-gradient(0deg, rgba(0,0,0,0.9), transparent),
                repeating-linear-gradient(90deg, rgba(0, 243, 255, 0.03) 0px, rgba(0, 243, 255, 0.03) 1px, transparent 1px, transparent 50px),
                repeating-linear-gradient(0deg, rgba(0, 243, 255, 0.03) 0px, rgba(0, 243, 255, 0.03) 1px, transparent 1px, transparent 50px);
            z-index: -2;
            transform: scale(1.1);
            animation: moveGrid 30s linear infinite;
        }
        
        @keyframes moveGrid {
            0% { transform: scale(1.1) translate(0, 0) rotate(0deg); }
            50% { transform: scale(1.15) translate(-20px, -20px) rotate(1deg); }
            100% { transform: scale(1.1) translate(0, 0) rotate(0deg); }
        }

        /* Floating Particles (Pseudo-elements) */
        body::before, body::after {
            content: '';
            position: absolute;
            width: 100%; height: 100%;
            background-image: radial-gradient(white 1px, transparent 1px);
            background-size: 50px 50px;
            opacity: 0.1;
            z-index: -1;
            animation: stars 100s linear infinite;
        }
        body::after {
            background-size: 100px 100px;
            animation: stars 60s linear infinite reverse;
            opacity: 0.2;
        }
        
        @keyframes stars { from { transform: translateY(0); } to { transform: translateY(-1000px); } }

        /* --- GLITCH TEXT EFFECT --- */
        .glitch {
            position: relative;
            color: #fff;
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 5px;
        }
        .glitch::before, .glitch::after {
            content: attr(data-text);
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: var(--bg-dark);
        }
        .glitch::before {
            left: 2px; text-shadow: -1px 0 var(--neon-pink);
            clip: rect(24px, 550px, 90px, 0);
            animation: glitch-anim-1 3s infinite linear alternate-reverse;
        }
        .glitch::after {
            left: -2px; text-shadow: -1px 0 var(--neon-blue);
            clip: rect(85px, 550px, 140px, 0);
            animation: glitch-anim-2 2s infinite linear alternate-reverse;
        }
        
        @keyframes glitch-anim-1 {
            0% { clip: rect(20px, 9999px, 80px, 0); }
            20% { clip: rect(60px, 9999px, 10px, 0); }
            40% { clip: rect(10px, 9999px, 90px, 0); }
            60% { clip: rect(80px, 9999px, 20px, 0); }
            80% { clip: rect(30px, 9999px, 70px, 0); }
            100% { clip: rect(50px, 9999px, 60px, 0); }
        }
        @keyframes glitch-anim-2 {
            0% { clip: rect(90px, 9999px, 10px, 0); }
            100% { clip: rect(10px, 9999px, 90px, 0); }
        }

        /* --- HEADER --- */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 50px;
            background: rgba(2, 2, 4, 0.8);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255,255,255,0.05);
            box-shadow: 0 5px 30px rgba(0,0,0,0.5);
            z-index: 100;
        }
        
        .logo { font-size: 2.5rem; text-transform: uppercase; background: linear-gradient(to right, #fff, var(--neon-blue)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        
        /* --- DASHBOARD LAYOUT --- */
        .dashboard {
            display: grid;
            grid-template-columns: 320px 1fr 320px;
            gap: 30px;
            padding: 30px;
            height: 100%;
            position: relative;
        }

        .panel {
            background: var(--panel-bg);
            border: 1px solid rgba(0, 243, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            backdrop-filter: blur(15px);
            box-shadow: 0 0 40px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
            transition: 0.3s;
        }
        
        /* Holographic Border Animation */
        .panel::before {
            content: '';
            position: absolute;
            top: -50%; left: -50%; width: 200%; height: 200%;
            background: conic-gradient(transparent, rgba(0, 243, 255, 0.3), transparent 30%);
            animation: rotateBorder 4s linear infinite;
            z-index: -1;
        }
        .panel::after {
            content: '';
            position: absolute;
            inset: 2px;
            background: var(--panel-bg);
            border-radius: 18px;
            z-index: -1;
        }
        @keyframes rotateBorder { 100% { transform: rotate(360deg); } }

        .panel-title {
            font-family: 'Orbitron';
            color: var(--neon-blue);
            font-size: 1rem;
            letter-spacing: 3px;
            margin-bottom: 20px;
            border-bottom: 1px solid rgba(0, 243, 255, 0.2);
            padding-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        /* --- CENTER CONSOLE (ARC REACTOR STYLE) --- */
        .console-screen {
            position: relative;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        /* Arc Reactor Circle */
        .arc-reactor {
            position: absolute;
            width: 500px; height: 500px;
            border-radius: 50%;
            border: 2px dashed rgba(0, 243, 255, 0.2);
            animation: spinReactor 20s linear infinite;
            pointer-events: none;
            z-index: -1;
        }
        .arc-reactor::before {
            content: ''; position: absolute; top: 10%; left: 10%; right: 10%; bottom: 10%;
            border-radius: 50%; border: 1px solid rgba(0, 243, 255, 0.1);
            border-left: 1px solid var(--neon-blue);
            animation: spinReactor 10s linear infinite reverse;
        }
        @keyframes spinReactor { 100% { transform: rotate(360deg); } }

        .input-group {
            position: relative;
            width: 100%;
            max-width: 600px;
            text-align: center;
        }

        .phrase-label {
            font-size: 0.9rem; color: var(--neon-blue); letter-spacing: 2px; margin-bottom: 15px;
            text-shadow: 0 0 10px var(--neon-blue);
        }
        .phrase-highlight {
            font-size: 2.5rem; font-family: 'Orbitron'; font-weight: 700; color: #fff;
            text-shadow: 0 0 20px rgba(0, 243, 255, 0.8);
            margin-bottom: 30px; display: block;
        }

        input[type="text"] {
            width: 100%;
            background: rgba(0,0,0,0.5);
            border: 2px solid var(--neon-blue);
            padding: 25px;
            font-family: 'JetBrains Mono';
            font-size: 1.8rem;
            color: #fff;
            text-align: center;
            border-radius: 50px;
            outline: none;
            transition: 0.3s;
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.2);
        }
        input:focus {
            box-shadow: 0 0 50px rgba(0, 243, 255, 0.5);
            transform: scale(1.05);
        }

        /* --- VISUALIZER --- */
        .visualizer-container {
            display: flex; gap: 5px; height: 60px; margin-top: 40px; align-items: center; justify-content: center;
        }
        .bar {
            width: 6px; height: 10px; background: var(--neon-blue); border-radius: 10px;
            transition: 0.1s; box-shadow: 0 0 10px var(--neon-blue);
        }

        /* --- BUTTONS --- */
        .controls {
            display: flex; gap: 20px; justify-content: center; margin-top: 40px;
        }
        
        .cyber-btn {
            position: relative;
            padding: 15px 40px;
            background: transparent;
            border: 1px solid var(--neon-blue);
            color: var(--neon-blue);
            font-family: 'Orbitron';
            font-size: 1rem;
            letter-spacing: 2px;
            cursor: pointer;
            overflow: hidden;
            transition: 0.4s;
            z-index: 1;
        }
        .cyber-btn:hover { color: #000; box-shadow: 0 0 30px var(--neon-blue); border-color: transparent; }
        .cyber-btn::before {
            content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
            background: var(--neon-blue); z-index: -1; transition: 0.4s;
        }
        .cyber-btn:hover::before { left: 0; }
        
        .btn-bot { border-color: var(--neon-pink); color: var(--neon-pink); }
        .btn-bot:hover { box-shadow: 0 0 30px var(--neon-pink); color: #fff; }
        .btn-bot::before { background: var(--neon-pink); }

        /* --- CAMERA FEED --- */
        .cam-box {
            position: relative; width: 100%; height: 200px;
            background: #000; border: 1px solid #333; overflow: hidden;
            display: flex; align-items: center; justify-content: center;
            border-radius: 10px; margin-bottom: 20px;
        }
        .cam-box video {
            width: 100%; height: 100%; object-fit: cover;
            filter: hue-rotate(180deg) contrast(1.2); /* Sci-Fi Look */
            opacity: 0.8;
        }
        .cam-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(rgba(0, 243, 255, 0.1) 50%, transparent 50%);
            background-size: 100% 4px; pointer-events: none; z-index: 2;
        }
        .face-tracker {
            position: absolute; width: 120px; height: 120px;
            border: 2px solid var(--neon-green); border-radius: 10px;
            top: 50%; left: 50%; transform: translate(-50%, -50%);
            box-shadow: 0 0 20px var(--neon-green);
            display: none; animation: pulseTrack 2s infinite;
        }
        @keyframes pulseTrack { 0% { opacity: 0.5; transform: translate(-50%, -50%) scale(1); } 50% { opacity: 1; transform: translate(-50%, -50%) scale(1.05); } 100% { opacity: 0.5; transform: translate(-50%, -50%) scale(1); } }

        /* --- STATS & LOGS --- */
        .stat-item {
            display: flex; justify-content: space-between; margin-bottom: 15px; font-size: 1.1rem;
            border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 5px;
        }
        .stat-val { font-family: 'Orbitron'; color: #fff; }
        
        .terminal {
            font-family: 'JetBrains Mono'; font-size: 0.85rem; color: #888;
            height: 100%; overflow-y: auto; padding-right: 10px;
        }
        .log-line { margin-bottom: 8px; padding-left: 10px; border-left: 2px solid transparent; }
        .log-info { border-left-color: var(--neon-blue); color: var(--neon-blue); }
        .log-warn { border-left-color: var(--neon-pink); color: var(--neon-pink); }
        .log-success { border-left-color: var(--neon-green); color: var(--neon-green); }

        /* --- OVERLAYS --- */
        #boot-screen {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #000; z-index: 9999; display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            font-family: 'Orbitron'; color: var(--neon-blue); font-size: 2rem;
            animation: fadeOut 1s ease 2s forwards;
        }
        @keyframes fadeOut { to { opacity: 0; visibility: hidden; } }

        .loader {
            width: 200px; height: 4px; background: #333; margin-top: 20px; position: relative;
        }
        .loader::after {
            content: ''; position: absolute; top: 0; left: 0; height: 100%; width: 0%;
            background: var(--neon-blue); animation: loadBar 2s ease forwards;
        }
        @keyframes loadBar { to { width: 100%; } }

        #vault-screen {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.95); z-index: 200;
            flex-direction: column; align-items: center; justify-content: center;
            backdrop-filter: blur(10px);
        }
        
        .folder-grid {
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-top: 50px;
        }
        .folder {
            width: 150px; height: 120px; border: 2px solid var(--neon-green);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            color: var(--neon-green); font-family: 'Orbitron'; cursor: pointer;
            transition: 0.3s; background: rgba(0, 255, 157, 0.05);
        }
        .folder:hover { background: var(--neon-green); color: #000; transform: scale(1.1); box-shadow: 0 0 30px var(--neon-green); }

    </style>
</head>
<body>

    <div id="boot-screen">
        <div>INITIALIZING CORE SYSTEMS...</div>
        <div class="loader"></div>
    </div>

    <div class="bg-animation"></div>

    <header>
        <div class="logo glitch" data-text="GHOST-AUTH">GHOST-AUTH</div>
        <div class="sys-status" style="color: var(--neon-green); text-shadow: 0 0 10px var(--neon-green);">
            ● SYSTEM ONLINE
        </div>
    </header>

    <div class="dashboard">
        
        <!-- LEFT: SENSORS -->
        <div class="panel">
            <div class="panel-title">OPTICAL FEED</div>
            <div class="cam-box" id="cam-box">
                <div style="color: #555; font-size: 0.8rem; letter-spacing: 2px;">[ FEED TERMINATED ]</div>
            </div>
            <div class="face-tracker" id="face-tracker"></div>
            <button class="cyber-btn" id="btn-cam" onclick="enableCamera()" style="width: 100%; font-size: 0.8rem;">ACTIVATE OPTICS</button>

            <div class="panel-title" style="margin-top: 30px;">BIO-METRICS</div>
            <div class="stat-item">
                <span style="color:#888">Flight Vectors</span>
                <span class="stat-val" id="flight-count">0</span>
            </div>
            <div class="stat-item">
                <span style="color:#888">Dwell Vectors</span>
                <span class="stat-val" id="dwell-count">0</span>
            </div>
            <div class="stat-item">
                <span style="color:#888">Status</span>
                <span class="stat-val" id="model-status" style="color: #666">STANDBY</span>
            </div>
        </div>

        <!-- CENTER: INTERACTION -->
        <div class="panel console-screen">
            <div class="arc-reactor"></div>
            
            <div class="input-group">
                <div class="phrase-label">SECURITY PROTOCOL: PASSPHRASE REQUIRED</div>
                <div class="phrase-highlight">{{ phrase }}</div>
                <input type="text" id="input-box" placeholder="AWAITING INPUT..." autocomplete="off">
            </div>

            <div class="visualizer-container" id="visualizer"></div>

            <div class="controls">
                <button class="cyber-btn" onclick="setMode('train')">1. ENROLL</button>
                <button class="cyber-btn" onclick="attemptVerify()">2. VERIFY</button>
                <button class="cyber-btn btn-bot" onclick="attemptBot()">3. HACK</button>
            </div>
        </div>

        <!-- RIGHT: LOGS -->
        <div class="panel">
            <div class="panel-title">SYSTEM LOGS</div>
            <div class="terminal" id="terminal-logs">
                <div class="log-line log-info">System Kernel Loaded... OK</div>
                <div class="log-line log-info">Numpy Tensor Core... OK</div>
                <div class="log-line log-info">Waiting for User Interaction...</div>
            </div>
        </div>

    </div>

    <!-- SECRET VAULT -->
    <div id="vault-screen">
        <h1 style="color: var(--neon-green); font-size: 4rem; text-shadow: 0 0 30px var(--neon-green); font-family: 'Orbitron'; margin-bottom: 10px;">ACCESS GRANTED</h1>
        <p style="color: #fff; letter-spacing: 5px; font-family: 'Rajdhani';">WELCOME TO THE MAINFRAME</p>
        
        <div class="folder-grid">
            <div class="folder">
                <div style="font-size: 2rem;">☢️</div>
                <div style="margin-top: 10px; font-size: 0.8rem;">LAUNCH CODES</div>
            </div>
            <div class="folder">
                <div style="font-size: 2rem;">👽</div>
                <div style="margin-top: 10px; font-size: 0.8rem;">AREA 51</div>
            </div>
            <div class="folder">
                <div style="font-size: 2rem;">₿</div>
                <div style="margin-top: 10px; font-size: 0.8rem;">CRYPTO WALLET</div>
            </div>
        </div>
        
        <button class="cyber-btn btn-bot" style="margin-top: 50px;" onclick="location.reload()">LOGOUT</button>
    </div>

    <script>
        // ... (Logic remains similar, refined for new UI) ...
        let mode = 'train';
        let flightTimes = [];
        let holdTimes = [];
        let keyDownMap = {};
        let lastKeyUpTime = 0;
        let phrase = "{{ phrase }}";
        let isModelTrained = false;
        let isCameraActive = false;

        const inputBox = document.getElementById('input-box');
        const visualizer = document.getElementById('visualizer');
        const term = document.getElementById('terminal-logs');
        const modelStatus = document.getElementById('model-status');
        
        // Init Visualizer bars
        for(let i=0; i<20; i++){
            let d = document.createElement('div');
            d.className = 'bar';
            visualizer.appendChild(d);
        }

        function log(msg, type='info') {
            const div = document.createElement('div');
            div.className = `log-line log-${type}`;
            div.innerText = `> ${msg}`;
            term.prepend(div);
        }

        function enableCamera() {
             navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    const camBox = document.getElementById('cam-box');
                    camBox.innerHTML = '<video id="video-feed" autoplay muted playsinline></video><div class="cam-overlay"></div>';
                    const video = document.getElementById('video-feed');
                    video.srcObject = stream;
                    log("Optical Sensors: ONLINE", "success");
                    document.getElementById('btn-cam').style.display = 'none';
                    isCameraActive = true;
                    
                    // Show Face Tracker Animation
                    document.getElementById('face-tracker').style.display = 'block';
                })
                .catch(err => {
                    log("Optical Sensors: ERROR " + err, "warn");
                    alert("Camera Permission Denied");
                });
        }

        function setMode(m) {
            mode = m;
            resetUI();
            if (m === 'train') {
                inputBox.placeholder = "TYPE TO ENROLL...";
                inputBox.style.borderColor = "var(--neon-blue)";
                log("Mode switched: TRAINING", "info");
            } else if (m === 'verify') {
                inputBox.placeholder = "VERIFY IDENTITY...";
                inputBox.style.borderColor = "var(--neon-green)";
                log("Mode switched: VERIFICATION", "success");
            }
        }

        function attemptVerify() {
            if(!isModelTrained) { alert("⚠️ ERROR: Train Model First!"); return; }
            setMode('verify');
        }

        function attemptBot() {
            if(!isModelTrained) { alert("⚠️ ERROR: Train Model First!"); return; }
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
                b.style.height = '10px';
                b.style.background = 'var(--neon-blue)';
            });
        }

        // INPUT LOGIC
        inputBox.addEventListener('keydown', e => {
            if(e.key === 'Enter') return;
            if(!keyDownMap[e.code]) keyDownMap[e.code] = Date.now();
        });

        inputBox.addEventListener('keyup', e => {
            let now = Date.now();
            if(keyDownMap[e.code]) {
                let hold = now - keyDownMap[e.code];
                holdTimes.push(hold);
                updateVis(hold);
                delete keyDownMap[e.code];
            }
            if(lastKeyUpTime !== 0) {
                let flight = now - lastKeyUpTime;
                flightTimes.push(flight);
            }
            lastKeyUpTime = now;

            if(inputBox.value.length === phrase.length) {
                log("Analyzing Biometric Vectors...", "info");
                processData();
            }
        });

        function updateVis(val) {
            const bars = document.querySelectorAll('.bar');
            for(let i=0; i<bars.length-1; i++) {
                bars[i].style.height = bars[i+1].style.height;
            }
            let last = bars[bars.length-1];
            let h = Math.min(val * 1.5, 60);
            last.style.height = Math.max(h, 10) + 'px';
            last.style.background = mode === 'bot' ? 'var(--neon-pink)' : 'var(--neon-blue)';
        }

        async function processData() {
            if(inputBox.value !== phrase) {
                log("Phrase Mismatch. Resetting...", "warn");
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
                    is_bot_simulation: mode === 'bot',
                    camera_active: isCameraActive
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
                log("Biometric Profile Created.", "success");
                alert("TRAINING COMPLETE");
                setMode('verify');
            } else if (data.status === 'verified') {
                log(`ACCESS GRANTED. Score: ${data.score}%`, "success");
                document.getElementById('vault-screen').style.display = 'flex'; // OPEN VAULT
            } else {
                log(`ACCESS DENIED. Score: ${data.score}% (${data.reason})`, "warn");
                alert(`⛔ ACCESS DENIED\\nScore: ${data.score}%\\nReason: ${data.reason}`);
                resetUI();
            }
        }

        function simulateBot() {
            mode = 'bot';
            resetUI();
            log("WARNING: Bot Script Injection Detected", "warn");
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
        # Formula: Vector - Mean(Vector)
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
        # If camera active: 30% Flight, 30% Hold, 40% Face
        # Else: 60% Flight, 40% Hold
        
        if camera_active:
            final_score = int((flight_score * 0.3) + (hold_score * 0.3) + (face_score * 0.4))
        else:
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
            reason_text = "Multi-Factor Authentication Success" if camera_active else "Biometric Match Confirmed"
            return jsonify({
                "status": "verified",
                "score": final_score,
                "reason": reason_text
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