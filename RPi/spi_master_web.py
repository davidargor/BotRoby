#!/usr/bin/env python3
from flask import Flask, render_template_string, request, redirect, url_for
import spidev
import time
import subprocess
import threading

app = Flask(__name__)

# --- SPI CONFIGURATION ---
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000
spi.mode = 0
spi.bits_per_word = 8

print("RPi SPI WEB SERVER started...")

# Secret code to confirm shutdown (you can change it)
SHUTDOWN_CODE = "1234"

# Map web commands to SPI codes
SPI_COMMANDS = {
    'forward': 2,     # Forward
    'backward': 3,    # Backward
    'left': 4,        # Left
    'right': 5,       # Right
    'rotate_ccw': 6,  # Counterclockwise rotation
    'rotate_cw': 7,   # Clockwise rotation
    'stop': 0         # Manual stop
}


def send_spi(cmd_code):
    """Send the SPI packet to the robot."""
    try:
        packet_to_send = [0x01, int(cmd_code), 0]
        response_from_slave = spi.xfer2(packet_to_send)
        print(f"--> SPI SENT: {packet_to_send}")
    except Exception as e:
        print(f"SPI error: {e}")

# HTML/CSS web interface with a shutdown button and security prompt
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Robot SPI Web Controller</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            touch-action: manipulation;
        }
        
        body {
            font-family: sans-serif;
            background-color: #121212;
            color: white;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            position: relative;
        }

        h2 {
            margin-bottom: 15px;
            font-size: 1.4rem;
        }

        .controls-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
            width: 90vw;
            max-width: 400px;
        }

        .control-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: repeat(3, 1fr);
            gap: 12px;
            height: 45vh;
            max-height: 280px;
        }

        .rotation-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            height: 8vh;
            min-height: 50px;
        }

        button {
            background-color: #1f1f1f;
            color: white;
            border: 2px solid #333;
            font-size: 2rem;
            font-weight: bold;
            border-radius: 12px;
            cursor: pointer;
            user-select: none;
            -webkit-user-select: none;
            display: flex;
            justify-content: center;
            align-items: center;
            touch-action: none; /* Prevent unusual touch scrolling behavior */
        }

        button.pressed {
            background-color: #00bcd4 !important;
            color: black !important;
        }

        .btn-up { grid-column: 2; grid-row: 1; }
        .btn-left { grid-column: 1; grid-row: 2; }
        .btn-stop { grid-column: 2; grid-row: 2; background-color: #d32f2f; font-size: 1.5rem; }
        .btn-right { grid-column: 3; grid-row: 2; }
        .btn-down { grid-column: 2; grid-row: 3; }

        .btn-rotate {
            background-color: #263238;
            border-color: #37474F;
        }

        /* Shutdown button in the top-right corner */
        .btn-power {
            position: absolute;
            top: 15px;
            right: 15px;
            background-color: #b71c1c;
            color: white;
            border: none;
            border-radius: 50%;
            width: 45px;
            height: 45px;
            font-size: 1.2rem;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .btn-power:active {
            background-color: #d32f2f;
        }
    </style>
</head>
<body>

    <!-- Shutdown button -->
    <button class="btn-power" onclick="requestShutdown()" title="Shut down Raspberry Pi">⏻</button>

    <h2>SPI Robot Control</h2>

    <div class="controls-container">
        <div class="control-grid">
            <button class="btn-up" data-cmd="forward">↑</button>
            <button class="btn-left" data-cmd="left">←</button>
            <button class="btn-stop" data-cmd="stop">■</button>
            <button class="btn-right" data-cmd="right">→</button>
            <button class="btn-down" data-cmd="backward">↓</button>
        </div>

        <div class="rotation-grid">
            <button class="btn-rotate" data-cmd="rotate_ccw">↺</button>
            <button class="btn-rotate" data-cmd="rotate_cw">↻</button>
        </div>
    </div>

    <script>
        document.querySelectorAll('button[data-cmd]').forEach(button => {
            const cmd = button.getAttribute('data-cmd');

            button.addEventListener('pointerdown', (e) => {
                e.preventDefault();
                button.classList.add('pressed');
                sendAction(cmd);
            });

            button.addEventListener('pointerup', (e) => {
                e.preventDefault();
                button.classList.remove('pressed');
                sendAction('stop');
            });

            button.addEventListener('pointerleave', (e) => {
                if (button.classList.contains('pressed')) {
                    button.classList.remove('pressed');
                    sendAction('stop');
                }
            });
        });

        function sendAction(action) {
            let formData = new FormData();
            formData.append('direction', action);
            
            fetch('/move', {
                method: 'POST',
                body: formData
            }).catch(error => {
                console.error("Failed to send request:", error);
            });
        }

        function requestShutdown() {
            let code = prompt("Enter the confirmation code to shut down the Raspberry Pi:");
            if (code !== null && code !== "") {
                let formData = new FormData();
                formData.append('code', code);
                
                fetch('/shutdown', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (response.ok) {
                        alert("Correct code! The Raspberry Pi is shutting down...");
                    } else {
                        alert("Incorrect code! Shutdown cancelled.");
                    }
                })
                .catch(error => {
                    console.error("Network error:", error);
                });
            }
        }
    </script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/move', methods=['GET', 'POST'])
def move():
    if request.method == 'GET':
        return redirect(url_for('index'))
        
    direction = request.form.get('direction')
    cmd_code = SPI_COMMANDS.get(direction, 0)
    send_spi(cmd_code)
    return "OK", 200

@app.route('/shutdown', methods=['POST'])
def shutdown():
    code = request.form.get('code')
    if code == SHUTDOWN_CODE:
        print("\nWEB DEBUG -> Correct shutdown code. System is shutting down...")
        
        # Delay shutdown to allow Flask to send the HTTP response first
        def delayed_shutdown():
            time.sleep(1)
            subprocess.run(['sudo', 'shutdown', '-h', 'now'])
            
        threading.Thread(target=delayed_shutdown).start()
        return "OK", 200
    else:
        print(f"\nWEB DEBUG -> Shutdown attempt failed: incorrect code entered.")
        return "UNAUTHORIZED", 401

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nClosing...")
        spi.close()

