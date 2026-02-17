import json
import time
import os
import sys

# --- TRY IMPORTING MODULES WITH FRIENDLY ERRORS ---


try:
    import numpy as np
    from flask import Flask, render_template_string, request, jsonify
except ImportError as e:
    print("\n" + "="*50)
    print(f"❌ ERROR: Missing Library - {e.name}")
    print("Please run this command to install requirements:")
    print("pip install flask numpy")
    print("="*50 + "\n")
    sys.exit(1)

# 👇 He try block baher add kar
from biometric_project import FingerprintAuth

fingerprint = FingerprintAuth()



# --- CONFIGURATION ---
app = Flask(__name__)
# Testing sathi password soppa kela ahe
TARGET_PHRASE = "hello ghost"

# --- HTML/CSS/JS UI (BIO-TRUST DASHBOARD) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BIO-TRUST | The Invisible Shield</title>
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-dark: #020408;
            --panel-bg: rgba(10, 25, 40, 0.85);
            --primary: #00f3ff;     /* Cyan */
            --success: #00ff9d;     /* Green */
            --danger: #ff0055;      /* Red */
            --text-main: #e0faff;
            --border: 1px solid rgba(0, 243, 255, 0.3);
        }
        
        * { box-sizing: border-box; }

        body {
            margin: 0;
            height: 100vh;
            background-color: var(--bg-dark);
            font-family: 'Rajdhani', sans-serif;
            color: var(--text-main);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        /* --- BACKGROUND MESH --- */
        .bg-mesh {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                linear-gradient(rgba(0, 243, 255, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 243, 255, 0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            z-index: -1;
            animation: panGrid 60s linear infinite;
        }
        @keyframes panGrid { 0% { transform: translate(0,0); } 100% { transform: translate(-40px, -40px); } }

        /* --- HEADER --- */
        header {
            height: 60px;
            border-bottom: var(--border);
            display: flex; justify-content: space-between; align-items: center;
            padding: 0 30px;
            background: rgba(0,0,0,0.9);
            z-index: 10;
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.1);
        }
        .brand { font-family: 'Share Tech Mono'; font-size: 1.5rem; letter-spacing: 2px; color: var(--primary); text-shadow: 0 0 10px var(--primary); }
        .sys-status { font-size: 0.8rem; color: var(--success); }

        /* --- DASHBOARD GRID --- */
        .dashboard {
            display: grid;
            grid-template-columns: 320px 1fr 320px;
            height: calc(100vh - 60px);
            gap: 20px;
            padding: 20px;
        }

        .panel {
            background: var(--panel-bg);
            border: var(--border);
            border-radius: 12px;
            backdrop-filter: blur(10px);
            padding: 20px;
            display: flex; flex-direction: column;
            overflow: hidden;
            position: relative;
            box-shadow: 0 0 30px rgba(0,0,0,0.5);
        }
        .panel h3 { margin: 0 0 15px 0; color: var(--primary); font-size: 1.1rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px; font-family: 'Share Tech Mono'; }

        /* --- LEFT PANEL: STATS --- */
        .stat-card {
            background: rgba(0, 243, 255, 0.05);
            margin-bottom: 15px; padding: 15px;
            border-left: 4px solid var(--primary);
            border-radius: 4px;
        }
        .stat-val { font-size: 1.5rem; font-family: 'Share Tech Mono'; font-weight: bold; }
        .stat-label { font-size: 0.8rem; color: #aaa; letter-spacing: 1px; }

        /* --- CENTER PANEL: AUTHENTICATION --- */
        .auth-container {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100%; position: relative;
        }

        /* Shield Animation */
        .shield-ring {
            width: 260px; height: 260px;
            border: 2px dashed var(--primary);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            margin-bottom: 30px;
            position: relative;
            animation: spinShield 20s linear infinite;
            box-shadow: 0 0 40px rgba(0, 243, 255, 0.2);
            transition: 0.5s;
        }
        .shield-core {
            width: 180px; height: 180px;
            background: url('https://api.dicebear.com/7.x/bottts/svg?seed=Shield') center/cover;
            border-radius: 50%;
            filter: drop-shadow(0 0 15px var(--primary));
            animation: pulseCore 2s infinite;
        }
        @keyframes spinShield { 100% { transform: rotate(360deg); } }
        @keyframes pulseCore { 0% { transform: scale(0.95); opacity: 0.8; } 50% { transform: scale(1); opacity: 1; } 100% { transform: scale(0.95); opacity: 0.8; } }

        /* Input */
        .input-group { width: 100%; max-width: 500px; position: relative; }
        input {
            width: 100%; padding: 20px;
            background: rgba(0,0,0,0.6);
            border: 2px solid var(--primary);
            border-radius: 50px;
            color: #fff; font-size: 1.5rem; font-family: 'Share Tech Mono';
            text-align: center; outline: none; letter-spacing: 3px;
            box-shadow: 0 0 30px rgba(0, 243, 255, 0.15);
            transition: 0.3s;
        }
        input:focus { box-shadow: 0 0 50px rgba(0, 243, 255, 0.4); transform: scale(1.02); }

        /* Controls */
        .controls { display: flex; gap: 20px; margin-top: 30px; }
        .btn {
            padding: 12px 30px;
            background: rgba(0, 243, 255, 0.1);
            border: 1px solid var(--primary);
            color: var(--primary);
            font-family: 'Rajdhani'; font-weight: 700; letter-spacing: 1px;
            cursor: pointer; transition: 0.3s;
            clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
        }
        .btn:hover, .btn.active { background: var(--primary); color: #000; box-shadow: 0 0 20px var(--primary); }
        .btn-hack { border-color: var(--danger); color: var(--danger); background: rgba(255,0,85,0.1); }
        .btn-hack:hover { background: var(--danger); color: #fff; box-shadow: 0 0 20px var(--danger); }

        /* --- RIGHT PANEL: LIVE LOGS --- */
        .log-terminal {
            font-family: 'Share Tech Mono'; font-size: 0.75rem; color: #aaa;
            overflow-y: auto; height: 100%; padding-right: 5px;
        }
        .log-entry { margin-bottom: 5px; border-bottom: 1px solid rgba(255,255,255,0.05); padding: 4px 0; }
        .log-time { color: var(--primary); margin-right: 5px; font-weight: bold; }
        .log-warn { color: var(--danger); }
        .log-success { color: var(--success); }

        /* --- OVERLAY: VAULT --- */
        #vault-screen {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(2, 4, 8, 0.98); z-index: 100;
            display: none; flex-direction: column; align-items: center; justify-content: center;
            animation: fadeIn 0.5s ease;
        }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        .folder-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; margin-top: 50px; }
        .folder {
            border: 1px solid var(--success); padding: 30px; text-align: center;
            background: rgba(0, 255, 157, 0.05); cursor: pointer; transition: 0.3s;
            border-radius: 10px;
        }
        .folder:hover { background: var(--success); color: #000; box-shadow: 0 0 40px var(--success); transform: translateY(-5px); }

        /* --- OVERLAY: BOT DETECTED --- */
        #bot-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255, 0, 0, 0.2); z-index: 200;
            display: none; flex-direction: column; align-items: center; justify-content: center;
            backdrop-filter: blur(5px);
        }
        .bot-msg {
            font-size: 4rem; color: var(--danger); font-family: 'Share Tech Mono';
            text-shadow: 0 0 30px var(--danger);
            animation: blinkFast 0.5s infinite;
            background: rgba(0,0,0,0.8); padding: 20px; border: 2px solid var(--danger);
        }
        @keyframes blinkFast { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

        /* Glitch Animation */
        .glitch-anim { animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both; border-color: var(--danger) !important; box-shadow: 0 0 30px var(--danger) !important; }
        @keyframes shake { 10%, 90% { transform: translate3d(-1px, 0, 0); } 20%, 80% { transform: translate3d(2px, 0, 0); } 30%, 50%, 70% { transform: translate3d(-4px, 0, 0); } 40%, 60% { transform: translate3d(4px, 0, 0); } }

    </style>
</head>
<body>

    <div class="bg-mesh"></div>

    <header>
        <div class="brand">BIO-TRUST <span style="font-size:0.8rem; color:#888;">// THE INVISIBLE SHIELD</span></div>
        <div class="sys-status">SYSTEM SECURE ●</div>
    </header>

    <div class="dashboard">
        
        <!-- LEFT PANEL -->
        <div class="panel">
            <h3>THREAT INTELLIGENCE</h3>
            <div class="stat-card">
                <div class="stat-label">THREAT LEVEL</div>
                <div class="stat-val" id="threat-level" style="color:var(--success)">LOW</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">ACTIVE SESSIONS</div>
                <div class="stat-val">1</div>
            </div>
            
            <h3>BIOMETRIC TELEMETRY</h3>
            <canvas id="rhythmChart" height="150"></canvas>
        </div>

        <!-- CENTER PANEL -->
        <div class="panel">
            <div class="auth-container" id="auth-ui">
                <div class="shield-ring" id="shield-ring">
                    <div class="shield-core"></div>
                </div>
                
                <h1 style="margin:0 0 10px 0; letter-spacing:3px; text-shadow:0 0 20px var(--primary);">AUTHENTICATION</h1>
                <div id="instruction" style="color:#888; margin-bottom:30px; letter-spacing:1px; font-weight:bold;">VERIFY IDENTITY TO ACCESS VAULT</div>

                <div class="input-group">
                    <input type="text" id="password-input" placeholder="ENTER PASSPHRASE" autocomplete="off">
                </div>

                <div class="controls">
                    <button class="btn active" id="btn-train" onclick="setMode('train')">ENROLL ID</button>
                    <button class="btn" id="btn-verify" onclick="setMode('verify')">VERIFY</button>
                    <button class="btn btn-hack" onclick="simulateHack()">SIMULATE FRAUD</button>
                </div>
            </div>
        </div>

        <!-- RIGHT PANEL -->
        <div class="panel">
            <h3>REAL-TIME ANALYSIS LOGS</h3>
            <div class="log-terminal" id="terminal">
                <div class="log-entry"><span class="log-time">SYS</span> Initializing Bio-Trust Engine...</div>
                <div class="log-entry"><span class="log-time">SYS</span> Numpy Vectors Loaded.</div>
                <div class="log-entry"><span class="log-time">SYS</span> Ready for input.</div>
            </div>
        </div>

    </div>

    <!-- SECRET VAULT -->
    <div id="vault-screen">
        <h1 style="color:var(--success); font-size:3rem; text-shadow:0 0 30px var(--success);">ACCESS GRANTED</h1>
        <p style="letter-spacing:3px; font-family: 'Share Tech Mono';">WELCOME TO THE SECURE MAINFRAME</p>
        
        <div class="folder-grid">
            <div class="folder">
                <div style="font-size:3rem;">☢️</div>
                <div style="margin-top:10px; font-weight:bold;">LAUNCH CODES</div>
            </div>
            <div class="folder">
                <div style="font-size:3rem;">₿</div>
                <div style="margin-top:10px; font-weight:bold;">CRYPTO WALLET</div>
            </div>
            <div class="folder">
                <div style="font-size:3rem;">📂</div>
                <div style="margin-top:10px; font-weight:bold;">CLASSIFIED FILES</div>
            </div>
        </div>
        <button class="btn btn-hack" style="margin-top:50px;" onclick="location.reload()">LOCK TERMINAL</button>
    </div>

    <!-- BOT DETECTED OVERLAY -->
    <div id="bot-overlay">
        <div class="bot-msg">⚠️ SYSTEM BREACH DETECTED</div>
        <p style="color:white; font-size:1.5rem; margin-top:20px;">ROBOTIC BEHAVIOR IDENTIFIED</p>
        <button class="btn" style="margin-top:30px;" onclick="location.reload()">REBOOT SYSTEM</button>
    </div>

    <script>
        // --- CHART SETUP ---
        const ctx = document.getElementById('rhythmChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['1', '2', '3', '4', '5', '6'],
                datasets: [{
                    label: 'Typing Rhythm (ms)',
                    data: [0, 0, 0, 0, 0, 0],
                    borderColor: '#00f3ff',
                    backgroundColor: 'rgba(0, 243, 255, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 2
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { x: { display: false }, y: { display: false, min: 0 } },
                animation: { duration: 200 }
            }
        });

        // --- APP LOGIC ---
        let mode = 'train';
        let flightTimes = [];
        let holdTimes = [];
        let keyDownMap = {};
        let lastKeyUpTime = 0;
        let phrase = "{{ phrase }}";
        let isModelTrained = false;

        const pwdInput = document.getElementById('password-input');
        const terminal = document.getElementById('terminal');
        const shieldRing = document.getElementById('shield-ring');
        const threatLevel = document.getElementById('threat-level');
        const vaultScreen = document.getElementById('vault-screen');
        const instruction = document.getElementById('instruction');
        const botOverlay = document.getElementById('bot-overlay');

        pwdInput.placeholder = `TYPE: "${phrase}"`;

        function log(msg, type='info') {
            const div = document.createElement('div');
            div.className = 'log-entry';
            let colorClass = type === 'warn' ? 'log-warn' : (type === 'success' ? 'log-success' : '');
            div.innerHTML = `<span class="log-time">${new Date().toLocaleTimeString().split(' ')[0]}</span> <span class="${colorClass}">${msg}</span>`;
            terminal.prepend(div);
        }

        function setMode(m) {
            if (m !== 'train' && !isModelTrained) {
                alert("⚠️ MODEL NOT TRAINED! Please Enroll First.");
                setMode('train');
                return;
            }
            mode = m;
            resetUI();
            
            document.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
            if(m === 'train') {
                document.getElementById('btn-train').classList.add('active');
                instruction.innerText = "TRAINING MODE: TYPE NATURALLY TO CREATE DIGITAL DNA";
                instruction.style.color = "var(--primary)";
                pwdInput.placeholder = `ENROLL: "${phrase}"`;
                shieldRing.style.borderColor = "var(--primary)";
                shieldRing.style.boxShadow = "0 0 30px rgba(0, 243, 255, 0.1)";
            } else {
                document.getElementById('btn-verify').classList.add('active');
                instruction.innerText = "SECURITY MODE: VERIFY IDENTITY";
                instruction.style.color = "#fff";
                pwdInput.placeholder = "ENTER PASSPHRASE";
            }
        }

        function resetUI() {
            pwdInput.value = '';
            pwdInput.disabled = false;
            flightTimes = [];
            holdTimes = [];
            keyDownMap = {};
            lastKeyUpTime = 0;
            pwdInput.focus();
            pwdInput.style.borderColor = "var(--primary)";
            pwdInput.classList.remove('glitch-anim');
            shieldRing.style.borderColor = "var(--primary)";
            shieldRing.style.boxShadow = "0 0 30px rgba(0, 243, 255, 0.1)";
            threatLevel.innerText = "LOW";
            threatLevel.style.color = "var(--success)";
        }

        // --- KEYSTROKE CAPTURE ---
        pwdInput.addEventListener('keydown', e => {
            if(e.key === 'Enter') return;
            if(!keyDownMap[e.code]) keyDownMap[e.code] = Date.now();
        });

        pwdInput.addEventListener('keyup', e => {
            let now = Date.now();
            let hold = 0, flight = 0;

            if(keyDownMap[e.code]) {
                hold = now - keyDownMap[e.code];
                holdTimes.push(hold);
                delete keyDownMap[e.code];
                log(`Keystroke Pressure: ${hold}ms`);
            }
            if(lastKeyUpTime !== 0) {
                flight = now - lastKeyUpTime;
                flightTimes.push(flight);
                log(`Flight Latency: ${flight}ms`);
                
                // Update Chart Live
                chart.data.datasets[0].data.shift();
                chart.data.datasets[0].data.push(flight);
                chart.update();
            }
            lastKeyUpTime = now;

            if(pwdInput.value.length >= phrase.length) {
                pwdInput.disabled = true;
                log("Analyzing Vector Pattern...", "info");
                setTimeout(processData, 1000);
            }
        });

        async function processData() {
            if(pwdInput.value !== phrase) {
                log("ERROR: INCORRECT PASSWORD", "warn");
                loginFail("WRONG PASSWORD");
                return;
            }

            try {
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
                    log("✅ DIGITAL DNA CREATED.", "success");
                    alert("TRAINING COMPLETE. SYSTEM ARMED.");
                    setMode('verify');
                } else if (data.status === 'verified') {
                    loginSuccess();
                } else {
                    loginFail(data.reason);
                }
            } catch (error) {
                console.error("Server Error:", error);
                log("SERVER CONNECTION FAILED!", "warn");
                alert("Error connecting to server. Is Python running?");
                pwdInput.disabled = false;
            }
        }

        function loginSuccess() {
            log("ACCESS GRANTED - IDENTITY CONFIRMED", "success");
            instruction.innerText = "ACCESS GRANTED";
            instruction.style.color = "var(--success)";
            pwdInput.style.borderColor = "var(--success)";
            shieldRing.style.borderColor = "var(--success)";
            shieldRing.style.boxShadow = "0 0 50px var(--success)";
            
            setTimeout(() => {
                document.querySelector('.dashboard').style.display = 'none';
                vaultScreen.style.display = 'flex';
            }, 1000);
        }

        function loginFail(reason) {
            // Check if it was a bot detection for special overlay
            if(reason.includes("ROBOTIC")) {
                botOverlay.style.display = 'flex';
                log("CRITICAL THREAT: BOT DETECTED", "warn");
                return;
            }

            log(`SECURITY ALERT: ${reason}`, "warn");
            instruction.innerText = `⛔ DENIED: ${reason}`;
            instruction.style.color = "var(--danger)";
            pwdInput.classList.add('glitch-anim');
            pwdInput.style.borderColor = "var(--danger)";
            shieldRing.style.borderColor = "var(--danger)";
            shieldRing.style.boxShadow = "0 0 50px var(--danger)";
            threatLevel.innerText = "CRITICAL";
            threatLevel.style.color = "var(--danger)";
            
            setTimeout(() => {
                resetUI();
                instruction.innerText = "RETRY AUTHENTICATION";
                instruction.style.color = "#888";
                threatLevel.innerText = "LOW";
                threatLevel.style.color = "var(--success)";
            }, 3000);
        }

        function simulateHack() {
            if(!isModelTrained) { alert("Train first!"); return; }
            setMode('verify');
            mode = 'bot';
            
            log("⚠️ WARNING: BOT SCRIPT INJECTED", "warn");
            pwdInput.disabled = true;
            let chars = phrase.split('');
            let i = 0;
            // Use local variable for data to avoid polluting real user data if interrupted
            flightTimes = [];
            holdTimes = [];
            
            let intv = setInterval(() => {
                if(i < chars.length) {
                    pwdInput.value += chars[i];
                    // Bots have perfect timing (zero variance)
                    let perfectFlight = 50; 
                    flightTimes.push(perfectFlight); 
                    holdTimes.push(80);
                    
                    // Update visuals
                    log(`Bot Keystroke: ${perfectFlight}ms (Suspicious)`);
                    chart.data.datasets[0].data.shift();
                    chart.data.datasets[0].data.push(perfectFlight);
                    chart.update();
                    
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

# --- PYTHON BACKEND LOGIC ---
user_profile = { "trained": False, "flight_avg": [], "hold_avg": [] }

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

    if not flight_times: return jsonify({"status": "error", "message": "No data"})

    if mode == 'train':
        user_profile["flight_avg"] = flight_times
        user_profile["hold_avg"] = hold_times
        user_profile["trained"] = True
        return jsonify({"status": "trained"})

    elif mode == 'verify':
        if not user_profile["trained"]: return jsonify({"status": "denied", "score": 0, "reason": "Untrained"})

        curr_flight = np.array(flight_times)
        ref_flight = np.array(user_profile["flight_avg"])
        
        # Match lengths
        min_len = min(len(curr_flight), len(ref_flight))
        curr_flight = curr_flight[:min_len]
        ref_flight = ref_flight[:min_len]
        
        # Calculate Manhattan Distance (L1 Norm) between vectors
        flight_diff = np.mean(np.abs(curr_flight - ref_flight))
        score = max(0, 100 - flight_diff)
        
        # Bot Detection: Check Variance (Standard Deviation)
        # Humans have variance (shaky hands), Bots have near-zero variance
        flight_var = np.std(curr_flight)
        
        if is_bot or flight_var < 5:
            return jsonify({"status": "denied", "score": 5, "reason": "ROBOTIC BEHAVIOR DETECTED (ZERO VARIANCE)"})
        
        elif score > 50:
            return jsonify({"status": "verified", "score": int(score)})
        else:
            return jsonify({"status": "denied", "score": int(score), "reason": "BEHAVIORAL MISMATCH"})

if __name__ == '__main__':
    # Running on port 5001 to avoid conflicts
    print("🔥 BIO-TRUST SYSTEM ONLINE: http://127.0.0.1:5001")
    app.run(debug=True, port=5001)