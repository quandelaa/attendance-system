# attendance_system_gui.py of the attendance system

import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

from attendance_system import find_matching_face, get_data_func, reset_findings, attendance_system_func
from student_db import add_student, init, get_students, get_student_id_for_logging, get_student
from tkinter import messagebox
from pathlib import Path
import attendance_system
from PIL import Image
import tkinter as tk
import threading
import pyttsx3

class AttendanceSystem:
    def __init__(self, window_frame):
        self.window = window_frame

        self.SEC_COLOR = "#FFFFFF"
        self.MAIN_COLOR = "#000000"
        self.font = ("Verdana", 18)

        self.running = threading.Event()

        self.findings = None
        self.face_detections = None
        self.name = None
        self.face_crop = None
        
        attendance_system_thread = threading.Thread(target=self.att_system_thread, daemon=True)
        attendance_system_thread.start()

        get_findings_thread = threading.Thread(target=self.get_findings, daemon=True)
        get_findings_thread.start()

        self.setup_gui()

    def setup_gui(self):
        self.window.title("attendance System")
        self.window.config(background="#000000")
        
        name_text = tk.Label(self.window, text="Name: ", font=self.font, bg=self.MAIN_COLOR, fg=self.SEC_COLOR)
        self.name_entry = tk.Entry(self.window, font=self.font, bg=self.MAIN_COLOR, fg=self.SEC_COLOR, width=18)
        
        age_text = tk.Label(self.window, text="Age: ", font=self.font, bg=self.MAIN_COLOR, fg=self.SEC_COLOR)
        self.age_entry = tk.Entry(self.window, font=self.font, bg=self.MAIN_COLOR, fg=self.SEC_COLOR, width=18)

        id_text = tk.Label(self.window, text="Student ID: ", font=self.font, bg=self.MAIN_COLOR, fg=self.SEC_COLOR)
        self.id_num = tk.Entry(self.window, font=self.font, bg=self.MAIN_COLOR, fg=self.SEC_COLOR, width=18)

        capture_button = tk.Button(self.window, text="Capture", font=self.font, fg=self.SEC_COLOR, bg=self.MAIN_COLOR, command=self.get_data)
        verify_button = tk.Button(self.window, text="Verify Student", font=self.font, fg=self.SEC_COLOR, bg=self.MAIN_COLOR, command=self.verify_face)

        student_id_text = tk.Label(self.window, text="Student ID: ", font=self.font, bg=self.MAIN_COLOR, fg=self.SEC_COLOR)
        self.student_id_add_data = tk.Entry(self.window, font=self.font, bg=self.MAIN_COLOR, fg=self.SEC_COLOR, width=18)    
        get_att_button = tk.Button(self.window, text="Get Student Attendance Data", font=self.font, fg=self.SEC_COLOR, bg=self.MAIN_COLOR, command=self.get_student_att_data)
        
        get_button = tk.Button(self.window, text="Get All Students", font=self.font, fg=self.SEC_COLOR, bg=self.MAIN_COLOR, command=self.get_students_data)

        name_text.pack()
        self.name_entry.pack()
        age_text.pack()
        self.age_entry.pack()
        id_text.pack()
        self.id_num.pack()
        capture_button.pack()
        verify_button.pack()
        get_button.pack()
        student_id_text.pack()
        self.student_id_add_data.pack()
        get_att_button.pack()

    def get_data(self):
        self.face_detections, self.face_crop, _ = get_data_func()
        self.name = self.name_entry.get()

        if self.face_detections is not None:
            self.save_image(self.face_crop)
        else:
            tts_thread = threading.Thread(target=self.tts, daemon=True, args=("Did not detect any faces",))
            tts_thread.start()

    def verify_face(self):
        self.face_detections, self.face_crop, _ = get_data_func()

        if self.face_detections is not None and not attendance_system.find_face_running.is_set():
            verify_face_thread = threading.Thread(target=find_matching_face, args=(self.face_crop.copy(),), daemon=True)        
            verify_face_thread.start()
        elif self.face_detections is None:
            tts_thread = threading.Thread(target=self.tts, daemon=True, args=("No faces seems to match",))
            tts_thread.start()
        elif attendance_system.find_face_running.is_set():
            tts_thread = threading.Thread(target=self.tts, daemon=True, args=("A previous verify scan is still running, please wait..",))
            tts_thread.start()

    def save_image(self, face_crop):
        if not self.name or face_crop is None:
            return

        modified_name = self.name.replace(' ', '_')
        
        try:
            id_num_to_give = int(self.id_num.get())
            age_to_give = int(self.age_entry.get())
            if id_num_to_give < 1 or age_to_give < 1:
                raise ValueError("ID and age has to be greater than 0")

            add_student(student_id=id_num_to_give, name=self.name, age=age_to_give)
        except Exception as e:
            tts_thread1 = threading.Thread(target=self.tts, daemon=True, args=(f"Failed because {e}",))
            tts_thread1.start()

            return

        cropped_img_to_save = Image.fromarray(face_crop)
        cropped_img_to_save.save(Path(__file__).parent / "faces" / f"{modified_name}.png")

        tts_thread = threading.Thread(target=self.tts, daemon=True, args=("Success.",))
        tts_thread.start()

    def get_findings(self):
        while True:
            attendance_system.upd_event.wait()
            attendance_system.upd_event.clear()

            if not self.running.is_set():
                _, _, self.findings = get_data_func()
                self.determine_findings(self.findings)

    def determine_findings(self, findings):
        if findings is not None:
            self.running.set()

            if len(findings) > 0:
                df = findings[0]

                if not df.empty:
                    top_match = df.iloc[0]
                    img_path = top_match['identity']
                    
                    name = Path(img_path).stem.replace('_', ' ')

                    try:
                        get_student_id_for_logging(name=name)
                    except Exception as e:
                        tts_thread = threading.Thread(target=self.tts, daemon=True, args=(f"Failed because {e}",))

                        tts_thread.start()
                        self.running.clear()
                        reset_findings()

                        return
                    
                    tts_thread = threading.Thread(target=self.tts, daemon=True, args=(f"Hello {name}, logged in for today.",))
                    tts_thread.start()

                    self.running.clear()

                    reset_findings()
                else:
                    tts_thread = threading.Thread(target=self.tts, daemon=True, args=("No such face recognized.",))
                    tts_thread.start()

                    self.running.clear()

                    reset_findings()

    def get_students_data(self):
        try:
            student = get_students()
        except Exception as e:
            self.capture_msg(f"Failed because {e}")
            return

        print(student)

    def get_student_att_data(self):
        try:
            data = get_student(int(self.student_id_add_data.get())) 
            
            if len(data) == 0:
                print("Student id hasn't been registered!")
                return
                
            print(data)
        except Exception as e:
            self.capture_msg(f"Failed because {e}")
            return

    def capture_msg(self, message):
        self.window.after(0, lambda: messagebox.showinfo(title="Info", message=message))

    def tts(self, subject):
        tts_engine = pyttsx3.init()
        
        tts_engine.setProperty('rate', 150)
        
        try:
            tts_engine.say(subject)
            tts_engine.runAndWait()
        except RuntimeError:
            self.capture_msg("There is still an ongoing TTS, please wait..")
            return

    def att_system_thread(self):
        attendance_system_func()

if __name__ == "__main__":
    init()

    window = tk.Tk()
    AttendanceSystem(window)
    window.mainloop()