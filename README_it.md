# BotRoby

[English](README.md)

BotRoby è un progetto sperimentale di robot mobile modulare, pensato per scopi
didattici e per sperimentare con hardware e software per la robotica. Il
repository raccoglie il software per Raspberry Pi, il firmware per STM32 e la
documentazione dei collegamenti hardware.

La base meccanica è un telaio in alluminio con ruote Mecanum, reperibile presso
diversi rivenditori online. Il progetto è in sviluppo: prima di utilizzare il
robot, consultare le guide e le limitazioni note del firmware.

## Guide e componenti

- [Configurazione e controllo da Raspberry Pi](RPi/README.md)
- [Firmware SPI per STM32 e controllo motori](arduino/README.md)
- [Alimentazione e ricarica](Hardware/Power/README.md)
- [Driver dei motori](Hardware/Motor_Drivers/README.md)
- [Scheda di collegamento STM32 Nucleo–Raspberry Pi](Hardware/STM32-RPi_board/README.md)

## Stato del progetto

Le funzioni di base per la mobilità sono in fase di sviluppo. In particolare,
il firmware STM32 attualmente ignora il parametro di velocità ricevuto nel
pacchetto SPI e usa un valore fisso; vedere la sezione sulle limitazioni nella
[guida del firmware](arduino/README.md).

## Attività future

### Elettronica

- [ ] Progettare e realizzare i PCB, prevedendo i fori di fissaggio al telaio:
  - [ ] modulo di alimentazione e ricarica;
  - [ ] modulo driver motori;
  - [ ] scheda di collegamento Raspberry Pi–Nucleo.
- [ ] Aggiornare gli schemi della scheda di collegamento con pin per sensori e
  attuatori:
  - [ ] Raspberry Pi: LiDAR;
  - [ ] Nucleo: sensori inerziali, GPS, servomotori, finecorsa e altri sensori.
- [ ] Collegare altoparlante, microfono e telecamera alla Raspberry Pi.

### Software

- [ ] Aggiungere il controllo della velocità dei motori.
- [ ] Preparare un'immagine Raspberry Pi con script e servizi già configurati.
- [ ] Generare un avviso acustico quando il sistema è pronto.
- [ ] Integrare ROS e Rust.
- [ ] Aggiungere test unitari e di regressione.

### Meccanica

- [ ] Progettare un supporto per la telecamera.
- [ ] Progettare supporti per microfono e altoparlante.
- [ ] Progettare un supporto per LiDAR.
- [ ] Progettare supporti generici per sensori e attuatori.

## Licenze

Il codice e i materiali originali del progetto hanno licenze distinte. Consultare
il [riepilogo delle licenze](LICENSES.md) prima di riutilizzare o ridistribuire
i contenuti.
