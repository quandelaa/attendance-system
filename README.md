# Simple Attendance System

An attendance system project that uses face recognition. Built with Python.

## Features

- Face detection running at all times via webcam using MediaPipe
- Face recognition using DeepFace (specifically the ArcFace model)
- Adding students with their credentials (name, age, unique student id)
- Disallows adding student if the inputted student id has a duplicate
- Automatic attendance logging and prevents duplicate entries per day
- TTS feedback for logging in or adding students
- SQLite database for keeping record of student data and attendance data
- Tkinter GUI

## Requirements

- Python 3.12>=
- Working webcam

Install dependencies:

```bash
pip install opencv-python mediapipe deepface pillow pyttsx3
```

## How It Works

### 1. Registering a Student

Fill in the student's credentials (all required), then click the "Capture" button. If the system detects a face from the webcam, it will save a screenshot into the `faces/` folder alongside their name as the file name. 

<img width="1016" height="512" alt="SHIDKDKS" src="https://github.com/user-attachments/assets/093f9aaf-4487-433d-8c4e-b2604286f557" />

### 2. Verifying / Logging Attendance

Click the "Verify Student" button, and if the system detects a face from the current webcam frame, it will take the same screenshot as when registering a student, and compares it against all registered faces in the `faces/` folder using ArcFace.

### 3. Match Found

If a match is found, the student's name is announced via TTS and their attendance is logged with the current timestamp (date and time). If they have already been logged today, the system will notify you instead of creating a duplicate entry.

### 4. Viewing Attendance Records

- Click the "Get All Students" to print all registered students' credentials to the console.
<img width="207" height="21" alt="allstudents" src="https://github.com/user-attachments/assets/451c9599-17c8-4de8-b034-311367e54797" />
  
- Enter a student ID and click the "Get Student Attendance Data" button to print that student's full attendance history.
<img width="225" height="18" alt="studnetid" src="https://github.com/user-attachments/assets/082a33a9-6238-46c3-8401-faec87cc5fbf" />

## Usage

```bash
python attendance_system_gui.py
```

The webcam window will open automatically alongside the GUI. Press `q` in the webcam window to quit.

## Database

The system uses a local SQLite database `attendance.db` with two tables:

- "students" — stores students' credentials (name, age, unique id),
- "attendance" — stores timestamps for each time a student logs in

## Notes

- The `faces/` directory must exist before running (create it manually if not yet)
- Face images are saved as `FirstName_LastName.png` based on the name entered
- TTS feedback runs in a seperate thread to avoid blocking the UI

---

**NOT vibecoded. Entirely by quandelaa**
