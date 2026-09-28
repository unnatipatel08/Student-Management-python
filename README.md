# 🎓 Student Management System

A Python-based Student Management System developed using Streamlit, Pandas, and Plotly. The application provides an interactive dashboard to manage student information, academic performance, attendance, grades, and student records.

## 📌 Project Overview

The Student Management System is designed to manage student academic and personal information through a simple and interactive web-based dashboard.

The system allows users to:

- View student performance through an interactive dashboard
- Filter students by Branch and Semester
- Add new students
- Update existing student information
- Search students by ID or Name
- Delete student records
- Calculate Grades automatically
- Calculate Pass/Fail results
- Calculate Performance Level
- Monitor student attendance
- View top-performing students
- Analyze student data using interactive charts

## 🚀 Features

### 📊 Dashboard

The dashboard provides an overview of student performance.

It includes:

- Total Students
- Average Marks
- Average Attendance
- Pass Students
- Low Attendance Alert
- Top Students
- Student Records

### 📈 Data Visualization

The project uses Plotly for interactive data visualization.

The dashboard includes:

- Branch-wise Student Count
- Marks Distribution
- Grade Distribution
- Attendance Distribution

### ➕ Add Student

Users can add a new student by entering:

- Student ID
- Student Name
- Email
- Phone
- Branch
- Semester
- Division
- Attendance
- Marks
- Assignment Score
- Study Hours
- Previous Percentage

The system automatically calculates:

- Grade
- Result
- Performance Level

### ✏️ Update Student

Existing student information can be updated.

Users can update:

- Student ID
- Name
- Email
- Phone
- Branch
- Semester
- Division
- Enrollment Status
- Marks
- Attendance
- Assignment Score
- Study Hours

Grade, Result, and Performance Level are automatically recalculated after updating marks.

### 🔍 Search Student

Students can be searched using:

- Student ID
- Student Name

The matching student records are displayed in the application.

### 🗑️ Delete Student

Student records can be deleted using the Student ID.

The system checks whether the Student ID exists before deleting the record.

## 🧮 Automatic Performance Calculation

The system automatically calculates grades based on marks.

| Marks | Grade |
|------|------|
| 90–100 | A+ |
| 80–89 | A |
| 70–79 | B |
| 60–69 | C |
| 50–59 | D |
| Below 50 | F |

### Result

- Marks >= 40 → Pass
- Marks < 40 → Fail

### Performance Level

- Marks >= 80 → High
- Marks >= 60 → Average
- Marks < 60 → Low

## 🚀 Beyond Syllabus Feature

### Python Decorator

A custom Python Decorator is included as a Beyond Syllabus feature.

The decorator is designed to add activity logging functionality to Python functions without changing their main logic.

## 🔐 Activity Logging

The application implements an activity logging mechanism using Python's built-in `logging` module. It records important user activities performed within the Student Management System.

### Logged Activities

The system can record activities such as:

- Student Added
- Student Updated
- Student Searched
- Student Deleted
- Dashboard Viewed

The activity records are stored in the following log file:


📌 Conclusion

The Student Management System provides an interactive platform for managing student records and analyzing academic performance.

The application combines Python, Pandas, Streamlit, and Plotly to provide data management and visualization capabilities.

As a Beyond Syllabus enhancement, the project incorporates Python Decorators and Activity Logging, demonstrating how additional functionality can be integrated into a Python application through function wrapping and logging mechanisms.

Overall, the project demonstrates practical applications of Python for Data Science along with interactive dashboard development and student performance management.



💻 Important Code Implementation
1. Python Decorator — Beyond Syllabus

   
```text

def activity_logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        logging.info(f"Activity started: {func.__name__}")

        result = func(*args, **kwargs)

        logging.info(f"Activity completed: {func.__name__}")

        return result

    return wrapper

    return wrapper
