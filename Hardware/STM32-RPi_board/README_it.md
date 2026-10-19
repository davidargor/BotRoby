# Scheda di collegamento tra STM32 Nucleo e Raspberry Pi

[English](README.md)

Per facilitare il collegamento della scheda microcontrollore STM32 Nucleo alla Raspberry Pi, è stata utilizzata una basetta millefori con i seguenti componenti:
- una coppia di strip femmina per alloggiare i pin della Nucleo;
- un connettore maschio a cui è collegato un cavo piatto diretto alla Raspberry Pi;
- una coppia di connettori per alimentare le schede;
- un connettore maschio a 10 pin per collegare la scheda driver dei motori.

<center>
<img src="Nucleo-RPi_perfboard(photo_1).jpg" alt="basetta millefori Nucleo-Raspberry Pi (foto 1)" style="width:600px;"/>
</center>

## Collegamenti sulla scheda

I connettori di alimentazione sono separati solo in parte (il polo negativo è comune a entrambi).

Il disegno rappresenta la basetta millefori vista dal lato delle saldature, quindi è speculare rispetto alla rappresentazione abituale. Purtroppo, ho invertito la piedinatura del connettore della Raspberry Pi e le etichette sono ancora capovolte.

Nel diagramma i collegamenti non sono rappresentati esplicitamente, ma si possono ricostruire seguendo le etichette.

La maggior parte dei pin delle schede è lasciata libera per consentire future espansioni.

<center>
<img src="Nucleo-RPi_perfboard_links_(solder_side).jpg" alt="collegamenti della basetta millefori (lato saldature)" style="width:600px;"/>
</center>

## Posizionamento della scheda Nucleo, del connettore Raspberry Pi e dei collegamenti esterni

Il cavo piatto multicolore nella foto collega i 10 pin della basetta millefori a quelli della scheda driver dei motori.

È necessario collegare:
- i due connettori di alimentazione;
- il cavo piatto della Raspberry Pi;
- la scheda Nucleo, inserendola negli zoccoli predisposti.

<center>
<img src="Nucleo-RPi_perfboard(photo_2).jpg" alt="basetta millefori Nucleo-Raspberry Pi (foto 2)" style="width:600px;"/>
</center>
