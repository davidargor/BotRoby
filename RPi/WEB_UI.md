# SPI web interface for robot control on Raspberry Pi (headless)

- **Device**: Raspberry Pi 2 (Raspbian Lite / no desktop)
- **Technology**: Python 3, Flask, spidev, HTML5/CSS3 (Pointer Events)
- **Mode**: Hold-to-move (the robot moves while the button is pressed and stops when released)

## 1. SYSTEM PREPARATION

### A. Enable the SPI interface

From the Raspberry Pi terminal, run the configuration tool:

```bash
sudo raspi-config
```

- Go to `Interfacing Options -> SPI` and select `Enable`.
- Reboot the Raspberry Pi (`sudo reboot`).

### B. Install the required libraries

Make sure the system has **Python 3**, **Flask**, and the **SPI** module installed:

```bash
sudo apt update
sudo apt install python3-flask python3-spidev
```

## 2. COPY THE PYTHON SCRIPT ([spi_master_web_SPI.py](spi_master_web_SPI.py))

Copy the main script in the user's home folder (for example `/home/pi/spi_master_web_SPI.py`):

- Make the script executable:

```bash
chmod +x /home/pi/spi_master_web_SPI.py
```

## 3. AUTOMATIC STARTUP CONFIGURATION (systemd service)

To make the server start automatically when the Raspberry Pi powers on:

1. Create the service file:

```bash
sudo nano /etc/systemd/system/robot-web.service
```

2. Paste the following block (replace `pi` with your actual username if different):

```ini
[Unit]
Description=Robot SPI Web Controller
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 /home/pi/spi_master_web_SPI.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Save and exit (`Ctrl + O`, Enter, `Ctrl + X`).

3. Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable robot-web.service
sudo systemctl start robot-web.service
```

## 4. DAILY USAGE

1. Find the Raspberry Pi IP address:

```bash
hostname -I
```

2. Open a browser (from a smartphone, tablet, or PC connected to the same network) and visit:
   `http://<RASPBERRY_IP>:5000` (for example `http://192.168.4.247:5000`)

3. **Control the robot:** the buttons respond to continuous touch (when the finger is released, the robot automatically sends the stop command).

*If you need to check the service status or logs later:*

- Status: `sudo systemctl status robot-web.service`
- Real-time logs: `sudo journalctl -u robot-web.service -f`

