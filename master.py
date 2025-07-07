import cv2 as cv
import mediapipe as mp
import keyboard
import time
from collections import Counter
import pyautogui
import win32gui
import win32con
import win32api
import win32process
import ctypes
from ctypes import wintypes
import pydirectinput

# Define structures needed for SendInput
user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004

# Key codes
VK_CODE = {
    'w': 0x57,
    'a': 0x41,
    's': 0x53,
    'd': 0x44,
    'h': 0x48,
    # You can add more keys here
}

# Define necessary structures
class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                   ("mi", ctypes.c_char * 28),
                   ("hi", ctypes.c_char * 32))
    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD),
               ("_input", _INPUT))

def send_key_with_sendinput(key):
    """
    Send key using SendInput with improved method
    """
    if key not in VK_CODE:
        return False
        
    vk_code = VK_CODE[key]
    
    # Send key down with more settings
    x = INPUT(type=INPUT_KEYBOARD, 
              ki=KEYBDINPUT(wVk=vk_code, 
                           wScan=0, 
                           dwFlags=0, 
                           time=0, 
                           dwExtraInfo=ctypes.pointer(ctypes.c_ulong(0))))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
    
    time.sleep(0.2)  # Increase key hold time
    
    # Send key up
    x = INPUT(type=INPUT_KEYBOARD, 
              ki=KEYBDINPUT(wVk=vk_code, 
                           wScan=0, 
                           dwFlags=KEYEVENTF_KEYUP, 
                           time=0, 
                           dwExtraInfo=ctypes.pointer(ctypes.c_ulong(0))))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
    
    print(f"Key sent successfully with SendInput: {key}")
    return True

def send_key_to_game(key):
    """
    Send key to game using pydirectinput
    """
    global game_focused
    try:
        print(f"Attempting to send key: {key}")
        
        # Check focus before sending key
        current_window = win32gui.GetForegroundWindow()
        if current_window != game_window:
            focus_game_window()
            time.sleep(0.1)  # Wait a bit for focus to complete
        
        # Use pydirectinput
        pydirectinput.keyDown(key)
        time.sleep(0.1)
        pydirectinput.keyUp(key)
        print(f"Key sent successfully with pydirectinput: {key}")
        return True
    except Exception as e:
        print(f"Error with pydirectinput: {e}")
        
        # Other methods as backup
        try:
            # Method 1: SendInput
            if send_key_with_sendinput(key):
                return True
                
            # Method 2: pyautogui
            pyautogui.keyDown(key)
            time.sleep(0.1)
            pyautogui.keyUp(key)
            print(f"Key sent successfully with pyautogui: {key}")
            return True
        except Exception as e2:
            print(f"Error with backup methods: {e2}")
            return False

# pyautogui settings
pyautogui.FAILSAFE = False  # Disable failsafe
pyautogui.PAUSE = 0.01  # Reduce delay

# Game window information
game_window = None
game_focused = False

def find_game_window():
    """
    Find ETS2 game window
    """
    global game_window
    try:
        # Search for various ETS2 windows
        window_titles = [
            "Euro Truck Simulator 2",
            "Euro Truck Simulator 2 - Steam",  # Add this new title
            "eurotrucks2",
            "ETS2",
            "ets2",
            "Euro Truck Simulator 2 Multiplayer",
            "ETS2MP"
        ]
        
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                for title in window_titles:
                    if title.lower() in window_text.lower():
                        windows.append((hwnd, window_text))
                        print(f"Found window: {window_text}")  # Add this line for more information
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            game_window = windows[0][0]
            print(f"✅ Game window found: {windows[0][1]}")
            return True
        else:
            print("❌ Game window not found!")
            return False
            
    except Exception as e:
        print(f"Error finding game window: {e}")
        return False

def focus_game_window():
    """
    Focus on the game window using various methods
    """
    global game_window, game_focused
    try:
        if game_window:
            # Check if the current window is already the game window
            current_window = win32gui.GetForegroundWindow()
            if current_window == game_window:
                game_focused = True
                return True
            
            # Method 1: Use SetForegroundWindow
            win32gui.ShowWindow(game_window, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(game_window)
            
            # Method 2: Use AttachThreadInput
            foreground_thread = win32process.GetWindowThreadProcessId(current_window)[0]
            target_thread = win32process.GetWindowThreadProcessId(game_window)[0]
            
            if foreground_thread != target_thread:
                win32process.AttachThreadInput(foreground_thread, target_thread, True)
                win32gui.SetForegroundWindow(game_window)
                win32gui.BringWindowToTop(game_window)
                win32process.AttachThreadInput(foreground_thread, target_thread, False)
            
            game_focused = True
            return True
    except Exception as e:
        print(f"Error in focusing: {e}")
        game_focused = False
    return False

# New variable to control display mode
show_window = True

# Open video capture
cap = cv.VideoCapture(0)
if not cap.isOpened():
    cap = cv.VideoCapture(1)

def resize(frame, scale=0.5):  
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    return cv.resize(frame, (width, height), interpolation=cv.INTER_AREA)

# Create Mediapipe module
mphands = mp.solutions.hands
hands = mphands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mpdraw = mp.solutions.drawing_utils

# Gesture smoothing variables
gesture_history = []
HISTORY_SIZE = 5
last_action_time = 0
ACTION_COOLDOWN = 0.15  # Reduce delay for better response

def fingers_status(handLM, w, h):
    """
    Check the status of fingers (open or closed)
    """
    tip_ids = [4, 8, 12, 16, 20]
    fingers = []
    landmarks = [(int(handLM.landmark[i].x * w), int(handLM.landmark[i].y * h)) for i in range(21)]

    # Thumb
    if landmarks[tip_ids[0]][0] > landmarks[tip_ids[0] - 1][0]:  
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for i in range(1, 5):
        if landmarks[tip_ids[i]][1] < landmarks[tip_ids[i] - 2][1]:  
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def get_stable_gesture(current_gesture):
    global gesture_history
    gesture_history.append(current_gesture)
    if len(gesture_history) > HISTORY_SIZE:
        gesture_history.pop(0)
    
    if len(gesture_history) >= 3:
        gesture_counts = Counter(tuple(g) for g in gesture_history)
        most_common = gesture_counts.most_common(1)[0][0]
        return list(most_common)
    return current_gesture

def execute_action(key_action):
    """
    Execute button press with focus on the game
    """
    global last_action_time, game_focused
    current_time = time.time()
    
    if current_time - last_action_time > ACTION_COOLDOWN:
        # Check current focus
        current_window = win32gui.GetForegroundWindow()
        if current_window != game_window:
            game_focused = False
            focus_game_window()
            time.sleep(0.05)  # Wait a bit for focus to complete
        
        success = send_key_to_game(key_action)
        if success:
            last_action_time = current_time
            print(f"✅ Key sent: {key_action}")
            return True
        else:
            print(f"❌ Error sending key: {key_action}")
    return False

def get_gesture_name(fingers):
    gesture_map = {
        (0, 0, 0, 0, 0): "Fist - Accelerate",
        (1, 1, 1, 1, 1): "Open Hand - Brake", 
        (0, 1, 0, 0, 0): "Index - Left",
        (0, 1, 1, 0, 0): "Two Fingers - Right",
        (1, 0, 0, 0, 0): "Thumb - Horn",
        (0, 1, 1, 1, 0): "Three Fingers - Left Signal",
        (0, 0, 1, 1, 1): "Last Three - Right Signal",
        (1, 1, 0, 0, 0): "Thumb+Index - Beacon"
    }
    return gesture_map.get(tuple(fingers), "Unknown")

print("=== ETS2 Hand Control - Improved Version ===")
print("🔍 Searching for game window...")

# Find game window
if find_game_window():
    print("✅ Game window found!")
    print("\n📋 Usage Guide:")
    print("1. First, open ETS2")
    print("2. The game should be in Windowed or Borderless mode")
    print("3. Place your hand in front of the camera")
    print("4. For best results, ensure adequate lighting")
    print("\n🎮 Controls:")
    print("🤛 Closed fist: Accelerate")
    print("🖐️ Open hand: Brake")
    print("👆 Index finger: Left")
    print("✌️ Two fingers: Right")
    print("👍 Thumb: Horn")
    print("\nPress 'q' to exit")
    print("=" * 50)
else:
    print("❌ Please open ETS2 first!")
    print("📌 Note: The game should be in Windowed mode")
    input("Press Enter to continue...")

# Start main loop
focus_game_window()  # Initial focus

cv.namedWindow("ETS2 Hand Control", cv.WINDOW_NORMAL)
# Set window to always on top
cv.setWindowProperty("ETS2 Hand Control", cv.WND_PROP_TOPMOST, 1)

while True:
    isTrue, frame = cap.read()
    if not isTrue:
        break
    
    frame = cv.flip(frame, 1)
    frame = resize(frame, 1.2)
    h, w, _ = frame.shape 
    RGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    result = hands.process(RGB)
    
    status_text = "No hand detected"
    action_text = ""
    
    if result.multi_hand_landmarks:
        for handLM in result.multi_hand_landmarks:
            fingers = fingers_status(handLM, w, h)
            stable_fingers = get_stable_gesture(fingers)
            gesture_name = get_gesture_name(stable_fingers)
            
            status_text = f"Gesture: {gesture_name}"
            
            action_executed = False
            
            # Accelerate - Closed fist
            if stable_fingers == [0, 0, 0, 0, 0]:
                action_executed = execute_action("w")
                action_text = ">> Accelerate!" if action_executed else ""
                
            # Brake - Open hand
            elif stable_fingers == [1, 1, 1, 1, 1]:
                action_executed = execute_action("s")
                action_text = "|| Brake!" if action_executed else ""
                
            # Left - Index finger
            elif stable_fingers == [0, 1, 0, 0, 0]:
                action_executed = execute_action("a")
                action_text = "<- Left!" if action_executed else ""
                
            # Right - Two fingers
            elif stable_fingers == [0, 1, 1, 0, 0]:
                action_executed = execute_action("d")
                action_text = "-> Right!" if action_executed else ""
                
            # Horn - Thumb
            elif stable_fingers == [1, 0, 0, 0, 0]:
                action_executed = execute_action("h")
                action_text = "* Horn!" if action_executed else ""
            
            # Draw hand
            mpdraw.draw_landmarks(frame, handLM, mphands.HAND_CONNECTIONS)
            
            # Display fingers
            for i, finger_status in enumerate(fingers):
                color = (0, 255, 0) if finger_status == 1 else (0, 0, 255)
                cv.circle(frame, (30 + i * 30, 40), 12, color, -1)
    
    # Display status
    cv.putText(frame, status_text, (10, h - 50), 
              cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    if action_text:
        cv.putText(frame, action_text, (10, h - 20), 
                  cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Display focus status
    focus_color = (0, 255, 0) if game_focused else (0, 0, 255)
    cv.putText(frame, f"Game Focus: {'ON' if game_focused else 'OFF'}", 
              (w - 150, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, focus_color, 2)

    if show_window:
        cv.imshow("ETS2 Hand Control", frame)
    else:
        cv.destroyWindow("ETS2 Hand Control")
    
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('f'):  # Press F to refocus
        focus_game_window()
    elif key == ord('h'):  # Press H to hide/show window
        show_window = not show_window
        if show_window:
            cv.namedWindow("ETS2 Hand Control", cv.WINDOW_NORMAL)
            cv.setWindowProperty("ETS2 Hand Control", cv.WND_PROP_TOPMOST, 1)

cap.release()
cv.destroyAllWindows()
print("ETS2 Hand Control stopped!")