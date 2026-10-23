
# Week 6 Final Project
# Student Management System

import json
from abc import ABC, abstractmethod
from datetime import datetime
import os


# Abstraction: define the required storage operations
class Storage(ABC):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self, records):
        pass


# Inheritance: JSONStorage implements Storage
class JSONStorage(Storage):
    def __init__(self, filename="students.json"):
        self.filename = filename

    def load(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Warning: Data file is empty or damaged.")
            return []

    def save(self, records):
        with open(self.filename, "w") as file:
            json.dump(records, file, indent=4)


# Parent class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_details(self):
        print("Name:", self.name)
        print("Age:", self.age)


# Child class: inherits from Person
class Student(Person):
    def __init__(self, student_id, name, age, course):
        super().__init__(name, age)
        self.student_id = student_id
        self.course = course

    # Polymorphism: override the parent method
    def display_details(self):
        print("\nStudent ID:", self.student_id)
        super().display_details()
        print("Course:", self.course)

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "course": self.course
        }


# Main application class
class StudentManagementSystem:
    def __init__(self):
        self.storage = JSONStorage()
        self.students = self.storage.load()

    def save_records(self):
        try:
            self.storage.save(self.students)
        except OSError as error:
            print("Unable to save records:", error)

    def add_student(self):
        try:
            student_id = input("Enter student ID: ").strip()

            if not student_id:
                print("Student ID cannot be empty.")
                return

            if any(s["student_id"] == student_id
                   for s in self.students):
                print("Student ID already exists.")
                return

            name = input("Enter name: ").strip()
            age = int(input("Enter age: "))
            course = input("Enter course: ").strip()

            if not name or not course:
                print("Name and course cannot be empty.")
                return

            if age <= 0:
                print("Age must be greater than zero.")
                return

            student = Student(student_id, name, age, course)
            self.students.append(student.to_dict())
            self.save_records()
            print("Student added successfully!")

        except ValueError:
            print("Invalid age. Please enter a number.")

    def view_students(self):
        if not self.students:
            print("No student records found.")
            return

        for record in self.students:
            student = Student(
                record["student_id"],
                record["name"],
                record["age"],
                record["course"]
            )
            student.display_details()

    def search_student(self):
        student_id = input("Enter student ID to search: ").strip()

        for record in self.students:
            if record["student_id"] == student_id:
                student = Student(
                    record["student_id"],
                    record["name"],
                    record["age"],
                    record["course"]
                )
                student.display_details()
                return

        print("Student not found.")

    def update_student(self):
        student_id = input("Enter student ID to update: ").strip()

        for record in self.students:
            if record["student_id"] == student_id:
                try:
                    name = input("Enter new name: ").strip()
                    age = int(input("Enter new age: "))
                    course = input("Enter new course: ").strip()

                    if not name or not course or age <= 0:
                        print("Enter valid student details.")
                        return

                    record["name"] = name
                    record["age"] = age
                    record["course"] = course
                    self.save_records()
                    print("Student updated successfully!")
                    return

                except ValueError:
                    print("Age must be a valid number.")
                    return

        print("Student not found.")

    def delete_student(self):
        student_id = input("Enter student ID to delete: ").strip()

        for record in self.students:
            if record["student_id"] == student_id:
                self.students.remove(record)
                self.save_records()
                print("Student deleted successfully!")
                return

        print("Student not found.")

    def run(self):
        print("Started at:", datetime.now().strftime("%d-%m-%Y %H:%M"))

        while True:
            print("\n===== STUDENT MANAGEMENT SYSTEM =====")
            print("1. Add Student")
            print("2. View Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.update_student()
            elif choice == "5":
                self.delete_student()
            elif choice == "6":
                print("Thank you for using the system!")
                break
            else:
                print("Invalid choice. Select 1 to 6.")


if __name__ == "__main__":
    app = StudentManagementSystem()
    app.run()
