# Gestione dei motori

[English](README.md)

Per azionare i 4 motori CC da 6 V sono stati utilizzati due moduli **DRV8833**. Entrambi i moduli ricevono alimentazione direttamente dalla coppia di batterie da 3,7 V (per un totale di 7,4 V).

## Modulo DRV8833

https://it.aliexpress.com/item/1005008699175375.html

Modulo driver per motori CC DRV8833 a doppio canale da 1,5 A e 3–10 V, ponte H, controllo di motori passo-passo a 4 fili, con protezione da sovracorrente.

<center>
<img src="drv8833.jpg" alt="modulo 8833" style="width:300px;"/>
</center>

## Collegamenti dei moduli

Per attivare il modulo, il pin "EEP" (presumibilmente un'abbreviazione errata di "SLEEP") deve essere impostato su livello alto.

I due moduli condividono i pin di alimentazione dei motori e il pin di abilitazione. La figura mostra il lato delle saldature.

I 4 motori sono identificati con le lettere A, B, C e D.

<center>
<img src="motor_drivers_wirings.jpg" alt="collegamenti dei driver motori" style="width:300px;"/>

<img src="MotorDrivers.jpg" alt="coppia di moduli" style="width:250px;"/>
</center>

## Collegamento della scheda al microcontrollore

La scheda di controllo dei motori si collega al microcontrollore tramite 10 pin, di cui:
8 costituiscono le 4 coppie di pin di controllo dei motori, 1 è il pin di abilitazione (la tensione per un segnale logico alto è 3,3 V) e 1 è il pin GND.

I comandi per azionare i motori sono segnali PWM la cui polarità determina il senso di rotazione, mentre il ciclo di lavoro PWM controlla la velocità. Per gestirli, il microcontrollore deve quindi disporre di 8 pin capaci di generare PWM.
