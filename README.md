# Attendance System

An extremely simple attendance system built using Python

## What's Included

- Face detection using mediapipe
- Face recognition using deepface with arcface model
- Hand landmark detection though serves no purpose for now (maybe forever)
- SQLite database for recording student data and attendance data
- Simple TTS feedback using pyttsx3
- Tkinter GUI for managing students and viewing attendance data (but the attendance data is printed into terminal hehehehhehe)
- Duplicate attendance prevention, a student can only be logged once per day

## How It Works

1. The webcam continuously scans for faces
2. When a face is detected, you can verify the detected face by clicking the "Verify Student" button (when face is in frame/detected)
3. Then, DeepFace compares the detected face against registered faces in the database (a folder, "faces")
4. If a match is found, the student is logged as present for the day with a TTS confirmation
5. But if no match is found, the system announces that it was unable to recognize the face and moves on

## Notes

The "faces" folder isn't included in this repository

---

NOT vibecoded whatsoever,
Authored 100% by quandelaa