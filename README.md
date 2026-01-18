# Hand Tracking Cursor Control ✋🖱️

Control your mouse using **hand gestures** via **OpenCV + MediaPipe + PyAutoGUI**.  
This project turns your webcam into a real-time hand-based mouse controller supporting:

- Cursor movement  
- Left / right click  
- Double click  
- Drag & drop  
- Scroll  

---

## Features

- 🖱️ **Move cursor** using thumb position
- 👆 **Left click** – thumb + index finger pinch
- 👉 **Right click** – thumb + middle finger pinch
- 🧲 **Drag & drop** – sustained pinch
- 🧾 **Scroll** – 4 fingers up + thumb–ring gesture
- 🎯 Cursor smoothing and sensitivity scaling
- 🛑 Safe mouse release on exit

---

## Requirements

- Python **3.11+**
- Webcam

### Python dependencies
- opencv-python
- mediapipe==0.10.13
- pyautogui
- numpy

---

## Installation

```bash
git clone https://github.com/your-username/Hand_Tracking_Game.git
cd Hand_Tracking_Game
```
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python hand_cursor.py
```
Press `q` to quit safely.

## Gesture Controls
### Cursor Movement
- Move thumb to move the cursor
- Sensitivity can be adjusted:
```bash
sensitivity = 2
```

### Left Click
- Pinch thumb + index finger
- Double pinch quickly → double click

### Right Click
- Pinch thumb + middle finger
- Double pinch → right double click

### Drag & Drop
- Hold thumb + index finger at mid distance
- Move hand to drag
- Release pinch to drop

### Scroll
- Show 4 fingers
- Touch thumb + ring finger
- Move index finger:
- Up → scroll up
- Down → scroll down

## Safety Notes
- PyAutoGUI has a built-in failsafe (mouse to screen corner)
- Program releases mouse buttons on exit
- If mouse gets stuck:
  - Press q
  - Or move mouse to a screen corner

## File Structure
```bash
Hand_Tracking_Game/
│
├── hand_cursor.py
├── util.py
├── requirements.txt
├── README.md
└── venv/        # Not tracked by Git
```

## Known Limitations
- Single-hand tracking only
- Gesture jitter possible at low FPS
- Designed for experimentation, not production use

## Future Improvements
- Gesture calibration UI
- Adaptive sensitivity
- Multi-hand support
- Gesture-based keyboard input
- Better smoothing using velocity prediction

## Disclaimer
This project directly controls your system mouse.
Use responsibly and terminate immediately if behavior becomes unstable.
