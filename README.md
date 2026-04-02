# attendance system

a very simple attendance system built using Python

## what's included

- face detection using mediapipe
- face recognition using deepface with arcface model
- hand landmark detection though serves no purpose for now (maybe forever)
- sqlite database for recording student data and attendance data
- simple text-to-speech feedback using pyttsx3
- tkinter GUI for managing students and viewing attendance data (but the attendance data is printed into terminal hehehehhehe)
- duplicate attendance prevention, a student can only be logged once per day

## how it works

1. the webcam continuously scans for faces
2. when a face is detected, you can basically verify the face by clicking the "Verify Student" button
3. then, deepface compares the detected face against registered faces in the database (a folder "faces")
4. if a match is found, the student is logged as present for the day with a pyttsx confirmation
5. but if no match is found, the sys