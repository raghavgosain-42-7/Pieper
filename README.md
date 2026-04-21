# Pieper: All-in-One Underwater Acoustic System
<img width="747" height="551" alt="Screenshot 2026-04-08 224853" src="https://github.com/user-attachments/assets/49509e45-204e-4c5b-9072-ee8a48f8dded" />

## Overview

Pieper is a compact, modular underwater acoustic system designed for **localization, communication, and signal processing** using hydrophones. It integrates multi-channel acquisition, beamforming, and inter-vehicle communication into a single board.

The system is built around a **multi-hydrophone array**, high-speed ADC sampling, and an embedded processing unit (Rockchip-class SoC preferred) with Ethernet connectivity.

---

## Key Features

* 🎯 **3-Hydrophone Array for Localization**

  * Time Difference of Arrival (TDOA)-based direction finding
  * Supports beamforming and steering vector computation

* 📡 **2-Hydrophone Communication Channel**

  * Dedicated pair for inter-vehicle acoustic communication
  * Frequency-selective signaling and decoding

* ⚡ **High-Speed ADC Sampling**

  * Simultaneous multi-channel acquisition
  * Designed for phase-coherent sampling

* 🧠 **Onboard Processing (Rockchip or Equivalent)**

  * Real-time signal processing
  * Beamforming, filtering, and decoding

* 🌐 **Ethernet Interface**

  * Data streaming to external systems
  * Remote control and monitoring

---

## System Architecture

```
        [ Hydrophone Array (3) ]
                 |
         [ Analog Front End ]
                 |
         [ Multi-Channel ADC ]
                 |
        -----------------------
        |                     |
[ Rockchip Processor ]   [ Comm Hydrophones (2) ]
        |
  [ Beamforming + DSP ]
        |
     [ Ethernet ]
```

---

## Core Functionalities

### 1. Acoustic Localization

* Uses **TDOA (Time Difference of Arrival)** between 3 hydrophones
* Computes direction of arrival (DOA)
* Supports narrowband and broadband beamforming

### 2. Beamforming

* Delay-and-sum beamforming implementation
* Steering vector-based directional enhancement
* Noise suppression and spatial filtering

### 3. Inter-Vehicle Communication

* Separate hydrophone pair for communication
* Frequency-based signaling (FSK/PSK extensible)
* Robust decoding in noisy underwater environments

### 4. Signal Processing Pipeline

* Band-pass filtering
* Amplification and conditioning
* Sampling → Digital processing → Feature extraction

---

## Hardware Design

### Analog Front End

* Low-noise preamplifiers
* Band-pass filters tuned to target frequency range
* Impedance matching for hydrophones

### ADC Requirements

* Minimum 3 synchronized channels (localization)
* Additional channels for communication
* High sampling rate (depending on acoustic band)

### Processing Unit

* Rockchip SoC (or equivalent ARM-based SBC)
* Capable of handling:

  * FFT
  * Cross-correlation
  * Real-time DSP

### Networking

* Ethernet switch for:

  * Data streaming
  * Multi-device synchronization

---

## Software Stack

* Embedded Linux (preferred)
* DSP pipeline written in C/C++ or Python
* Modules:

  * Signal acquisition
  * Filtering
  * TDOA estimation
  * Beamforming
  * Communication decoding

---

## Applications

* Autonomous underwater vehicles (AUVs)
* Swarm robotics communication
* Acoustic localization systems
* Research in underwater acoustics

---

## Future Improvements

* Adaptive beamforming (MVDR, MUSIC)
* Machine learning-based signal classification
* Higher hydrophone count for better resolution
* FPGA-based real-time acceleration

---

## Status

🚧 In development

---

## Author

Raghav Gosain

---

## License

MIT License (or TBD)
