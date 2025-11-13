# ...existing code...
import os
import json
import uuid
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

DB_FILENAME = os.path.join(os.path.dirname(__file__), "students.json")

@dataclass
class Student:
    id: str
    name: str
    age: int
    major: str
    gpa: float
    email: str 

    @staticmethod
    def create(name: str, age: int, major: str, gpa: float, email: str) -> "Student":
        return Student(id=str(uuid.uuid4()), name=name, age=age, major=major, gpa=gpa, email=email)


class StudentManager:
    def __init__(self, db_path: str = DB_FILENAME):
        self.db_path = db_path
        self.students: Dict[str, Student] = {}
        self.load()

    def load(self) -> None:
        if not os.path.exists(self.db_path):
            self.students = {}
            return
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.students = {s["id"]: Student(**s) for s in data}
        except Exception:
            self.students = {}

    def save(self) -> None:
        data = [asdict(s) for s in self.students.values()]
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def add_student(self, name: str, age: int, major: str, gpa: float, email: str) -> Student:
        s = Student.create(name, age, major, gpa, email)
        self.students[s.id] = s
        self.save()
        return s

    def list_students(self) -> List[Student]:
        return list(self.students.values())

    def get_student(self, student_id: str) -> Optional[Student]:
        return self.students.get(student_id)

    def update_student(self, student_id: str, **fields) -> Optional[Student]:
        s = self.get_student(student_id)
        if not s:
            return None
        for k, v in fields.items():
            if hasattr(s, k) and v is not None:
                setattr(s, k, v)
        self.save()
        return s

    def delete_student(self, student_id: str) -> bool:
        if student_id in self.students:
            del self.students[student_id]
            self.save()
            return True
        return False

    def search_by_name(self, query: str) -> List[Student]:
        q = query.lower()
        return [s for s in self.students.values() if q in s.name.lower()]


def prompt(prompt_text: str, default: Optional[str] = None) -> str:
    if default is None:
        return input(f"{prompt_text}: ").strip()
    else:
        val = input(f"{prompt_text} [{default}]: ").strip()
        return val or default


def input_int(prompt_text: str, default: Optional[int] = None) -> int:
    while True:
        val = prompt(prompt_text, str(default) if default is not None else None)
        try:
            return int(val)
        except Exception:
            print("Please enter a valid integer.")


def input_float(prompt_text: str, default: Optional[float] = None) -> float:
    while True:
        val = prompt(prompt_text, str(default) if default is not None else None)
        try:
            return float(val)
        except Exception:
            print("Please enter a valid number.")


def print_student(s: Student) -> None:
    print(f"ID   : {s.id}")
    print(f"Name : {s.name}")
    print(f"Age  : {s.age}")
    print(f"Major: {s.major}")
    print(f"GPA  : {s.gpa}")
    print(f"Email: {s.email}")
    print("-" * 40)


def main_menu() -> None:
    mgr = StudentManager()
    MENU = """
Student Record System
1) List students
2) Add student
3) View student
4) Update student
5) Delete student
6) Search by name
7) Exit
"""
    while True:
        print(MENU)
        choice = prompt("Choose option")
        if choice == "1":
            students = mgr.list_students()
            if not students:
                print("No students found.")
            else:
                for s in students:
                    print_student(s)
        elif choice == "2":
            name = prompt("Name")
            age = input_int("Age")
            major = prompt("Major")
            gpa = input_float("GPA")
            email = prompt("Email")
            s = mgr.add_student(name, age, major, gpa, email)
            print("Added student:")
            print_student(s)
        elif choice == "3":
            sid = prompt("Student ID")
            s = mgr.get_student(sid)
            if s:
                print_student(s)
            else:
                print("Student not found.")
        elif choice == "4":
            sid = prompt("Student ID to update")
            s = mgr.get_student(sid)
            if not s:
                print("Student not found.")
                continue
            name = prompt("Name", s.name)
            age = input_int("Age", s.age)
            major = prompt("Major", s.major)
            gpa = input_float("GPA", s.gpa)
            email = prompt("Email", s.email)
            updated = mgr.update_student(sid, name=name, age=age, major=major, gpa=gpa, email=email)
            print("Updated:")
            print_student(updated)
        elif choice == "5":
            sid = prompt("Student ID to delete")
            ok = mgr.delete_student(sid)
            print("Deleted." if ok else "Student not found.")
        elif choice == "6":
            q = prompt("Search query (name)")
            results = mgr.search_by_name(q)
            if not results:
                print("No matches.")
            for s in results:
                print_student(s)
        elif choice == "7" or choice.lower() in ("q", "exit"):
            print("Goodbye.")
            break
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main_menu()
# ...existing code...