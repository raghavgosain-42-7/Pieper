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
- Custom preamplifier using fixed-bias transistor design
- Signal gain stage for weak sensor outputs
- Noise-conscious analog conditioning

### DSP / Localization
- Delay-and-sum beamforming
- Direction of Arrival (DOA) estimation
- Multi-sensor phase/time difference analysis
- Sound source angle estimation

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
