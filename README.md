# Hand Gesture Controlled Subway Surfers

A Python project that lets you play **Subway Surfers** (or similar keyboard-controlled games) using **hand gestures** captured from a webcam.  
It uses **OpenCV**, **MediaPipe Hands**, and multithreading for smooth real-time gesture detection and game control.

---

## ✨ Features
- 🎥 **Multithreaded camera capture** for low-latency video processing.  
- ✋ **Real-time hand gesture recognition** using MediaPipe.  
- 🎮 **Keyboard emulation** to map gestures (Jump, Roll, Left, Right, Start) into game actions.  
- 📊 Live **FPS counter** for performance monitoring.  

---

## 🎮 Gesture Mapping
| Gesture Region | Action  |
|----------------|---------|
| Top            | Jump    |
| Bottom         | Roll    |
| Left           | Move Left |
| Right          | Move Right |
| Center (Start) | Start the Game |

---

## ⚡ Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/md-hzs-22/Gesture-controlled-Subway-surfers.git
   cd Gesture-controlled-Subway-surfers
   ```
2. Install dependencies:
   ```bash
   pip install opencv-python mediapipe numpy keyboard
   ```
3. Run the program:
   ```bash
   python main.py
   ```

---

## 🖥 Requirements
- Python 3.8+
- Webcam
- Windows/Linux (tested on Windows)

---

## 🎥 Demo
*(Add screenshots or a GIF of the game being controlled by hand gestures)*

---

## 🚀 Future Improvements
- Add support for more gestures.
- Train a custom gesture model.
- Cross-platform compatibility (MacOS).

---
