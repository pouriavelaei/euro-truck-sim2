import cv2 as cv
import mediapipe as mp
import keyboard
import time
from pynput.keyboard import Controller
# باز کردن ویدیو
cap = cv.VideoCapture(0)

def resize(frame, scale=0.5):  
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    return cv.resize(frame, (width, height), interpolation=cv.INTER_AREA)

# ایجاد ماژول Mediapipe
mphands = mp.solutions.hands
hands = mphands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpdraw = mp.solutions.drawing_utils

def fingers_status(handLM, w, h):
    """
    بررسی وضعیت باز یا بسته بودن انگشت‌ها و برگرداندن نتیجه به‌صورت لیست.
    """
    tip_ids = [4, 8, 12, 16, 20]  # نقاط نوک انگشتان
    fingers = []

    # دریافت مختصات نقاط دست
    landmarks = [(int(handLM.landmark[i].x * w), int(handLM.landmark[i].y * h)) for i in range(21)]

    # بررسی انگشت شست (X محور را بررسی می‌کنیم)
    if landmarks[tip_ids[0]][0] > landmarks[tip_ids[0] - 1][0]:  # اگر x نوک شست از x مفصل آن بیشتر بود
        fingers.append(1)  # شست باز است
    else:
        fingers.append(0)  # شست بسته است

    # بررسی 4 انگشت دیگر (Y محور را بررسی می‌کنیم)
    for i in range(1, 5):
        if landmarks[tip_ids[i]][1] < landmarks[tip_ids[i] - 2][1]:  # مقایسه نوک با مفصل دوم
            fingers.append(1)  # انگشت باز است
        else:
            fingers.append(0)  # انگشت بسته است

    return fingers  # لیستی از وضعیت انگشت‌ها (0=بسته، 1=باز)

while True:
    isTrue, frame = cap.read()
    if not isTrue:
        print("End of video or error reading frame")
        break
    
    frame = resize(frame, 1.5)  # تغییر اندازه فریم
    h, w, _ = frame.shape 
    RGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  # تبدیل رنگ

    # پردازش دست‌ها
    result = hands.process(RGB)
    
    if result.multi_hand_landmarks:
        for handLM in result.multi_hand_landmarks:
            fingers = fingers_status(handLM, w, h)

            # استفاده از if برای بررسی وضعیت دست
            if fingers == [0, 0, 0, 0, 0]:  
                keyboard.write("gay")

            elif fingers == [1, 1, 1, 1, 1]:  
                keyboard.write("abol konie")
            elif fingers == [0, 1, 0, 0, 0]:  
                keyboard.write("i'm nerd")
            elif fingers == [0, 1, 1, 0, 0]:  
                print("علامت صلح ✌️")
            elif fingers == [1, 0, 0, 0, 0]:  
                print("لایک 👍")
            elif fingers == [0, 1, 1, 1, 1]:  
                print("چهار انگشت باز است 🤚")
            time.sleep(1)
        
            
            # نمایش نقاط کلیدی روی دست
            for id, lm in enumerate(handLM.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv.circle(frame, (cx, cy), 5, (0, 0, 255), cv.FILLED)
            mpdraw.draw_landmarks(frame, handLM, mphands.HAND_CONNECTIONS)

    cv.imshow("Hand Tracking", frame)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

cap.release()
cv.destroyAllWindows()
