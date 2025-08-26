import cv2
import time
import keyboard
import mediapipe as mp
import numpy as np
from threading import Thread

# ---------------- MULTITHREADED CAMERA ---------------- #
class VideoCaptureAsync:
    def __init__(self, src=0, width=640, height=360):
        self.cap = cv2.VideoCapture(src, cv2.CAP_DSHOW)  # DSHOW prevents lag on Windows
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # always keep latest frame

        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = False

    def start(self):
        if self.started:
            return None
        self.started = True
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            if grabbed:
                self.grabbed, self.frame = grabbed, frame

    def read(self):
        return self.grabbed, self.frame.copy()

    def stop(self):
        self.started = False
        self.cap.release()

# ---------------- KEYBOARD CONTROL ---------------- #
def execute(move):
    if move == "JUMP":
        keyboard.press_and_release("up")
    elif move == "LEFT":
        keyboard.press_and_release("left")
    elif move == "RIGHT":
        keyboard.press_and_release("right")
    elif move == "ROLL":
        keyboard.press_and_release("down")
    elif move == "START":
        keyboard.press_and_release("space")

def put_text_in_polygon(frame, pts, text, color=(255,255,255)):
    M = cv2.moments(pts)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        cx, cy = pts[0][0]
    cv2.putText(frame, text, (cx-20, cy), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, color, 2, cv2.LINE_AA)

def play_move(frame, index_tip, last_played, is_start):
    h,w,_ = frame.shape
    xc,yc = index_tip
    move = None

    if not is_start:
        if 3*w//8 < xc < 5*w//8 and 3*h//8 < yc < 5*h//8:
            move = "START"
        else:
            move = "NOT_STARTED"
    else:
        if xc <= w//4:
            if yc <= h//4:
                move = "JUMP" if yc/xc < h/w else "LEFT"
            elif h//4 < yc < 3*h//4:
                move = "LEFT"
            else:
                move = "ROLL" if (yc-h)/xc >= -1*(h/w) else "LEFT"
        elif w//4 < xc < 3*w//4:
            if yc <= h//4: move = "JUMP"
            elif yc >= 3*h//4: move = "ROLL"
            else: move = "STILL"
        else:
            if yc <= h//4:
                move = "JUMP" if yc/(xc-w) >= -1*(h/w) else "RIGHT"
            elif yc >= 3*h//4:
                move = "ROLL" if (yc-h)/(xc-w) < -1*(h/w) else "RIGHT"
            else:
                move = "RIGHT"

    if move != last_played and move not in ["STILL", "NOT_STARTED", "NO_HAND"]:
        execute(move)
    if move == "START":
        print("THE GAME HAS STARTED... ENJOY..")
        return "STILL"
    return move

# ---------------- MAIN GAME ---------------- #
def subway_surfer_player():
    prev_time = 0

    video_capture = VideoCaptureAsync(0, 640, 360).start()

    mp_hands = mp.solutions.hands
    hands_detector = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    mp_draw = mp.solutions.drawing_utils

    last_played = "NOT_STARTED"
    is_start = False

    while True:
        success, frame = video_capture.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)  # mirror
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands_detector.process(rgb_image)

        h, w, _ = frame.shape
        index_tip = (0,0)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            lm = hand_landmarks.landmark[8]
            index_tip = (int(lm.x * w), int(lm.y * h))
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        else:
            last_played = "NO_HAND"
            cv2.imshow('CONTROL PANEL FOR SUBWAY SURFERS', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if curr_time != prev_time else 0
        prev_time = curr_time

        overlay = frame.copy()
        if not is_start:
            pts_start = np.array([
                [3*w//8, 3*h//8],
                [5*w//8, 3*h//8],
                [5*w//8, 5*h//8],
                [3*w//8, 5*h//8]
            ], np.int32)

            cv2.fillPoly(overlay, [pts_start], color=(0,0,0))
            frame = cv2.addWeighted(overlay, 0.2, frame, 0.8, 0)
            put_text_in_polygon(frame, pts_start, "START", (0,0,0))

            curr_played = play_move(frame, index_tip, last_played, is_start)
            last_played = curr_played
            if curr_played == "STILL":
                is_start = True
        else:
            pts_jump = np.array([[0,0],[w,0],[3*w//4,h//4],[w//4,h//4]], np.int32)
            pts_left = np.array([[0,0],[w//4,h//4],[w//4,3*h//4],[0,h]], np.int32)
            pts_roll = np.array([[w//4,3*h//4],[3*w//4,3*h//4],[w,h],[0,h]], np.int32)
            pts_right = np.array([[3*w//4,h//4],[w,0],[w,h],[3*w//4,3*h//4]], np.int32)

            cv2.fillPoly(overlay, [pts_jump], color=(0,0,255))
            cv2.fillPoly(overlay, [pts_left], color=(0,255,255))
            cv2.fillPoly(overlay, [pts_right], color=(0,255,0))
            cv2.fillPoly(overlay, [pts_roll], color=(255,0,0))

            frame = cv2.addWeighted(overlay, 0.2, frame, 0.8, 0)

            cv2.putText(frame, f"FPS : {int(fps)}", (10,30),
                        cv2.FONT_ITALIC, 1, (255,255,255), 2)
            put_text_in_polygon(frame, pts_jump, "JUMP", (0,0,255))
            put_text_in_polygon(frame, pts_left, "LEFT", (0,255,255))
            put_text_in_polygon(frame, pts_right, "RIGHT", (0,255,0))
            put_text_in_polygon(frame, pts_roll, "ROLL", (255,0,0))

            curr_played = play_move(frame, index_tip, last_played, is_start)
            last_played = curr_played

        cv2.imshow('CONTROL PANEL FOR SUBWAY SURFERS', frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or keyboard.is_pressed('q'):
            break

    video_capture.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    subway_surfer_player()
