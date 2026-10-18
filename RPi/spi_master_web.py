#!/usr/bin/env python3
from flask import Flask, render_template_string, request, redirect, url_for
import spidev

app = Flask(__name__)

# SPI configuration
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000
spi.mode = 0
spi.bits_per_word = 8

print("RPi SPI web server started...")

# Mapping of web commands to SPI codes
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
    """Send the SPI packet using the same format as the Pygame script."""
    try:
        packet = [0x01, cmd_code, 0]
        spi.xfer2(packet)
        print(f"SPI sent: {packet}")
    except Exception as e:
        print(f"SPI error: {e}")


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
    </style>
</head>
<body>

    <h2>Robot SPI control</h2>

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
        // Use Pointer Events to unify mouse, touch and pen input without conflicts
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
                console.error("Send error:", error);
            });
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
    print(f"WEB DEBUG -> received command: {direction}")

    if direction in SPI_COMMANDS:
        cmd_code = SPI_COMMANDS[direction]
        send_spi(cmd_code)

    return "OK", 200


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nShutdown in progress...")
        spi.close()
