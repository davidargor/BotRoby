# Alimentazione e ricarica

[English](README.md)

Il modulo di alimentazione è composto da due parti:
- una dedicata alla ricarica della batteria;
- una coppia di moduli step-down per alimentare le schede del microcontrollore e del microprocessore (se ne usano due per garantire una corrente di picco di 3 A per scheda).

<center>
<img src="power_module_system_schematic.jpg" alt="schema del modulo di alimentazione" style="width:600px;"/>
</center>

Come fonte di alimentazione sono state utilizzate due batterie ricaricabili da 3,7 V.
<center>
<img src="Batteries.jpg" alt="batterie" style="width:300px;"/>
</center>

<div style="page-break-after: always;"></div>

## Modulo di ricarica della batteria

https://it.aliexpress.com/item/1005012647494433.html

- Modulo boost per la ricarica di batterie al litio 2S e 3S
- BMS USB Type-C da 15 W, 8,4 V/12,6 V, massimo 1,5 A
- Supporto alla ricarica rapida bilanciata
- Predisposizione per un indicatore di carica

<center><img src="battery_charger_module.jpg" alt="modulo di ricarica della batteria" style="width:400px;"/></center>

<div style="page-break-after: always;"></div>

## Modulo step-down DC-DC MP1584

- Modulo di alimentazione step-down DC-DC **MP1584EN** ultracompatto
- Convertitore **Buck** regolabile fino a **3 A**
- Alimentatore regolato ad alta precisione

<center><img src="step_down_module.jpg" alt="modulo step-down" style="width:400px;"/></center>

## Collegamenti dei due moduli e della batteria

Nel complesso, il modulo ha come ingressi i due poli della coppia di batterie (+ e -) e il polo centrale (bilanciamento 2S / Battery_m); le uscite sono le coppie di connettori da 5 V.

<center><img src="power_module_wiring_diagram.jpg" alt="schema dei collegamenti del modulo di alimentazione" style="height:400px;"/><img src="power_module_interface.jpg" alt="collegamenti dell'interfaccia del modulo di alimentazione" style="height:400px;"/></center>
