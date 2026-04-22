# Acoustic Localization System

An embedded acoustic sensing system built for **sound source localization** using multiple microphones / hydrophones, real-time sampling on the **ESP32**, analog front-end signal conditioning, and beamforming-based direction estimation.

This project combines embedded systems, analog electronics, and DSP to detect and estimate the direction of an incoming sound source.

---

## Project Overview

The system captures signals from multiple sensors placed in a known array geometry.  
Each signal is amplified through a custom analog preamplifier stage, sampled by the ESP32 ADC, and processed using beamforming algorithms to estimate the source direction.

Goal: determine **where the sound is coming from** using timing and phase differences between sensors.

---

## Features

### Embedded Processing
- ESP32-based data acquisition
- Multi-channel sensor sampling
- Real-time signal capture
- On-board processing for localization

### Analog Front-End

#### Basic Pre-Amp
<img width="1756" height="955" alt="Screenshot 2026-04-12 071518" src="https://github.com/user-attachments/assets/08809567-8dea-43f7-a023-b7da725fa56b" />

#### Characteristics

<img width="1912" height="465" alt="Screenshot 2026-04-12 071607" src="https://github.com/user-attachments/assets/e5798ce9-1624-443a-b7a5-2eb7d85c9efc" />

<img width="1919" height="467" alt="Screenshot 2026-04-12 071640" src="https://github.com/user-attachments/assets/a9755fe4-b3a5-429d-a687-66785b2032a9" />

- Custom preamplifier using fixed-bias transistor design
- Signal gain stage for weak sensor outputs
- Noise-conscious analog conditioning

### DSP / Localization
- Delay-and-sum beamforming
- Direction of Arrival (DOA) estimation
- Multi-sensor phase/time difference analysis
- Sound source angle estimation

<img width="709" height="622" alt="Screenshot 2026-04-12 054401" src="https://github.com/user-attachments/assets/7bc6ec86-6cbb-4e9a-a7c6-8ac2daeb0b7b" />

<img width="1704" height="926" alt="Screenshot 2026-04-12 063242" src="https://github.com/user-attachments/assets/3aca790e-be72-4301-a3c9-df8a3eacdfa0" />

<img width="640" height="554" alt="Screenshot 2026-04-12 064903" src="https://github.com/user-attachments/assets/45136250-9570-4ee5-8d6f-f76053230cbb" />

---

## System Architecture

```text
Sound Source
     ↓
Microphone / Hydrophone Array
     ↓
Custom Pre-Amplifier Circuit
     ↓
ESP32 ADC Sampling
     ↓
Beamforming Algorithm
     ↓
Estimated Source Direction
