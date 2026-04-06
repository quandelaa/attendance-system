# Attendance System

An attendance system project that uses face recognition. Built with Python.

## Features

- Face detection running at all times via webcam using MediaPipe
- Face recognition using DeepFace (specifically the ArcFace model)
- Tkinter GUI
- Adding students with their credentials (name, age, unique student id)
- SQLite database for keeping record of student data and attendance data
- Automatic attendance logging and prevents duplicate entries per day
- TTS feedback for logging in or adding students
- Disallows adding a student if the inputted "student id" or "age" is not more than 0
- Disallows adding a student if the inputted "student id" has a duplicate

## Requirements

- Python >= 3.12
- Working webcam

Install dependencies:

```bash
pip install opencv-python mediapipe deepface pillow pyttsx3
```
## Usage

```bash
python attendance_system_gui.py
```

The webcam window will open automatically alongside the GUI. Press `q` in the webcam window to quit.

## How It Works

### 1. Registering a Student

Fill in the student's credentials (all required), then click the "Capture" button. If the system detects a face from the current webcam frame, it will save a screenshot into the `faces/` folder alongside their name as the file name. 

### 2. Verifying / Logging Attendance

Click the "Verify Student" button, and if the system detects a face from the current webcam frame, it will take a screenshot, and compares it against all registered faces in the `faces/` folder using ArcFace.

### 3. Match Found

If a match is found, the student's name is announced via TTS and their attendance is logged with the current timestamp (time is in UTC). If they have already been logged today, the system will notify you instead of creating a duplicate entry.

### 4. Viewing Attendance Records

- Click the "Get All Students" to print all registered students' credentials to the console.

or

- Enter a student ID and click the "Get Student Attendance Data" button to print that student's full attendance history.

## Database

The system uses a local SQLite database `attendance.db` with two tables:

- "students" — stores students' credentials (name, age, unique id),
- "attendance" — stores timestamps for each time a student logs in

## Screenshots

- Attendance System Manager window:
<img width="374" height="508" alt="attendance_sstem_anager" src="https://github.com/user-attachments/assets/e129d8b9-2919-4f50-b63f-f54e5f33155f" />

- Webcam window:
<img width="642" height="517" alt="webcamss" src="https://github.com/user-attachments/assets/7d88e374-b800-43d7-abc5-e0791855f6e3" />
lol brian kernighan

## Notes

- The `faces/` directory must exist before running (create it manually if not yet)
- Face images are saved as `FirstName_LastName.png` based on the name entered

---

- **NOT vibecoded. Entirely by quandelaa.**
- **There may still be some bugs (and TTS is still pretty unclear), so I'll appreciate contributions!!**
