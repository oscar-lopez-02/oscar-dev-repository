# 25 kHz Active Bandpass Filter & Peak Detector

## Project Overview
This repository contains the design, simulation, and hardware implementation of a highly selective frequency detection circuit. The primary objective of this project was to successfully isolate a 25 kHz target signal (such as an IR transmission) while actively attenuating adjacent noise frequencies at 10 kHz and 17 kHz.

## System Architecture
The circuit is composed of three primary functional stages:
1. **8th-Order Sallen-Key Bandpass Filter:** Constructed using four cascaded 2nd-order stages centered at 25 kHz. This provides a steep roll-off, resulting in a measured 27.7 dB separation between the target signal and the 17 kHz noise.
2. **Envelope Peak Detector:** Utilizes an RC circuit to rectify the high-frequency AC signal and hold its peak voltage, converting it into a stable, readable DC voltage.
3. **Voltage Comparator:** An LM339 comparator evaluates the DC peak voltage against a fixed 1.0V reference, driving a physical LED indicator HIGH only when the 25 kHz signal is present.

## Repository Contents
* `Final_Project_Report.pdf`: Comprehensive engineering report detailing transfer functions, stage-by-stage gain calculations, and physical lab measurements.
* `filter_design.m`: MATLAB script used to calculate the theoretical transfer functions and generate Bode plots.
* `8th_order_filter.asc`: Complete LTspice schematic used for pre-build simulation and frequency response verification.
* `/images`: Directory containing all schematic captures, MATLAB/LTspice plots, and oscilloscope readings.
* `index.html`: The front-end code for the web portfolio display of this project.

## Software & Hardware Used
* **Simulation & Math:** LTspice, MATLAB
* **Hardware:** LM324 Op-Amps, LM339 Comparator, standard passive components (resistors, capacitors, diodes), Breadboard.
* **Lab Equipment:** Keysight Oscilloscope, Function Generator, DC Power Supply.
