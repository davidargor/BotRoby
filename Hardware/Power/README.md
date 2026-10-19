# Power supply and charging

[Italiano](README_it.md)

The power supply module consists of two parts:
- one responsible for charging the battery
- a pair of step-down modules to power the microcontroller and microprocessor boards (two are used to guarantee a 3A peak current per board)

<center>
<img src="power_module_system_schematic.jpg" alt="power supply module schematic" style="width:600px;"/>
</center>

Two rechargeable 3.7V batteries were used as the power source.
<center>
<img src="Batteries.jpg" alt="batteries" style="width:300px;"/>
</center>

<div style="page-break-after: always;"></div>

## Battery charging module

https://it.aliexpress.com/item/1005012647494433.html

- 2S and 3S lithium battery charging boost module
- Type-C USB BMS 15W 8.4V 12.6V 1.5A max
- support for fast balanced charging
- provision for a charge indicator

<center><img src="battery_charger_module.jpg" alt="battery charging module" style="width:400px;"/></center>

<div style="page-break-after: always;"></div>

## MP1584 Step-Down DC-DC module

- Ultra-compact **MP1584EN** step-down DC-DC power module
- Adjustable **Buck** converter up to **3A**
- Regulated power supply with high precision

<center><img src="step_down_module.jpg" alt="step-down module" style="width:400px;"/></center>

## Connections of the two modules and the battery

As a whole, the module has as inputs the two poles of the battery pair (+ and -) plus the center pole (2S balance / Battery_m); as outputs, it has the pairs of 5V connector outputs.

<center><img src="power_module_wiring_diagram.jpg" alt="power module connection diagram" style="height:400px;"/><img src="power_module_interface.jpg" alt="power module interface connections" style="height:400px;"/></center>
