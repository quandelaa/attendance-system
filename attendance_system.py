# attendance_system.py of the attendance system

import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import cv2 as cv
import mediapipe as mp
from deepface import DeepFace
import threading

face_detections = None
face_crop = None
findings = None

find_face_running = threading.Event()
upd_event = threading.Event()
upd_lock = threading.Lock()

def reset_findings():
    global findings

    with upd_lock:
        findings = None

def get_data_func():
    with upd_lock:
        return face_detections, face_crop, findings 

def find_matching_face(face):
    global findings, upd_event, find_face_running

    try:
        find_face_running.set()

        results = DeepFace.find(img_path=face, db_path="attendance_system/faces", model_name="ArcFace", enforce_detection=False, detector_backend="skip", distance_metric="cosine")
    except Exception as e:
        print(f"No item found in db {e}")
        return
        
    find_face_running.clear()

    with upd_lock:
        findings = results
        upd_event.set()

def attendance_system_func():
    global face_detections, face_crop

    webcam = cv.VideoCapture(0)
    mp_face_detect = mp.solutions.face_detection
    mp_hands_detect = mp.solutions.hands

    with mp_face_detect.FaceDetection(model_selection=0, min_detection_confidence=0.8) as face_detection, mp_hands_detect.Hands(model_complexity=0, min_detection_confidence=0.75, min_tracking_confidence=0.75) as hands_detection:
        while True:
            ret, frame = webcam.read()
            if not ret:
                break

            H, W, _ = frame.shape

            rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            rgb.flags.writeable = False
            process = face_detection.process(rgb)
            hands_process = hands_detection.process(rgb)

            with upd_lock:
                face_detections = process.detections

            if process.detections:
                for detection in process.detections:
                    bbox = detection.location_data.relative_bounding_box
                    confidence = detection.score[0]

                    y1, x1, w1, h1 = bbox.ymin, bbox.xmin, bbox.width, bbox.height

                    y2 = int(y1*H)
                    x2 = int(x1*W)
                    w2 = int(w1*W)
                    h2 = int(h1*H)

                    with upd_lock:
                        face_crop = rgb[y2:y2+h2, x2:x2+w2].copy()

                    cv.rectangle(frame, (x2, y2), (x2+w2, y2+h2), (0,255,0), 2)

                    for keypoint in detection.location_data.relative_keypoints:
                        x4, y4 = int(keypoint.x*W), int(keypoint.y*H)

                        cv.rectangle(frame, (x4, y4), (x4+1, y4+1), (0,255,0), 2)

                    cv.putText(frame, f"{(float(confidence)*100):.2f}%", (x2, y2-15), thickness=2, lineType=cv.LINE_AA, fontFace=cv.FONT_HERSHEY_SCRIPT_SIMPLEX, fontScale=w1 * 3, color=(0,255,0))

            if hands_process.multi_hand_landmarks:
                for hand_landmarks in hands_process.multi_hand_landmarks:

                    for landmark in hand_landmarks.landmark:
                        y3, x3 = int(landmark.y*H), int(landmark.x*W)
                            
                        cv.rectangle(frame, (x3, y3), (x3+3, y3+3), (0,255,0), 2)

            cv.imshow('Webcam', frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            
        webcam.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    attendance_system_func()