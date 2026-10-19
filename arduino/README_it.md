# Firmware slave SPI

[English](README.md)

Questa cartella contiene il firmware che riceve comandi SPI e li converte in uscite PWM per i quattro motori. La guida descrive il comportamento del codice attuale e gli elementi da modificare per aggiungere comandi o nuove funzionalità.

L'ambiente di sviluppo utilizzato per scrivere il codice del microcontrollore è [Arduino IDE](https://www.arduino.cc/en/software/) con la libreria [STM32duino](https://github.com/stm32duino).

## File e responsabilità

| File | Responsabilità |
| --- | --- |
| `spi_slave.ino` | Inizializza SPI, riceve i pacchetti e avvia l'elaborazione nel ciclo principale Arduino. |
| `cmdParser.h` | Definisce gli ID dei comandi, i pin dei motori e le dichiarazioni delle funzioni. |
| `cmdParser.cpp` | Associa gli ID alle funzioni di gestione e genera i segnali PWM per i motori. |

## Flusso dei pacchetti

Il formato previsto per un comando è un frame di tre byte:

| Indice | Campo | Significato previsto |
| --- | --- | --- |
| 0 | `grpID` | Gruppo o sottosistema di destinazione; `0x01` indica il gruppo mobilità. |
| 1 | `cmdID` | Identificatore dell'azione. |
| 2 | `param` | Parametro dell'azione; per i comandi di movimento è la velocità. |

Il flusso del firmware è il seguente:

1. `MX_SPI1_Init()` configura SPI1 come slave e avvia la ricezione, tramite interrupt, di `BUFFER_SIZE` byte (attualmente 3).
2. Al termine della ricezione, `HAL_SPI_RxCpltCallback()` imposta `dataReady` e riavvia la ricezione.
3. `loop()` rileva `dataReady`, stampa i byte ricevuti e chiama `executeCommand()`.
4. `executeCommand()` seleziona una funzione di gestione in base al comando.
5. Le funzioni di gestione impostano le uscite dei motori tramite `setMotorPWM()`, `setMotorOff()` o `setMotorBrake()`.

L'interrupt segnala solo la ricezione; l'elaborazione dei comandi avviene nel ciclo principale, non nella callback.

## Configurazione SPI e collegamenti

La configurazione in `MX_SPI1_Init()` è:

- SPI1 in modalità slave, full duplex, a due fili;
- parole da 8 bit, bit più significativo per primo (MSB first);
- polarità e fase `LOW` / `1EDGE` (modalità SPI 0);
- NSS hardware, collegato a PA4;
- CRC hardware disabilitato;
- pin SPI: PA5 = SCK, PA6 = MISO, PA7 = MOSI, PA4 = NSS.

Il master deve quindi utilizzare impostazioni compatibili e mantenere NSS attivo durante la trasmissione del frame. In questo file la frequenza SPI non è specificata.

## Comportamento attuale e limitazioni note

Il formato a tre byte è quello previsto, ma il codice attuale non ne implementa completamente la semantica:

- `loop()` chiama `executeCommand(spiRxBuffer[0], spiRxBuffer[1], 100)`. Il terzo byte ricevuto (`spiRxBuffer[2]`) è commentato e quindi ignorato; i comandi di movimento usano sempre la velocità `100`.
- `executeCommand()` non usa `grpID`; lo `switch` seleziona il comando basandosi solo su `cmdID`. Il gruppo `0x01` è documentato come gruppo mobilità, ma il parser non lo convalida né lo instrada.
- La ricezione è fissa a tre byte. Non sono previsti campo lunghezza, delimitatore, numero di sequenza o checksum/CRC a livello applicativo.
- `HAL_SPI_RxCpltCallback()` riavvia la ricezione usando lo stesso buffer condiviso con `loop()`. Un pacchetto successivo ricevuto prima che il ciclo principale abbia elaborato il precedente potrebbe sovrascrivere i dati. Se si prevedono trasmissioni frequenti, è opportuno usare buffer separati o una coda.
- Se `HAL_SPI_Init()` fallisce, il firmware rimane nel ciclo infinito definito dal codice; non è prevista alcuna procedura di recupero.

Questi aspetti implementativi vanno considerati quando si estende il sistema e non devono essere confusi con le funzionalità previste dal formato del protocollo.

## Comandi di mobilità

Gli ID sono definiti in `cmdParser.h`:

| ID | Macro | Azione | Parametro |
| --- | --- | --- | --- |
| `0x00` | `CMD_MOTORS_OFF` | Spegne i motori: PWM a zero su entrambe le uscite di ciascun motore. | Ignorato dalla funzione di gestione. |
| `0x01` | `CMD_MOTORS_BRAKE` | Applica PWM `255` a entrambe le uscite di ciascun motore. | Ignorato dalla funzione di gestione. |
| `0x02` | `CMD_MOTORS_FRONT` | Movimento in avanti. | Velocità. |
| `0x03` | `CMD_MOTORS_BACK` | Movimento all'indietro. | Velocità. |
| `0x04` | `CMD_MOTORS_LEFT` | Movimento laterale verso sinistra. | Velocità. |
| `0x05` | `CMD_MOTORS_RIGHT` | Movimento laterale verso destra. | Velocità. |
| `0x06` | `CMD_MOTORS_RLEFT` | Rotazione in senso antiorario. | Velocità. |
| `0x07` | `CMD_MOTORS_RRIGHT` | Rotazione in senso orario. | Velocità. |

Le funzioni di gestione passano velocità e direzione a `setMotorPWM(pinA, pinB, speed, forward)`. Se `speed` è zero, entrambe le uscite vengono impostate a zero; altrimenti, `forward == true` attiva A e `forward == false` attiva B.

La mappatura della direzione implementata dalle funzioni di gestione è:

| Funzione di gestione | Motore A | Motore B | Motore C | Motore D |
| --- | --- | --- | --- | --- |
| `handleMotorsFront` | A | A | A | A |
| `handleMotorsBack` | B | B | B | B |
| `handleMotorsLeft` | B | A | A | B |
| `handleMotorsRight` | A | B | B | A |
| `handleMotorsRLeft` | B | B | A | A |
| `handleMotorsRRight` | A | A | B | B |

Qui A/B indica quale uscita della coppia del motore riceve il PWM, non una posizione fisica a sinistra o a destra. La mappatura dipende dal cablaggio e dai driver.

## Uscite dei motori

I pin sono definiti in `cmdParser.h` e configurati come uscite in `setup()`:

| Motore | Pin 1 | Pin 2 |
| --- | --- | --- |
| A | PA0 | PB10 |
| B | PA1 | PB11 |
| C | PB13 | PB14 |
| D | PB4 | PB5 |

Le funzioni primitive in `cmdParser.cpp` sono il livello di controllo più basso:

- `setMotorPWM()` seleziona direzione e ciclo di lavoro;
- `setMotorOff()` imposta entrambe le uscite a zero;
- `setMotorBrake()` imposta entrambe le uscite a `255`.

Prima di modificare queste funzioni, verificare sempre che pin, canali PWM, driver e significato elettrico di arresto/frenata siano compatibili con l'hardware.

## Aggiungere un comando di mobilità

Per aggiungere un comando appartenente al gruppo motori:

1. Scegliere un ID libero e definire la macro `CMD_MOTORS_...` in `cmdParser.h`, evitando conflitti con gli ID esistenti.
2. Dichiarare la funzione di gestione in `cmdParser.h` con il parametro appropriato (per esempio `uint8_t speed` se serve la velocità).
3. Aggiungere un `case` a `executeCommand()` in `cmdParser.cpp`. Il `case` deve chiamare la funzione di gestione e terminare con `break`.
4. Implementare la funzione di gestione in `cmdParser.cpp`. Per il movimento dei quattro motori, riutilizzare `setMotorPWM()` specificando i pin e la direzione per ciascun motore.
5. Verificare la generazione del frame sul master e la ricezione sullo slave. Prima di provare il movimento con i motori collegati, controllare le uscite con il robot sollevato o con i motori scollegati.

Esempio schematico:

```cpp
// cmdParser.h
#define CMD_MOTORS_EXAMPLE 0x08
void handleMotorsExample(uint8_t speed);

// cmdParser.cpp: dentro executeCommand()
case CMD_MOTORS_EXAMPLE:
  handleMotorsExample(param);
  break;

// cmdParser.cpp: implementazione
void handleMotorsExample(uint8_t speed) {
  // Impostare qui direzione e velocità per ciascun motore.
}
```

Per rendere effettivo il parametro del frame, aggiornare anche `loop()` in `spi_slave.ino`, in modo che passi `spiRxBuffer[2]` invece del valore fisso `100`. Il master deve inviare lo stesso ID e codificare la velocità nello stesso byte.

## Aggiungere un gruppo o una periferica

Al momento `grpID` viene ricevuto e passato a `executeCommand()`, ma viene ignorato. Per introdurre gruppi distinti, modificare `executeCommand()` in modo che instradi i comandi usando sia `grpID` sia `cmdID`; aggiungere poi le definizioni e le funzioni di gestione del nuovo gruppo nei file appropriati. Aggiornare contestualmente il firmware del master e la documentazione del protocollo.

Se la nuova periferica richiede più dati o un frame di lunghezza diversa, non basta aggiungere un `case`: è necessario aggiornare insieme `BUFFER_SIZE`, la ricezione HAL, l'interpretazione dei byte e il protocollo lato master.
