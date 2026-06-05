import sqlite3 as sql
import threading
from pathlib import Path

db_path = Path(__file__).parent / "attendance.db"
db_lock = threading.Lock()

def init():
    with db_lock:
        conn = sql.connect(db_path)
        cur = conn.cursor()

        cur.executescript(
            """CREATE TABLE IF NOT EXISTS students (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          student_id INTEGER,
                          name TEXT NOT NULL,
                          age INTEGER);
                CREATE TABLE IF NOT EXISTS attendance (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          student_id INTEGER,
                          name TEXT NOT NULL,
                          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);"""
            )
        
        conn.commit()
        conn.close()

def add_student(name, age, student_id):
    with db_lock:
        conn = sql.connect(db_path)
        cur = conn.cursor()

        cur.execute(
            "SELECT student_id FROM students WHERE student_id = ?",
            (student_id,)
            )

        test_for_already_registered_id = cur.fetchone()
        if test_for_already_registered_id is not None:
            conn.close()    
            raise ValueError(f"Student ID {student_id} is already registered.")

        cur.execute(
            "INSERT INTO students (student_id, name, age) VALUES (?, ?, ?)",
            (student_id, name, age)
        )

        conn.commit()
        conn.close()

def get_student_id_for_logging(name):
    with db_lock:
        conn = sql.connect(db_path)
        cur = conn.cursor()

        cur.execute(
            "SELECT student_id FROM students WHERE name = ?",
            (name,)
        )

        student_id_fetched = cur.fetchone()
        _log_student(int(student_id_fetched[0]), name, cur)        

        conn.commit()
        conn.close()

def _log_student(student_id, name, cur):
    cur.execute(
        """SELECT student_id FROM attendance
        WHERE student_id = ?
        AND DATE(attendance.timestamp) = DATE('now')""",
        (student_id,)
    )

    check = cur.fetchone()
    if check is not None:
        raise ValueError(f"{name} is already logged in present today.")

    cur.execute(
        "INSERT INTO attendance (student_id, name) VALUES (?, ?)",
        (student_id, name)
    )

def get_students():
    with db_lock:
        conn = sql.connect(db_path)
        cur = conn.cursor()

        cur.execute(
            "SELECT student_id, name, age FROM students"
        )

        students = cur.fetchall()

        conn.close()
        
        return students
    
def get_student(student_id):
    with db_lock:
        conn = sql.connect(db_path)
        cur = conn.cursor()

        cur.execute(
            "SELECT student_id, name, timestamp FROM attendance WHERE student_id = ?",
            (student_id,)
        )

        students = cur.fetchall()

        conn.close()
        
        return students