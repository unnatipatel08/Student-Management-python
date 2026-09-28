%%writefile app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import logging
from functools import wraps
from datetime import date

# CONFIGURATION

FILE = "/content/students (1).csv"

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

# LOGGING


logging.basicConfig(
    filename="student_management.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# PYTHON DECORATOR

def activity_logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        logging.info(f"Activity started: {func.__name__}")

        result = func(*args, **kwargs)

        logging.info(f"Activity completed: {func.__name__}")

        return result

    return wrapper


# LOAD DATA

try:

    df = pd.read_csv(FILE)

except FileNotFoundError:

    st.error("Student dataset file not found.")
    st.stop()

# HELPER FUNCTIONS

def save_data(data):

    data.to_csv(FILE, index=False)


def calculate_grade(marks):

    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"


def calculate_result(marks):

    return "Pass" if marks >= 40 else "Fail"


def calculate_performance(marks):

    if marks >= 80:
        return "High"
    elif marks >= 60:
        return "Average"
    else:
        return "Low"


# SIDEBAR MENU

st.sidebar.title("🎓 Student Management")

menu = st.sidebar.radio(
    "Select Operation",
    [
        "📊 Dashboard",
        "➕ Add Student",
        "✏️ Update Student",
        "🔍 Search Student",
        "🗑️ Delete Student"
    ]
)


# DASHBOARD

if menu == "📊 Dashboard":

    st.title("🎓 Student Management Dashboard")

    st.caption(
        "Python for Data Science - Student Performance Management System"
    )

    # FILTERS

    st.subheader("🔎 Filters")

    col1, col2 = st.columns(2)

    with col1:

        branches = ["All"] + sorted(
            df["Branch"].dropna().astype(str).unique().tolist()
        )

        selected_branch = st.selectbox(
            "Branch",
            branches
        )

    with col2:

        semesters = ["All"] + sorted(
            df["Semester"].dropna().astype(str).unique().tolist()
        )

        selected_semester = st.selectbox(
            "Semester",
            semesters
        )

    filtered_df = df.copy()

    if selected_branch != "All":

        filtered_df = filtered_df[
            filtered_df["Branch"].astype(str) == selected_branch
        ]

    if selected_semester != "All":

        filtered_df = filtered_df[
            filtered_df["Semester"].astype(str) == selected_semester
        ]

    # KPI CARDS


    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👨‍🎓 Total Students",
        len(filtered_df)
    )

    col2.metric(
        "📊 Average Marks",
        f"{filtered_df['Marks'].mean():.2f}"
    )

    col3.metric(
        "📅 Average Attendance",
        f"{filtered_df['Attendance'].mean():.2f}%"
    )

    col4.metric(
        "✅ Pass Students",
        int((filtered_df["Result"] == "Pass").sum())
    )


    # LOW ATTENDANCE ALERT

    low_attendance = filtered_df[
        filtered_df["Attendance"] < 75
    ]

    if len(low_attendance) > 0:

        st.warning(
            f"⚠️ {len(low_attendance)} student(s) have attendance below 75%."
        )


    # TOP STUDENTS

    st.subheader("🏆 Top Students")

    top_students = filtered_df.sort_values(
        by="Marks",
        ascending=False
    ).head(5)

    st.dataframe(
        top_students[
            [
                "Student_ID",
                "Name",
                "Branch",
                "Semester",
                "Marks",
                "Grade"
            ]
        ],
        use_container_width=True
    )


    # CHART 1 - BRANCH


    st.subheader("📊 Students by Branch")

    branch_count = (
        filtered_df["Branch"]
        .value_counts()
        .reset_index()
    )

    branch_count.columns = [
        "Branch",
        "Students"
    ]

    fig1 = px.bar(
        branch_count,
        x="Branch",
        y="Students",
        title="Branch-wise Student Count"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )


    # CHART 2 - MARKS

    st.subheader("📈 Marks Distribution")

    fig2 = px.histogram(
        filtered_df,
        x="Marks",
        nbins=10,
        title="Student Marks Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # CHART 3 - GRADE


    grade_count = (
        filtered_df["Grade"]
        .value_counts()
        .reset_index()
    )

    grade_count.columns = [
        "Grade",
        "Students"
    ]

    fig3 = px.pie(
        grade_count,
        names="Grade",
        values="Students",
        title="Grade Distribution"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


    # CHART 4 - ATTENDANCE

    fig4 = px.histogram(
        filtered_df,
        x="Attendance",
        nbins=10,
        title="Attendance Distribution"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )


    # STUDENT TABLE


    st.subheader("📋 Student Records")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    logging.info("Dashboard viewed")


# ADD STUDENT


elif menu == "➕ Add Student":

    st.title("➕ Add New Student")

    with st.form("add_student"):

        student_id = st.text_input("Student ID")

        name = st.text_input("Student Name")

        email = st.text_input("Email")

        phone = st.text_input("Phone")

        branch = st.selectbox(
            "Branch",
            sorted(df["Branch"].astype(str).unique())
        )

        semester = st.selectbox(
            "Semester",
            sorted(df["Semester"].astype(str).unique())
        )

        division = st.selectbox(
            "Division",
            sorted(df["Division"].astype(str).unique())
        )

        attendance = st.number_input(
            "Attendance %",
            min_value=0.0,
            max_value=100.0,
            value=75.0
        )

        marks = st.number_input(
            "Marks",
            min_value=0.0,
            max_value=100.0,
            value=50.0
        )

        assignment_score = st.number_input(
            "Assignment Score",
            min_value=0.0,
            max_value=100.0,
            value=50.0
        )

        study_hours = st.number_input(
            "Study Hours",
            min_value=0.0,
            max_value=24.0,
            value=5.0
        )

        previous_percentage = st.number_input(
            "Previous Percentage",
            min_value=0.0,
            max_value=100.0,
            value=60.0
        )

        add_button = st.form_submit_button(
            "➕ Add Student"
        )

    if add_button:

        if student_id == "" or name == "":
            st.error("Student ID and Name are required.")

        elif student_id in df["Student_ID"].astype(str).values:

            st.error("Student ID already exists.")

        else:

            grade = calculate_grade(marks)

            result = calculate_result(marks)

            performance = calculate_performance(marks)

            new_student = {
                "Student_ID": student_id,
                "Name": name,
                "Email": email,
                "Phone": phone,
                "Branch": branch,
                "Semester": semester,
                "Division": division,
                "Academic_Year": "2026-27",
                "Admission_Date": str(date.today()),
                "Attendance": attendance,
                "Marks": marks,
                "Internal_Marks": 0,
                "External_Marks": 0,
                "Assignment_Score": assignment_score,
                "Study_Hours": study_hours,
                "Previous_Percentage": previous_percentage,
                "Grade": grade,
                "Result": result,
                "Performance_Level": performance,
                "Enrollment_Status": "Active"
            }

            df = pd.concat(
                [
                    df,
                    pd.DataFrame([new_student])
                ],
                ignore_index=True
            )

            save_data(df)

            logging.info(
                f"Student added: {student_id}"
            )

            st.success(
                f"✅ {name} added successfully!"
            )


# UPDATE STUDENT

elif menu == "✏️ Update Student":

    st.title("✏️ Update Student")
    st.caption("Update student personal and academic information")

    st.divider()

    student_id = st.text_input(
        "Current Student ID",
        placeholder="Enter Student ID"
    )

    if student_id:

        student_rows = df[
            df["Student_ID"].astype(str).str.strip() == student_id.strip()
        ]

        if len(student_rows) == 0:

            st.error("❌ Student not found. Please check the Student ID.")

        else:

            index = student_rows.index[0]

            st.success(
                f"Student Found: {df.loc[index, 'Name']}"
            )

            st.subheader("👤 Student Information")

            col1, col2 = st.columns(2)

            with col1:

                new_student_id = st.text_input(
                    "Student ID",
                    value=str(df.loc[index, "Student_ID"])
                )

                new_name = st.text_input(
                    "Student Name",
                    value=str(df.loc[index, "Name"])
                )

                new_email = st.text_input(
                    "Email",
                    value=str(df.loc[index, "Email"])
                )

                new_phone = st.text_input(
                    "Phone",
                    value=str(df.loc[index, "Phone"])
                )

            with col2:

                new_branch = st.text_input(
                    "Branch",
                    value=str(df.loc[index, "Branch"])
                )

                new_semester = st.text_input(
                    "Semester",
                    value=str(df.loc[index, "Semester"])
                )

                new_division = st.text_input(
                    "Division",
                    value=str(df.loc[index, "Division"])
                )

                new_status = st.selectbox(
                    "Enrollment Status",
                    ["Active", "Inactive"],
                    index=0 if str(df.loc[index, "Enrollment_Status"]) == "Active" else 1
                )

            st.divider()

            st.subheader("📊 Academic Information")

            col1, col2 = st.columns(2)

            with col1:

                new_marks = st.number_input(
                    "Marks",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(df.loc[index, "Marks"]),
                    step=1.0
                )

                new_attendance = st.number_input(
                    "Attendance (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(df.loc[index, "Attendance"]),
                    step=1.0
                )

            with col2:

                new_assignment = st.number_input(
                    "Assignment Score",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(df.loc[index, "Assignment_Score"]),
                    step=1.0
                )

                new_study_hours = st.number_input(
                    "Study Hours",
                    min_value=0.0,
                    max_value=24.0,
                    value=float(df.loc[index, "Study_Hours"]),
                    step=0.5
                )

            st.divider()

            if st.button(
                "💾 Save All Changes",
                type="primary",
                use_container_width=True
            ):

                df.loc[index, "Student_ID"] = new_student_id
                df.loc[index, "Name"] = new_name
                df.loc[index, "Email"] = new_email
                df.loc[index, "Phone"] = new_phone
                df.loc[index, "Branch"] = new_branch
                df.loc[index, "Semester"] = new_semester
                df.loc[index, "Division"] = new_division
                df.loc[index, "Enrollment_Status"] = new_status
                df.loc[index, "Marks"] = new_marks
                df.loc[index, "Attendance"] = new_attendance
                df.loc[index, "Assignment_Score"] = new_assignment
                df.loc[index, "Study_Hours"] = new_study_hours

                df.loc[index, "Grade"] = calculate_grade(new_marks)
                df.loc[index, "Result"] = calculate_result(new_marks)
                df.loc[index, "Performance_Level"] = calculate_performance(new_marks)

                save_data(df)

                logging.info(
                    f"Student updated: {new_student_id}"
                )

                st.success(
                    f"✅ {new_name}'s complete details updated successfully!"
                )


# SEARCH STUDENT

elif menu == "🔍 Search Student":

    st.title("🔍 Search Student")

    search = st.text_input(
        "Enter Student ID or Name"
    )

    if search:

        result = df[
            df["Student_ID"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
            |
            df["Name"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

        st.write(
            f"Students Found: {len(result)}"
        )

        st.dataframe(
            result,
            use_container_width=True
        )

        logging.info(
            f"Student search: {search}"
        )


# DELETE STUDENT

elif menu == "🗑️ Delete Student":

    st.title("🗑️ Student Leave / Delete")

    student_id = st.text_input(
        "Enter Student ID"
    )

    if st.button("🗑️ Delete Student"):

        if student_id in df["Student_ID"].astype(str).values:

            df = df[
                df["Student_ID"].astype(str) != student_id
            ]

            save_data(df)

            logging.info(
                f"Student deleted: {student_id}"
            )

            st.success(
                f"✅ Student {student_id} deleted successfully."
            )

        else:

            st.error(
                "❌ Student ID not found."
            )
