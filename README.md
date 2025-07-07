# 🚚 Hand Detection for Euro Truck Simulator 2 (ETS2)

Control **Euro Truck Simulator 2** using real-time hand gestures via your webcam!
This project uses [MediaPipe](https://google.github.io/mediapipe/) for gesture detection and maps those gestures to in-game keyboard inputs.

---

## 📦 Features

- Real-time hand tracking via webcam
- Gesture-based driving: accelerate, brake, steer, signal & more
- Direct keyboard input into ETS2 using `pydirectinput`
- Simple UI overlay to visualize hand input

---

## 🧰 Prerequisites

- **Python 3.10** (recommended)
- **Webcam**
- **Euro Truck Simulator 2** (installed and running)

---

## ⚙️ Installation

1. **Clone the repository**:

```bash
git clone https://github.com/pouriavelaei/euro-truck-sim2.git
cd euro-truck-sim2
```

2. **Install dependencies**:

```bash
pip install opencv-python mediapipe keyboard pyautogui pydirectinput pywin32
```

---

## ▶️ How to Run

1. **Launch ETS2**

   > Make sure it's in **Windowed** or **Borderless** display mode.
   >
2. **Run the script**:

```bash
python master.py
```

3. A window titled **"ETS2 Hand Control"** will appear. Place your hand in front of the camera and begin driving!

---

## ✋ Hand Gesture Controls

| Gesture                           | Action       | Key Simulated     |
| --------------------------------- | ------------ | ----------------- |
| ✊ Closed Fist                    | Accelerate   | `W`             |
| 🖐️ Open Hand                    | Brake        | `S`             |
| 👆 Index Finger Only              | Turn Left    | `A`             |
| ✌️ Two Fingers (Index + Middle) | Turn Right   | `D`             |
| 👍 Thumb Up                       | Horn         | `H`             |
| ☝️ Index + Middle + Ring        | Left Signal  | `[`             |
| 🤟 Middle + Ring + Pinky          | Right Signal | `]`             |
| 👉 Thumb + Index                  | Beacon       | `O` (or custom) |

---

## ❌ Exiting

Press **`q`** to quit the application.

---

## 🛠️ Troubleshooting

- **"❌ Game window not found!"**

  - Make sure ETS2 is running in **Windowed** or **Borderless** mode.
  - Supported titles: `"Euro Truck Simulator 2"`, `"Euro Truck Simulator 2 - Steam"`, `"eurotrucks2"`, etc.
- **Game Not Responding to Gestures**

  - Press **`F`** to refocus the ETS2 window.
- **Toggle Control Window**

  - Press **`H`** to hide/show the webcam overlay.

---

## 📄 License

MIT License © [Pouria Velaei](https://github.com/pouriavelaei)

---

Enjoy hands-free trucking! 🛣️
