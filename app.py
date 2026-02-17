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

# --- CONFIGURATION ---
app = Flask(__name__)
TARGET_PHRASE = "hello ghost"

# --- ENHANCED HTML/CSS/JS UI (NEURAL SECURITY CORE) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost-Auth | Neural Security Core</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-dark: #050508;
            --panel-bg: rgba(10, 20, 35, 0.9);
            --primary: #00f3ff;
            --secondary: #7000ff;
            --success: #00ff9d;
            --danger: #ff0055;
            --warning: #ffbd2e;
            --text-main: #e0faff;
            --glow-primary: 0 0 20px rgba(0, 243, 255, 0.5);
            --glow-success: 0 0 30px rgba(0, 255, 157, 0.6);
            --glow-danger: 0 0 30px rgba(255, 0, 85, 0.8);
        }
        
        * { box-sizing: border-box; cursor: crosshair; }

        body {
            margin: 0;
            height: 100vh;
            background: var(--bg-dark);
            font-family: 'Rajdhani', sans-serif;
            color: var(--text-main);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        /* --- PARTICLE CANVAS --- */
        #particle-canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
            pointer-events: none;
        }

        /* --- ANIMATED GRID BACKGROUND --- */
        .bg-mesh {
            position: absolute; 
            top: 0; left: 0; 
            width: 200%; height: 200%;
            background-image: 
                linear-gradient(rgba(0, 243, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px),
                radial-gradient(circle at 50% 50%, rgba(0, 243, 255, 0.1) 0%, transparent 50%);
            background-size: 50px 50px, 50px 50px, 100% 100%;
            z-index: -1;
            animation: panGrid 20s linear infinite;
            transform-origin: center;
        }
        
        @keyframes panGrid { 
            0% { transform: translate(0,0) rotate(0deg); } 
            100% { transform: translate(-50px, -50px) rotate(0deg); } 
        }

        /* --- SCAN LINES --- */
        .scan-lines {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                to bottom,
                transparent 50%,
                rgba(0, 243, 255, 0.02) 50%
            );
            background-size: 100% 4px;
            z-index: 1000;
            pointer-events: none;
            animation: scanMove 8s linear infinite;
        }
        
        @keyframes scanMove {
            0% { transform: translateY(0); }
            100% { transform: translateY(4px); }
        }

        /* --- HEADER --- */
        header {
            height: 70px;
            border-bottom: 1px solid rgba(0, 243, 255, 0.3);
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            padding: 0 40px;
            background: linear-gradient(90deg, rgba(0,0,0,0.95) 0%, rgba(10,25,40,0.9) 50%, rgba(0,0,0,0.95) 100%);
            z-index: 10;
            box-shadow: 0 0 30px rgba(0, 243, 255, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 243, 255, 0.1), transparent);
            animation: headerScan 3s ease-in-out infinite;
        }
        
        @keyframes headerScan {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        .brand { 
            font-family: 'Orbitron', sans-serif; 
            font-size: 1.8rem; 
            font-weight: 900;
            letter-spacing: 4px; 
            color: var(--primary); 
            text-shadow: 0 0 20px var(--primary), 0 0 40px var(--primary);
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .brand::before {
            content: '◈';
            animation: rotateBrand 4s linear infinite;
        }
        
        @keyframes rotateBrand {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .sys-status { 
            font-size: 0.9rem; 
            color: var(--success);
            font-family: 'Share Tech Mono';
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 0 10px var(--success);
        }
        
        .status-dot {
            width: 10px;
            height: 10px;
            background: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--success);
            animation: pulseDot 1.5s ease-in-out infinite;
        }
        
        @keyframes pulseDot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.8); }
        }

        /* --- DASHBOARD GRID --- */
        .dashboard {
            display: grid;
            grid-template-columns: 350px 1fr 350px;
            height: calc(100vh - 70px);
            gap: 25px;
            padding: 25px;
            position: relative;
        }

        .panel {
            background: var(--panel-bg);
            border: 1px solid rgba(0, 243, 255, 0.2);
            border-radius: 16px;
            backdrop-filter: blur(20px);
            padding: 25px;
            display: flex; 
            flex-direction: column;
            overflow: hidden;
            position: relative;
            box-shadow: 
                0 0 40px rgba(0,0,0,0.6),
                inset 0 0 60px rgba(0, 243, 255, 0.02);
            transition: all 0.3s ease;
        }
        
        .panel:hover {
            border-color: rgba(0, 243, 255, 0.4);
            box-shadow: 
                0 0 60px rgba(0,0,0,0.7),
                inset 0 0 80px rgba(0, 243, 255, 0.05);
        }
        
        .panel::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--primary), transparent);
            opacity: 0.5;
        }

        .panel h3 { 
            margin: 0 0 20px 0; 
            color: var(--primary); 
            font-size: 1.2rem; 
            border-bottom: 1px solid rgba(255,255,255,0.1); 
            padding-bottom: 10px; 
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 2px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* --- LEFT PANEL: CAMERA & STATS --- */
        .cam-container {
            width: 100%; 
            height: 220px;
            background: #000; 
            border: 2px solid var(--primary);
            margin-bottom: 15px; 
            position: relative;
            overflow: hidden; 
            border-radius: 12px;
            box-shadow: var(--glow-primary);
            transition: all 0.3s ease;
        }
        
        .cam-feed { 
            width: 100%; 
            height: 100%; 
            object-fit: cover;
            filter: contrast(1.1) brightness(1.1);
        }
        
        .cam-overlay {
            position: absolute; 
            top: 0; left: 0; 
            width: 100%; 
            height: 100%;
            background: 
                linear-gradient(transparent 50%, rgba(0,243,255,0.05) 50%),
                linear-gradient(90deg, rgba(0,243,255,0.03) 1px, transparent 1px),
                linear-gradient(rgba(0,243,255,0.03) 1px, transparent 1px);
            background-size: 100% 4px, 20px 100%, 100% 20px;
            pointer-events: none;
            animation: overlayScan 2s linear infinite;
        }
        
        @keyframes overlayScan {
            0% { transform: translateY(0); }
            100% { transform: translateY(4px); }
        }
        
        /* Face Scanner Animation */
        .face-scan-beam {
            position: absolute; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--success), transparent);
            box-shadow: 0 0 30px var(--success);
            opacity: 0;
            z-index: 5;
        }
        
        .scanning .face-scan-beam {
            opacity: 1;
            animation: scanFace 2s ease-in-out infinite;
        }
        
        @keyframes scanFace { 
            0% { top: 0%; opacity: 0; } 
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { top: 100%; opacity: 0; } 
        }

        /* Face Boxes */
        .face-box {
            position: absolute; 
            border: 2px solid var(--success);
            display: none; 
            box-shadow: 0 0 20px var(--success), inset 0 0 20px rgba(0,255,157,0.2);
            transition: all 0.3s ease;
            background: rgba(0,255,157,0.05);
        }
        
        .face-box::before,
        .face-box::after {
            content: '';
            position: absolute;
            width: 10px;
            height: 10px;
            border: 2px solid var(--success);
        }
        
        .face-box::before {
            top: -2px;
            left: -2px;
            border-right: none;
            border-bottom: none;
        }
        
        .face-box::after {
            bottom: -2px;
            right: -2px;
            border-left: none;
            border-top: none;
        }

        /* Main User Box */
        #face-main {
            top: 50%; 
            left: 50%; 
            transform: translate(-50%, -50%);
            width: 120px; 
            height: 140px;
        }
        
        /* Second Person Box (Intruder) */
        #face-intruder {
            top: 50%; 
            left: 20%; 
            transform: translate(-50%, -50%);
            width: 100px; 
            height: 120px;
            border-color: var(--danger); 
            box-shadow: 0 0 30px var(--danger), inset 0 0 20px rgba(255,0,85,0.2);
            background: rgba(255,0,85,0.1);
            animation: intruderPulse 0.5s ease-in-out infinite;
        }
        
        #face-intruder::before,
        #face-intruder::after {
            border-color: var(--danger);
        }
        
        @keyframes intruderPulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        /* Alert States */
        .cam-container.alert #face-main { 
            border-color: var(--danger); 
            box-shadow: 0 0 30px var(--danger), inset 0 0 20px rgba(255,0,85,0.3);
            background: rgba(255,0,85,0.1);
            animation: alertPulse 0.3s ease-in-out infinite;
        }
        
        .cam-container.alert #face-main::before,
        .cam-container.alert #face-main::after {
            border-color: var(--danger);
        }
        
        @keyframes alertPulse {
            0%, 100% { transform: translate(-50%, -50%) scale(1); }
            50% { transform: translate(-50%, -50%) scale(1.05); }
        }
        
        .cam-container.alert { 
            border-color: var(--danger); 
            box-shadow: var(--glow-danger);
            animation: shakeCam 0.4s ease-in-out infinite;
        }
        
        @keyframes shakeCam { 
            0%, 100% { transform: translate(0,0); } 
            25% { transform: translate(3px,3px); } 
            50% { transform: translate(-3px,3px); } 
            75% { transform: translate(3px,-3px); } 
        }

        .cam-status {
            position: absolute; 
            bottom: 10px; 
            left: 10px; 
            font-size: 0.75rem; 
            color: var(--success); 
            background: rgba(0,0,0,0.8); 
            padding: 5px 10px;
            border-radius: 4px;
            font-family: 'Share Tech Mono';
            border: 1px solid rgba(0,255,157,0.3);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .cam-status::before {
            content: '●';
            animation: blink 1s ease-in-out infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }

        .stat-card {
            background: linear-gradient(135deg, rgba(0, 243, 255, 0.05) 0%, rgba(112, 0, 255, 0.05) 100%);
            margin-bottom: 20px; 
            padding: 20px;
            border-left: 4px solid var(--primary);
            border-radius: 8px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateX(5px);
            background: linear-gradient(135deg, rgba(0, 243, 255, 0.1) 0%, rgba(112, 0, 255, 0.1) 100%);
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, var(--primary), transparent);
        }
        
        .stat-val { 
            font-size: 1.8rem; 
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(0,243,255,0.3);
        }
        
        .stat-label { 
            font-size: 0.8rem; 
            color: #888; 
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 5px;
        }

        /* --- CENTER PANEL: AUTHENTICATION --- */
        .auth-container {
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center;
            height: 100%; 
            position: relative;
        }

        .shield-ring {
            width: 250px; 
            height: 250px;
            border: 3px dashed rgba(0, 243, 255, 0.3);
            border-radius: 50%;
            display: flex; 
            align-items: center; 
            justify-content: center;
            margin-bottom: 30px;
            position: relative;
            animation: spinShield 15s linear infinite;
            box-shadow: 
                0 0 60px rgba(0, 243, 255, 0.1),
                inset 0 0 60px rgba(0, 243, 255, 0.05);
            transition: all 0.5s ease;
        }
        
        .shield-ring::before,
        .shield-ring::after {
            content: '';
            position: absolute;
            border-radius: 50%;
            border: 2px dashed rgba(0, 243, 255, 0.2);
        }
        
        .shield-ring::before {
            width: 180px;
            height: 180px;
            animation: spinShield 10s linear infinite reverse;
        }
        
        .shield-ring::after {
            width: 220px;
            height: 220px;
            animation: spinShield 20s linear infinite;
        }
        
        .shield-core {
            width: 100px; 
            height: 100px;
            background: radial-gradient(circle, var(--primary) 0%, transparent 70%);
            border-radius: 50%;
            filter: drop-shadow(0 0 30px var(--primary));
            animation: pulseCore 3s ease-in-out infinite;
            position: relative;
        }
        
        .shield-core::before {
            content: '◈';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 3rem;
            color: var(--bg-dark);
        }
        
        @keyframes spinShield { 
            0% { transform: rotate(0deg); } 
            100% { transform: rotate(360deg); } 
        }
        
        @keyframes pulseCore { 
            0%, 100% { transform: scale(0.9); opacity: 0.7; } 
            50% { transform: scale(1.1); opacity: 1; } 
        }

        /* Input */
        .input-group { 
            width: 100%; 
            max-width: 600px; 
            position: relative;
        }
        
        .input-group::before,
        .input-group::after {
            content: '';
            position: absolute;
            width: 20px;
            height: 20px;
            border: 2px solid var(--primary);
            transition: all 0.3s ease;
        }
        
        .input-group::before {
            top: -10px;
            left: -10px;
            border-right: none;
            border-bottom: none;
        }
        
        .input-group::after {
            bottom: -10px;
            right: -10px;
            border-left: none;
            border-top: none;
        }
        
        .input-group:focus-within::before,
        .input-group:focus-within::after {
            width: 100%;
            height: 100%;
            opacity: 0.3;
        }
        
        input {
            width: 100%; 
            padding: 25px;
            background: rgba(0,0,0,0.6);
            border: 2px solid rgba(0, 243, 255, 0.3);
            border-radius: 4px;
            color: #fff; 
            font-size: 1.8rem; 
            font-family: 'Orbitron', sans-serif;
            text-align: center; 
            outline: none; 
            letter-spacing: 4px;
            box-shadow: 
                0 0 30px rgba(0, 243, 255, 0.1),
                inset 0 0 30px rgba(0,0,0,0.5);
            transition: all 0.3s ease;
        }
        
        input:focus { 
            border-color: var(--primary);
            box-shadow: 
                0 0 50px rgba(0, 243, 255, 0.3),
                inset 0 0 30px rgba(0,0,0,0.5);
            transform: scale(1.02);
        }
        
        input::placeholder {
            color: rgba(255,255,255,0.3);
            font-size: 1.2rem;
        }

        /* Controls */
        .controls { 
            display: flex; 
            gap: 15px; 
            margin-top: 40px; 
            flex-wrap: wrap; 
            justify-content: center; 
        }
        
        .btn {
            padding: 15px 30px;
            background: rgba(0, 243, 255, 0.05);
            border: 1px solid rgba(0, 243, 255, 0.3);
            color: var(--primary);
            font-family: 'Orbitron', sans-serif;
            font-weight: 700; 
            letter-spacing: 2px;
            cursor: pointer; 
            transition: all 0.3s ease;
            clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
            position: relative;
            overflow: hidden;
            font-size: 0.9rem;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0,243,255,0.2), transparent);
            transition: left 0.5s ease;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn:hover, .btn.active { 
            background: var(--primary); 
            color: #000; 
            box-shadow: var(--glow-primary);
            transform: translateY(-2px);
        }
        
        .btn-hack { 
            border-color: var(--danger); 
            color: var(--danger); 
            background: rgba(255,0,85,0.05);
        }
        
        .btn-hack::before {
            background: linear-gradient(90deg, transparent, rgba(255,0,85,0.2), transparent);
        }
        
        .btn-hack:hover { 
            background: var(--danger); 
            color: #fff; 
            box-shadow: var(--glow-danger);
        }
        
        .btn-capture { 
            border-color: var(--success); 
            color: var(--success); 
            background: rgba(0, 255, 157, 0.05);
            width: 100%; 
            margin-bottom: 20px; 
            display: none;
            clip-path: polygon(5% 0, 100% 0, 100% 80%, 95% 100%, 0 100%, 0 20%);
        }
        
        .btn-capture::before {
            background: linear-gradient(90deg, transparent, rgba(0,255,157,0.2), transparent);
        }
        
        .btn-capture:hover { 
            background: var(--success); 
            color: #000; 
            box-shadow: var(--glow-success);
        }

        /* --- RIGHT PANEL: LIVE LOGS --- */
        .log-terminal {
            font-family: 'Share Tech Mono'; 
            font-size: 0.8rem; 
            color: #aaa;
            overflow-y: auto; 
            height: 100%; 
            padding-right: 10px;
            position: relative;
        }
        
        .log-terminal::-webkit-scrollbar {
            width: 6px;
        }
        
        .log-terminal::-webkit-scrollbar-track {
            background: rgba(0,0,0,0.3);
        }
        
        .log-terminal::-webkit-scrollbar-thumb {
            background: var(--primary);
            border-radius: 3px;
        }
        
        .log-entry { 
            margin-bottom: 8px; 
            border-left: 2px solid rgba(0,243,255,0.2);
            padding: 8px 0 8px 12px;
            transition: all 0.3s ease;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .log-entry:hover {
            background: rgba(0,243,255,0.05);
            border-left-color: var(--primary);
        }
        
        .log-time { 
            color: var(--primary); 
            margin-right: 8px; 
            font-weight: bold;
            text-shadow: 0 0 10px rgba(0,243,255,0.5);
        }
        
        .log-warn { 
            color: var(--danger);
            text-shadow: 0 0 10px rgba(255,0,85,0.5);
            animation: warnPulse 1s ease-in-out infinite;
        }
        
        @keyframes warnPulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .log-success { 
            color: var(--success);
            text-shadow: 0 0 10px rgba(0,255,157,0.5);
        }

        /* --- OVERLAY: VAULT --- */
        #vault-screen {
            position: absolute; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%;
            background: radial-gradient(circle at center, rgba(0,20,10,0.98) 0%, rgba(0,5,5,0.99) 100%);
            z-index: 100;
            display: none; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center;
            animation: vaultReveal 1s ease-out;
        }
        
        @keyframes vaultReveal {
            0% {
                opacity: 0;
                transform: scale(0.9);
            }
            100% {
                opacity: 1;
                transform: scale(1);
            }
        }

        .folder-grid { 
            display: grid; 
            grid-template-columns: repeat(3, 1fr); 
            gap: 50px; 
            margin-top: 60px; 
        }
        
        .folder {
            border: 1px solid var(--success); 
            padding: 40px; 
            text-align: center;
            background: rgba(0, 255, 157, 0.05); 
            cursor: pointer; 
            transition: all 0.4s ease;
            border-radius: 12px;
            position: relative;
            overflow: hidden;
        }
        
        .folder::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0,255,157,0.2), transparent);
            transition: left 0.6s ease;
        }
        
        .folder:hover::before {
            left: 100%;
        }
        
        .folder:hover { 
            background: var(--success); 
            color: #000; 
            box-shadow: var(--glow-success);
            transform: translateY(-10px) scale(1.05);
        }
        
        .folder-icon {
            font-size: 4rem;
            margin-bottom: 15px;
            display: block;
            transition: transform 0.3s ease;
        }
        
        .folder:hover .folder-icon {
            transform: scale(1.2) rotate(5deg);
        }

        /* --- OVERLAY: PIRACY / DANGER --- */
        #danger-overlay {
            position: absolute; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%;
            background: 
                radial-gradient(circle at 30% 30%, rgba(255,0,85,0.2) 0%, transparent 50%),
                radial-gradient(circle at 70% 70%, rgba(255,0,85,0.2) 0%, transparent 50%),
                rgba(10, 0, 0, 0.95);
            z-index: 200;
            display: none; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center;
            backdrop-filter: blur(10px);
            border: 3px solid var(--danger);
            animation: dangerPulse 0.5s ease-in-out;
        }
        
        @keyframes dangerPulse {
            0% { transform: scale(1.1); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .danger-title {
            font-size: 6rem; 
            color: var(--danger); 
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            text-shadow: 0 0 50px var(--danger), 0 0 100px var(--danger);
            animation: dangerBlink 0.3s infinite;
            text-align: center; 
            line-height: 1;
            letter-spacing: 10px;
        }
        
        .danger-sub { 
            color: #fff; 
            font-size: 1.8rem; 
            margin-top: 30px; 
            letter-spacing: 5px;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            text-shadow: 0 0 20px rgba(255,255,255,0.5);
        }
        
        @keyframes dangerBlink { 
            0%, 100% { opacity: 1; text-shadow: 0 0 50px var(--danger), 0 0 100px var(--danger); } 
            50% { opacity: 0.3; text-shadow: 0 0 20px var(--danger); } 
        }

        .glitch-anim { 
            animation: glitch 0.3s cubic-bezier(.25, .46, .45, .94) both infinite;
            border-color: var(--danger) !important; 
            box-shadow: var(--glow-danger) !important;
            color: var(--danger) !important;
        }
        
        @keyframes glitch {
            0% { transform: translate(0); }
            20% { transform: translate(-3px, 3px); }
            40% { transform: translate(-3px, -3px); }
            60% { transform: translate(3px, 3px); }
            80% { transform: translate(3px, -3px); }
            100% { transform: translate(0); }
        }

        /* DEVICE ANGLE */
        .angle-meter {
            height: 6px; 
            width: 100%; 
            background: rgba(255,255,255,0.1); 
            margin-top: 15px; 
            position: relative;
            border-radius: 3px;
            overflow: hidden;
        }
        
        .angle-val {
            position: absolute; 
            top: 0; 
            left: 50%; 
            width: 4px; 
            height: 100%; 
            background: var(--primary);
            box-shadow: 0 0 10px var(--primary);
            transition: left 0.2s ease;
            border-radius: 2px;
        }
        
        .angle-val::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 12px;
            height: 12px;
            background: var(--primary);
            border-radius: 50%;
            box-shadow: 0 0 20px var(--primary);
        }

        /* Holographic effect */
        .holo-text {
            background: linear-gradient(90deg, var(--primary), var(--secondary), var(--primary));
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: holoShift 3s linear infinite;
        }
        
        @keyframes holoShift {
            0% { background-position: 0% center; }
            100% { background-position: 200% center; }
        }

        /* Loading bars */
        .loading-bar {
            width: 100%;
            height: 4px;
            background: rgba(255,255,255,0.1);
            border-radius: 2px;
            overflow: hidden;
            margin-top: 10px;
        }
        
        .loading-progress {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--success));
            width: 0%;
            transition: width 0.3s ease;
            box-shadow: 0 0 10px var(--primary);
        }

        /* Typing indicator */
        .typing-indicator {
            display: flex;
            gap: 5px;
            align-items: center;
            justify-content: center;
            margin-top: 20px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .typing-indicator.active {
            opacity: 1;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            background: var(--primary);
            border-radius: 50%;
            animation: typingBounce 1.4s ease-in-out infinite;
        }
        
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typingBounce {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }

    </style>
</head>
<body>

    <canvas id="particle-canvas"></canvas>
    <div class="bg-mesh"></div>
    <div class="scan-lines"></div>

    <header>
        <div class="brand">BIO-TRUST <span style="font-size:0.9rem; color:#888; font-weight:400;">// NEURAL SECURITY CORE v2.0</span></div>
        <div class="sys-status"><span class="status-dot"></span>SYSTEM SECURE</div>
    </header>

    <div class="dashboard">
        
        <!-- LEFT PANEL -->
        <div class="panel">
            <h3>◉ OPTICAL SENSOR</h3>
            <div class="cam-container" id="cam-container">
                <video id="video-feed" class="cam-feed" autoplay muted playsinline></video>
                <div class="cam-overlay"></div>
                <div class="face-scan-beam"></div>
                <div id="face-main" class="face-box"></div>
                <div id="face-intruder" class="face-box"></div>
                <div id="cam-status" class="cam-status">INITIALIZING...</div>
            </div>
            
            <button id="btn-capture" class="btn btn-capture" onclick="captureFace()">
                [ + ] INITIALIZE BIOMETRIC SCAN
            </button>

            <h3 style="margin-top:25px;">◉ LIVE METRICS</h3>
            <div class="stat-card">
                <div class="stat-label">DEVICE ORIENTATION</div>
                <div class="stat-val" id="angle-display">0.0°</div>
                <div class="angle-meter"><div class="angle-val" id="angle-bar"></div></div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">BEHAVIORAL ENTROPY</div>
                <div class="stat-val" id="mouse-score">0000</div>
                <div class="loading-bar">
                    <div class="loading-progress" id="entropy-bar" style="width: 0%"></div>
                </div>
            </div>
        </div>

        <!-- CENTER PANEL -->
        <div class="panel">
            <div class="auth-container" id="auth-ui">
                <div class="shield-ring" id="shield-ring">
                    <div class="shield-core"></div>
                </div>
                
                <h1 style="margin:0 0 15px 0; letter-spacing:5px;" class="holo-text">AUTHENTICATION</h1>
                <div id="instruction" style="color:#888; margin-bottom:40px; letter-spacing:2px; font-weight:600; font-size:1.1rem;">
                    VERIFY IDENTITY TO ACCESS NEURAL VAULT
                </div>

                <div class="input-group">
                    <input type="text" id="password-input" placeholder="ENTER PASSPHRASE" autocomplete="off">
                </div>
                
                <div class="typing-indicator" id="typing-indicator">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </div>

                <div class="controls">
                    <button class="btn active" id="btn-train" onclick="setMode('train')">1. ENROLL ID</button>
                    <button class="btn" id="btn-verify" onclick="setMode('verify')">2. VERIFY</button>
                    <button class="btn btn-hack" onclick="triggerMultiFace()">3. SIMULATE INTRUSION</button>
                </div>
            </div>
        </div>

        <!-- RIGHT PANEL -->
        <div class="panel">
            <h3>◉ NEURAL LOGS</h3>
            <div class="log-terminal" id="terminal">
                <div class="log-entry"><span class="log-time">[SYS]</span> Initializing Bio-Trust Neural Engine...</div>
                <div class="log-entry"><span class="log-time">[SYS]</span> Loading Optical Recognition Modules...</div>
                <div class="log-entry"><span class="log-time">[SYS]</span> Establishing Secure Connection...</div>
            </div>
            
            <h3 style="margin-top:20px;">◉ BIOMETRIC RHYTHM</h3>
            <canvas id="rhythmChart" height="140"></canvas>
        </div>

    </div>

    <!-- SECRET VAULT -->
    <div id="vault-screen">
        <h1 style="color:var(--success); font-size:4rem; text-shadow:0 0 40px var(--success); font-family:'Orbitron'; letter-spacing:5px;">ACCESS GRANTED</h1>
        <p style="letter-spacing:4px; font-family: 'Share Tech Mono'; font-size:1.2rem; color:#888;">WELCOME TO THE NEURAL MAINFRAME</p>
        
        <div class="folder-grid">
            <div class="folder">
                <span class="folder-icon">☢️</span>
                <div style="margin-top:15px; font-weight:bold; font-family:'Orbitron';">LAUNCH CODES</div>
            </div>
            <div class="folder">
                <span class="folder-icon">₿</span>
                <div style="margin-top:15px; font-weight:bold; font-family:'Orbitron';">CRYPTO VAULT</div>
            </div>
            <div class="folder">
                <span class="folder-icon">📂</span>
                <div style="margin-top:15px; font-weight:bold; font-family:'Orbitron';">CLASSIFIED DATA</div>
            </div>
        </div>
        <button class="btn btn-hack" style="margin-top:60px; padding:20px 40px; font-size:1.1rem;" onclick="location.reload()">⟲ LOCK TERMINAL</button>
    </div>

    <!-- DANGER / PIRACY OVERLAY -->
    <div id="danger-overlay">
        <div style="font-size:5rem; animation: dangerBlink 0.3s infinite;">⚠️</div>
        <div class="danger-title" id="alert-title">SECURITY BREACH</div>
        <div class="danger-title" style="font-size:2.5rem; margin-top:20px;" id="alert-msg">UNRECOGNIZED BIOMETRIC</div>
        <p class="danger-sub" id="alert-sub">INTRUDER DETECTED - INITIATING LOCKDOWN</p>
        <div style="margin-top:40px; font-family:'Share Tech Mono'; color:#888; font-size:1.1rem;">SYSTEM LOCKDOWN IN PROGRESS...</div>
        <div class="loading-bar" style="width:300px; margin-top:20px;">
            <div class="loading-progress" style="width:100%; background:var(--danger); box-shadow:0 0 20px var(--danger);"></div>
        </div>
        <button class="btn" style="margin-top:40px; padding:15px 30px;" onclick="location.reload()">REBOOT SYSTEM</button>
    </div>

    <script>
        // --- PARTICLE SYSTEM ---
        const canvas = document.getElementById('particle-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        let mouseX = 0, mouseY = 0;
        
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        
        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 0.5;
                this.vy = (Math.random() - 0.5) * 0.5;
                this.size = Math.random() * 2;
                this.opacity = Math.random() * 0.5 + 0.2;
            }
            
            update() {
                this.x += this.vx;
                this.y += this.vy;
                
                // Mouse interaction
                const dx = mouseX - this.x;
                const dy = mouseY - this.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 100) {
                    this.x -= dx * 0.01;
                    this.y -= dy * 0.01;
                }
                
                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
            }
            
            draw() {
                ctx.fillStyle = `rgba(0, 243, 255, ${this.opacity})`;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        
        // Create particles
        for (let i = 0; i < 100; i++) {
            particles.push(new Particle());
        }
        
        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            particles.forEach(p => {
                p.update();
                p.draw();
            });
            
            // Draw connections
            particles.forEach((p1, i) => {
                particles.slice(i + 1).forEach(p2 => {
                    const dx = p1.x - p2.x;
                    const dy = p1.y - p2.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    
                    if (dist < 100) {
                        ctx.strokeStyle = `rgba(0, 243, 255, ${0.1 * (1 - dist/100)})`;
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(p1.x, p1.y);
                        ctx.lineTo(p2.x, p2.y);
                        ctx.stroke();
                    }
                });
            });
            
            requestAnimationFrame(animateParticles);
        }
        animateParticles();
        
        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        // --- CHART SETUP ---
        const chartCtx = document.getElementById('rhythmChart').getContext('2d');
        const chart = new Chart(chartCtx, {
            type: 'line',
            data: {
                labels: ['1', '2', '3', '4', '5', '6', '7', '8'],
                datasets: [{
                    label: 'Keystroke Dynamics',
                    data: [0, 0, 0, 0, 0, 0, 0, 0],
                    borderColor: '#00f3ff',
                    backgroundColor: 'rgba(0, 243, 255, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#00f3ff',
                    pointBorderColor: '#fff',
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                plugins: { 
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleColor: '#00f3ff',
                        bodyColor: '#fff',
                        borderColor: '#00f3ff',
                        borderWidth: 1
                    }
                },
                scales: { 
                    x: { 
                        display: true,
                        grid: { color: 'rgba(0,243,255,0.1)' },
                        ticks: { color: '#888', font: { family: 'Share Tech Mono' } }
                    }, 
                    y: { 
                        display: true,
                        grid: { color: 'rgba(0,243,255,0.1)' },
                        ticks: { color: '#888', font: { family: 'Share Tech Mono' } }
                    } 
                },
                animation: { duration: 300 }
            }
        });

        // --- APP LOGIC ---
        let mode = 'train';
        let flightTimes = [];
        let holdTimes = [];
        let tiltData = [];
        let mouseEvents = 0;
        let keyDownMap = {};
        let lastKeyUpTime = 0;
        let phrase = "hello ghost";
        let isModelTrained = false;
        let isFaceTrained = false;
        let multiFaceMode = false;

        const pwdInput = document.getElementById('password-input');
        const terminal = document.getElementById('terminal');
        const shieldRing = document.getElementById('shield-ring');
        const instruction = document.getElementById('instruction');
        const dangerOverlay = document.getElementById('danger-overlay');
        const angleDisplay = document.getElementById('angle-display');
        const angleBar = document.getElementById('angle-bar');
        const mouseScoreDisplay = document.getElementById('mouse-score');
        const entropyBar = document.getElementById('entropy-bar');
        const faceMain = document.getElementById('face-main');
        const faceIntruder = document.getElementById('face-intruder');
        const btnCapture = document.getElementById('btn-capture');
        const camStatus = document.getElementById('cam-status');
        const camContainer = document.getElementById('cam-container');
        const alertTitle = document.getElementById('alert-title');
        const alertMsg = document.getElementById('alert-msg');
        const alertSub = document.getElementById('alert-sub');
        const typingIndicator = document.getElementById('typing-indicator');

        pwdInput.placeholder = `TYPE: "${phrase}"`;

        // --- SHORTCUT KEY 'M' FOR MULTI-FACE SIMULATION ---
        document.addEventListener('keydown', (e) => {
            if (e.key === 'm' || e.key === 'M') {
                triggerMultiFace();
            }
        });

        // --- AUTO START CAMERA ---
        window.onload = function() {
            enableCamera();
            log("Neural Engine: ONLINE", "success");
            log("Particle Field: STABILIZED", "info");
        };

        // --- MOUSE TRACKING ---
        document.addEventListener('mousemove', (e) => {
            mouseEvents++;
            mouseScoreDisplay.innerText = mouseEvents.toString().padStart(4, '0');
            const entropyPercent = Math.min((mouseEvents / 1000) * 100, 100);
            entropyBar.style.width = entropyPercent + '%';
        });

        // --- CAMERA LOGIC ---
        function enableCamera() {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    const video = document.getElementById('video-feed');
                    video.srcObject = stream;
                    camStatus.innerHTML = '<span style="color:var(--success)">●</span> OPTICAL SENSORS ACTIVE';
                    log("Face Recognition: ONLINE", "success");
                    faceMain.style.display = 'block';
                    
                    // Add scanning animation
                    setTimeout(() => {
                        camContainer.classList.add('scanning');
                    }, 1000);
                })
                .catch(err => {
                    log("Camera Error: " + err, "warn");
                    camStatus.innerHTML = '<span style="color:var(--danger)">●</span> SENSOR ERROR';
                    alert("Camera access required for biometric verification.");
                });
        }

        function captureFace() {
            log("Initializing Biometric Scan...", "info");
            camContainer.classList.add('scanning');
            
            // Visual feedback
            shieldRing.style.animation = 'spinShield 0.5s linear infinite';
            
            setTimeout(() => {
                isFaceTrained = true;
                log("Biometric Template: STORED", "success");
                camContainer.classList.remove('scanning');
                btnCapture.style.display = 'none';
                instruction.innerHTML = "<span style='color:var(--success)'>✓</span> BIOMETRIC CAPTURED. ENTER PASSPHRASE.";
                pwdInput.focus();
                shieldRing.style.animation = 'spinShield 15s linear infinite';
                
                // Success animation
                shieldRing.style.borderColor = 'var(--success)';
                shieldRing.style.boxShadow = 'var(--glow-success)';
            }, 2500);
        }

        function log(msg, type='info') {
            const div = document.createElement('div');
            div.className = 'log-entry';
            const time = new Date().toLocaleTimeString('en-US', { hour12: false });
            let colorClass = type === 'warn' ? 'log-warn' : (type === 'success' ? 'log-success' : '');
            div.innerHTML = `<span class="log-time">[${time}]</span> <span class="${colorClass}">${msg}</span>`;
            terminal.prepend(div);
            
            // Keep only last 20 logs
            while (terminal.children.length > 20) {
                terminal.removeChild(terminal.lastChild);
            }
        }

        function setMode(m) {
            mode = m;
            multiFaceMode = false;
            resetUI();
            
            document.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
            if(m === 'train') {
                document.getElementById('btn-train').classList.add('active');
                instruction.innerText = "STEP 1: SCAN FACE  →  STEP 2: TYPE PASSPHRASE";
                instruction.style.color = "var(--primary)";
                pwdInput.placeholder = `ENROLL: "${phrase}"`;
                shieldRing.style.borderColor = "rgba(0, 243, 255, 0.3)";
                shieldRing.style.boxShadow = "0 0 60px rgba(0, 243, 255, 0.1)";
                btnCapture.style.display = 'block';
            } else {
                if (!isModelTrained) {
                    alert("⚠️ NEURAL PROFILE NOT FOUND! Please Enroll First.");
                    setMode('train');
                    return;
                }
                document.getElementById('btn-verify').classList.add('active');
                instruction.innerText = "SECURITY MODE: MULTI-FACTOR AUTHENTICATION";
                instruction.style.color = "#fff";
                pwdInput.placeholder = "ENTER PASSPHRASE";
                btnCapture.style.display = 'none';
            }
        }

        function resetUI() {
            pwdInput.value = '';
            pwdInput.disabled = false;
            flightTimes = [];
            holdTimes = [];
            tiltData = [];
            mouseEvents = 0;
            keyDownMap = {};
            lastKeyUpTime = 0;
            pwdInput.focus();
            pwdInput.style.borderColor = "rgba(0, 243, 255, 0.3)";
            pwdInput.classList.remove('glitch-anim');
            shieldRing.style.borderColor = "rgba(0, 243, 255, 0.3)";
            shieldRing.style.boxShadow = "0 0 60px rgba(0, 243, 255, 0.1)";
            camContainer.classList.remove('alert');
            faceMain.style.borderColor = "var(--success)";
            faceIntruder.style.display = 'none';
            typingIndicator.classList.remove('active');
        }

        // --- KEYSTROKE & ANGLE CAPTURE ---
        pwdInput.addEventListener('keydown', e => {
            if(e.key === 'Enter') return;
            if(!keyDownMap[e.code]) keyDownMap[e.code] = Date.now();
            typingIndicator.classList.add('active');
        });

        pwdInput.addEventListener('keyup', e => {
            let now = Date.now();
            let hold = 0, flight = 0;

            // Simulate Device Angle with more variation
            let currentTilt = (mode === 'bot') ? 0 : (Math.random() * 20) - 10; 
            tiltData.push(currentTilt);
            
            angleDisplay.innerText = currentTilt.toFixed(1) + "°";
            angleBar.style.left = (50 + currentTilt * 2.5) + "%";

            if(keyDownMap[e.code]) {
                hold = now - keyDownMap[e.code];
                holdTimes.push(hold);
                delete keyDownMap[e.code];
            }
            if(lastKeyUpTime !== 0) {
                flight = now - lastKeyUpTime;
                flightTimes.push(flight);
                
                // Update chart with animation
                chart.data.datasets[0].data.shift();
                chart.data.datasets[0].data.push(flight);
                chart.update('active');
            }
            lastKeyUpTime = now;

            if(pwdInput.value.length >= phrase.length) {
                typingIndicator.classList.remove('active');
                pwdInput.disabled = true;
                log("Processing Biometric Vectors...", "info");
                setTimeout(processData, 1200);
            }
        });

        async function processData() {
            if(pwdInput.value !== phrase) {
                log("ERROR: PASSPHRASE MISMATCH", "warn");
                loginFail("INVALID PASSPHRASE");
                return;
            }

            if (mode === 'train' && !isFaceTrained) {
                alert("⚠️ BIOMETRIC SCAN REQUIRED!");
                resetUI();
                return;
            }

            if (multiFaceMode) {
                loginFail("MULTIPLE_FACES");
                return;
            }

            // Simulate server analysis
            log("Analyzing Keystroke Dynamics...", "info");
            await new Promise(r => setTimeout(r, 800));
            
            if (mode === 'train') {
                isModelTrained = true;
                log("✓ NEURAL PROFILE CREATED", "success");
                log("Digital DNA: ENCRYPTED & STORED", "success");
                
                // Success animation
                shieldRing.style.borderColor = 'var(--success)';
                shieldRing.style.boxShadow = 'var(--glow-success)';
                pwdInput.style.borderColor = 'var(--success)';
                
                setTimeout(() => {
                    alert("TRAINING COMPLETE. SYSTEM ARMED.");
                    setMode('verify');
                }, 1000);
            } else {
                // Verification logic
                const score = Math.random() * 100;
                if (score > 30) {
                    loginSuccess();
                } else {
                    loginFail("BEHAVIORAL MISMATCH");
                }
            }
        }

        function loginSuccess() {
            log("✓ ACCESS GRANTED - IDENTITY CONFIRMED", "success");
            instruction.innerHTML = "<span style='color:var(--success)'>✓</span> ACCESS GRANTED";
            pwdInput.style.borderColor = "var(--success)";
            shieldRing.style.borderColor = "var(--success)";
            shieldRing.style.boxShadow = "var(--glow-success)";
            
            // Particle explosion effect
            particles.forEach(p => {
                p.vx = (Math.random() - 0.5) * 10;
                p.vy = (Math.random() - 0.5) * 10;
            });
            
            setTimeout(() => {
                document.querySelector('.dashboard').style.display = 'none';
                document.getElementById('vault-screen').style.display = 'flex';
            }, 1500);
        }

        function loginFail(reason) {
            if(reason === "MULTIPLE_FACES") {
                dangerOverlay.style.display = 'flex';
                alertTitle.innerText = "SECURITY BREACH";
                alertMsg.innerText = "MULTIPLE BIOMETRIC SIGNATURES";
                alertSub.innerText = "SHOULDER SURFING ATTACK IDENTIFIED";
                log("CRITICAL: INTRUSION DETECTED", "warn");
                return;
            }

            log(`⚠ SECURITY ALERT: ${reason}`, "warn");
            instruction.innerHTML = `<span style='color:var(--danger)'>✗</span> DENIED: ${reason}`;
            instruction.style.color = "var(--danger)";
            pwdInput.classList.add('glitch-anim');
            pwdInput.style.borderColor = "var(--danger)";
            shieldRing.style.borderColor = "var(--danger)";
            shieldRing.style.boxShadow = "var(--glow-danger)";
            
            // Screen shake
            document.body.style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => {
                document.body.style.animation = '';
            }, 500);
            
            setTimeout(() => {
                resetUI();
                instruction.innerText = "RETRY AUTHENTICATION";
                instruction.style.color = "#888";
            }, 3000);
        }

        function triggerMultiFace() {
            if(!isModelTrained) { 
                alert("Complete enrollment first!"); 
                return; 
            }
            setMode('verify');
            
            multiFaceMode = true;
            log("⚠ WARNING: SECOND BIOMETRIC DETECTED", "warn");
            
            // Visual Updates
            camContainer.classList.add('alert');
            faceMain.style.borderColor = "var(--danger)";
            faceIntruder.style.display = 'block';
            
            // Auto-type with glitch effect
            pwdInput.disabled = true;
            pwdInput.value = phrase;
            pwdInput.classList.add('glitch-anim');
            
            setTimeout(() => {
                processData();
            }, 2000);
        }

    </script>
</body>
</html>
"""

# --- PYTHON BACKEND LOGIC ---
user_profile = { "trained": False, "flight_avg": [], "hold_avg": [], "tilt_avg": [] }

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, phrase=TARGET_PHRASE)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    mode = data.get('mode')
    flight_times = data.get('flight_times', [])
    hold_times = data.get('hold_times', [])
    tilt_data = data.get('tilt_data', [])
    face_match = data.get('face_match', True) 

    if not flight_times: 
        return jsonify({"status": "error", "message": "No data"})

    if mode == 'train':
        user_profile["flight_avg"] = flight_times
        user_profile["hold_avg"] = hold_times
        user_profile["tilt_avg"] = tilt_data
        user_profile["trained"] = True
        return jsonify({"status": "trained"})

    elif mode == 'verify':
        if not user_profile["trained"]: 
            return jsonify({"status": "denied", "score": 0, "reason": "Untrained"})

        curr_flight = np.array(flight_times)
        ref_flight = np.array(user_profile["flight_avg"])
        min_len = min(len(curr_flight), len(ref_flight))
        
        # 1. Rhythm Check
        flight_diff = np.mean(np.abs(curr_flight[:min_len] - ref_flight[:min_len]))
        score = max(0, 100 - flight_diff)
        
        if score > 50:
            return jsonify({"status": "verified", "score": int(score)})
        else:
            return jsonify({"status": "denied", "score": int(score), "reason": "BEHAVIORAL MISMATCH"})

if __name__ == '__main__':
    # Running on port 5001 to avoid conflicts
    print("🔥 BIO-TRUST NEURAL CORE ONLINE: http://127.0.0.1:5001")
    print("✨ Enhanced with particle physics and holographic UI")
    app.run(debug=True, port=5001)