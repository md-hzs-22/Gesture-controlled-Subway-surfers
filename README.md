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
   python handTracker.py
   ```

##### Note : This will run on websites like `poki.com` so start it in a browser window and then run the hand tracker file.
---

## 🖥 Requirements
- Python 3.8+
- Webcam
- Windows/Linux (tested on Windows)

---

## 🎥 Demo

The following demo shows how if i move my index finger from one region to another, the move is changed. This will be shown in the console.


*(Add screenshots or a GIF of the game being controlled by hand gestures)*

Note : Your `Index finger` must be in the region to trigger the action. To trigger it again, or to trigger it two times in a row, take the finger to the still region and then again to the desired region. Still region is the ucolored region.
---

## 🚀 Future Improvements
- Add support for more gestures.
- Train a custom gesture model.
- Cross-platform compatibility (MacOS).

---
