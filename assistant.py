import cv2
from ultralytics import YOLO
from gtts import gTTS
from playsound import playsound
import os
import tempfile
import time
import threading
import sys
from queue import Queue
from collections import Counter

# -------------------------------
# LANGUAGE
# -------------------------------
LANG = sys.argv[1] if len(sys.argv) > 1 else "en"
print(f"[INFO] Language set to: {LANG}")

# استدعاء الترجمة من trans.py
from trans import t as _t
def t(key):
    return _t(key, LANG)

# -------------------------------
# LOAD MODEL
# -------------------------------
model = YOLO("yolov8n.pt")

# -------------------------------
# VOICE SYSTEM
# -------------------------------
speech_queue = Queue()

def speech_worker():
    while True:
        try:
            text = speech_queue.get(timeout=1)
            while not speech_queue.empty():
                text = speech_queue.get_nowait()

            print(f"[VOICE] Saying: {text}")
            tts = gTTS(text=text, lang=LANG)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
                tmp_path = f.name
            tts.save(tmp_path)
            playsound(tmp_path)
            os.remove(tmp_path)
        except Exception as e:
            if "Empty" not in str(type(e).__name__):
                print(f"[VOICE ERROR] {e}")

threading.Thread(target=speech_worker, daemon=True).start()

# -------------------------------
# SPEECH CONTROL
# -------------------------------
last_spoken_time = 0
last_spoken_message = ""
history = []
history_size = 5
REPEAT_INTERVAL = 4
STABILITY_THRESHOLD = 3
SIMILARITY_THRESHOLD = 0.15

# -------------------------------
# DISTANCE ZONES
# -------------------------------
def estimate_distance(area):
    if area > 80000:
        return "very close, stop"
    elif area > 40000:
        return "close"
    elif area > 15000:
        return "nearby"
    else:
        return "far"

# -------------------------------
# CAMERA
# -------------------------------
cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()
    if not success:
        break

    results = model(frame, conf=0.5)
    annotated_frame = results[0].plot()
    frame_height, frame_width, _ = frame.shape

    detected_objects = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            object_name = model.names[class_id]
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
            area = (x2 - x1) * (y2 - y1)
            center_x = (x1 + x2) / 2

            if center_x < frame_width / 3:
                direction = "Right"
            elif center_x > 2 * frame_width / 3:
                direction = "Left"
            else:
                direction = "Front"

            distance = estimate_distance(area)

            detected_objects.append({
                "name":      object_name,
                "area":      area,
                "direction": direction,
                "distance":  distance,
                "box":       (x1, y1, x2, y2)
            })

    if len(detected_objects) > 0:

        detected_objects.sort(key=lambda obj: obj["area"], reverse=True)

        nearest = detected_objects[0]
        largest_area = nearest["area"]

        close_objects = [nearest]
        for obj in detected_objects[1:]:
            diff = abs(largest_area - obj["area"]) / largest_area
            if diff <= SIMILARITY_THRESHOLD:
                close_objects.append(obj)
            else:
                break

        # show on screen — English always
        for i, obj in enumerate(close_objects):
            cv2.putText(
                annotated_frame,
                f"{obj['name']} | {obj['direction']} | {obj['distance']}",
                (20, 40 + i * 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2
            )

        # spoken message — translated
        if len(close_objects) == 1:
            obj = close_objects[0]
            spoken = f"{t(obj['name'])}, {t(obj['direction'])}, {t(obj['distance'])}"
            current_key = (obj['name'], obj['direction'], obj['distance'])
        else:
            parts = [f"{t(obj['name'])} {t(obj['direction'])} {t(obj['distance'])}" for obj in close_objects]
            spoken = f"{t('Careful')}, " + f" {t('and')} ".join(parts)
            current_key = tuple(sorted([(o['name'], o['direction'], o['distance']) for o in close_objects]))

        history.append(current_key)
        if len(history) > history_size:
            history.pop(0)

        most_common_key = Counter(history).most_common(1)[0][0]
        is_stable = history.count(most_common_key) >= STABILITY_THRESHOLD

        current_time = time.time()
        is_new_message = spoken != last_spoken_message
        enough_time_passed = (current_time - last_spoken_time > REPEAT_INTERVAL)

        if is_stable and (is_new_message or enough_time_passed):
            print(">>> SPEAKING:", spoken)
            speech_queue.put(spoken)
            last_spoken_time = current_time
            last_spoken_message = spoken

    else:
        history.clear()

    cv2.imshow("Smart Blind Assistant", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()