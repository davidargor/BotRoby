# Configurazione del software

[English](README.md)

La Raspberry Pi gestisce la logica di livello superiore e comunica con la scheda STM-Nucleo tramite una connessione SPI.

È stata installata una versione headless del sistema operativo (Raspbian Lite).

Per abilitare SSH e l'accesso remoto, è stata utilizzata l'interfaccia di configurazione testuale della Raspberry Pi:

```bash
sudo raspi-config
```

> **Nota:** `amministratore` è il nome utente utilizzato su questa Raspberry Pi. Se si sceglie un nome utente diverso, occorre sostituirlo nel codice e nei riferimenti seguenti.

## Abilitare la modalità AP sulla Raspberry Pi

L'interfaccia Wi-Fi deve supportare la modalità AP, così da poterla configurare per l'avvio automatico e per usare un indirizzo IP fisso noto.

Sono stati seguiti questi passaggi:

- Abilitare la modalità AP sull'interfaccia `wlan0`:
    ```sh
    sudo nmcli device wifi hotspot ifname wlan0 ssid "RaspberryAP" password "12345678"
    ```
- Assegnare un indirizzo IP fisso:
    ```sh
    sudo nmcli connection modify Hotspot ipv4.addresses 192.168.4.1/24
    sudo nmcli connection modify Hotspot ipv4.method shared
    ```
- Assegnare una priorità alta, in modo che il sistema non perda tempo a cercare reti Wi-Fi:
    ```sh
    sudo nmcli connection modify Hotspot connection.autoconnect-priority 100
    ```
- Per assicurarsi che NetworkManager sia attivo all'avvio del sistema, eseguire:
    ```sh
    sudo systemctl enable NetworkManager
    ```

## Interfaccia web SPI per il controllo del robot dalla Raspberry Pi (headless)

Questa interfaccia è il modo più semplice e intuitivo per provare il sistema: ci si connette alla rete Wi-Fi della Raspberry Pi e si apre una pagina web con pulsanti che controllano il robot inviando comandi SPI al microcontrollore.

- **Dispositivo**: Raspberry Pi 2 (Raspbian Lite / senza ambiente desktop)
- **Tecnologie**: Python 3, Flask, spidev, HTML5/CSS3 (Pointer Events)
- **Modalità**: movimento mantenendo premuto il pulsante (il robot si muove finché il pulsante resta premuto e si ferma al rilascio)

### 1. PREPARAZIONE DEL SISTEMA

#### A. Abilitare l'interfaccia SPI

È necessario abilitare l'interfaccia SPI della Raspberry Pi. Dal terminale della Raspberry Pi, avviare lo strumento di configurazione:

```bash
sudo raspi-config
```

Quindi accedere a `Interfacing Options -> SPI` e selezionare `Enable`. Al termine, riavviare la Raspberry Pi (`sudo reboot`).

#### B. Installare le librerie necessarie

Verificare che siano installati **Python 3**, **Flask** e il modulo **SPI**:

```bash
sudo apt update
sudo apt install python3-flask python3-spidev
```

## 2. CREAZIONE DELLO SCRIPT PYTHON ([spi_master_web_SPI.py](spi_master_web_SPI.py))

Con le librerie Python installate è stato possibile creare l'interfaccia web di controllo: [spi_master_web_SPI.py](spi_master_web_SPI.py). È necessario renderla eseguibile:

```bash
chmod +x /home/amministratore/spi_master_web_SPI.py
```

### 3. CONFIGURAZIONE DELL'AVVIO AUTOMATICO (servizio systemd)

Per avviare automaticamente il server all'accensione della Raspberry Pi:

1. Creare il file di servizio:

```bash
sudo nano /etc/systemd/system/robot-web.service
```

2. Incollare il blocco seguente:

```ini
[Unit]
Description=Robot SPI Web Controller
After=network.target

[Service]
User=amministratore
WorkingDirectory=/home/amministratore
ExecStart=/usr/bin/python3 /home/amministratore/spi_master_web_SPI.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Salvare e uscire (`Ctrl + O`, Invio, `Ctrl + X`).

3. Abilitare e avviare il servizio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable robot-web.service
sudo systemctl start robot-web.service
```

### 4. UTILIZZO

Si suppone che l'indirizzo IP della Raspberry Pi, configurato in precedenza, sia `192.168.4.1`.

1. Connettersi alla rete Wi-Fi della Raspberry Pi.
2. Aprire il browser e visitare:
   `http://192.168.4.1:5000`

<center>
<img src="RPi_WEB_UI.jpg" alt="interfaccia web della Raspberry Pi" style="width:300px;"/>
</center>

3. **Controllare il robot:** i pulsanti rispondono al tocco continuo (quando si rilascia il pulsante, il robot invia automaticamente il comando di arresto).

*Per controllare lo stato del servizio o consultare i log:*

- Stato: `sudo systemctl status robot-web.service`
- Log in tempo reale: `sudo journalctl -u robot-web.service -f`
