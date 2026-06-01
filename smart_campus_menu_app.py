
import streamlit as st
import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

FILE_NAME = "student_records.csv"

if "students" not in st.session_state:
    st.session_state.students = []

if "courses" not in st.session_state:
    st.session_state.courses = []

if "page" not in st.session_state:
    st.session_state.page = "Home"


def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            reader = csv.DictReader(file)
            st.session_state.students = []
            for row in reader:
                st.session_state.students.append({
                    "id": int(row["ID"]),
                    "name": row["Name"],
                    "age": int(row["Age"]),
                    "marks": int(row["Marks"]),
                    "grade": row["Grade"]
                })


def save_data():
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Age", "Marks", "Grade"])
        for student in st.session_state.students:
            writer.writerow([
                student["id"],
                student["name"],
                student["age"],
                student["marks"],
                student["grade"]
            ])


def calculate_grade(score):
    if 90 <= score <= 100:
        return "A", "Excellent"
    elif score >= 75:
        return "B", "Very Good"
    elif score >= 60:
        return "C", "Good"
    elif score >= 40:
        return "D", "Average"
    else:
        return "F", "Needs Improvement"


class EmptyFolderError(Exception):
    pass


st.set_page_config(page_title="Smart Campus Information System", layout="wide")

# HOME PAGE
if st.session_state.page == "Home":
    st.title("SMART CAMPUS INFORMATION SYSTEM")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Register Student", use_container_width=True):
            st.session_state.page = "Register"
            st.rerun()

        if st.button("Course Enrollment", use_container_width=True):
            st.session_state.page = "Course"
            st.rerun()

        if st.button("Fee Calculation", use_container_width=True):
            st.session_state.page = "Fee"
            st.rerun()

        if st.button("Directory Scanning", use_container_width=True):
            st.session_state.page = "Directory"
            st.rerun()

        if st.button("Save Records", use_container_width=True):
            st.session_state.page = "Save"
            st.rerun()

    with col2:
        if st.button("Display Student Records", use_container_width=True):
            st.session_state.page = "Records"
            st.rerun()

        if st.button("Search Student", use_container_width=True):
            st.session_state.page = "Search"
            st.rerun()

        if st.button("Performance Analysis", use_container_width=True):
            st.session_state.page = "Analysis"
            st.rerun()

        if st.button("Load Records", use_container_width=True):
            st.session_state.page = "Load"
            st.rerun()

        if st.button("Sort Student IDs", use_container_width=True):
            st.session_state.page = "Sort"
            st.rerun()

# REGISTER
elif st.session_state.page == "Register":
    st.header("Student Registration")

    student_id = st.number_input("Student ID", min_value=1)
    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=1)
    marks = st.number_input("Marks", min_value=0, max_value=100)

    if st.button("Submit"):
        grade, remark = calculate_grade(int(marks))

        st.session_state.students.append({
            "id": int(student_id),
            "name": name,
            "age": int(age),
            "marks": int(marks),
            "grade": grade
        })

        st.success("Student Registered Successfully")
        st.write("Grade:", grade)
        st.write("Remark:", remark)

    if st.button("Back To Menu"):
        st.session_state.page = "Home"
        st.rerun()

# DISPLAY
elif st.session_state.page == "Records":
    st.header("Student Records")

    if len(st.session_state.students) == 0:
        st.warning("No student records found.")
    else:
        st.dataframe(pd.DataFrame(st.session_state.students))

    if st.button("Back To Menu"):
        st.session_state.page = "Home"
        st.rerun()

# COURSE
elif st.session_state.page == "Course":
    st.header("Course Enrollment")

    course = st.text_input("Course Name")
    credits = st.number_input("Credits", min_value=1)

    if st.button("Enroll"):
        if len(st.session_state.courses) >= 5:
            st.error("Maximum course limit reached!")
        else:
            st.session_state.courses.append((course, int(credits)))
            st.success("Course Added Successfully")

    st.subheader("Enrolled Courses")

    for c, cr in st.session_state.courses:
        st.write(f"{c} - {cr} credits")

    if st.button("Back To Menu"):
        st.session_state.page = "Home"
        st.rerun()

# SORT
elif st.session_state.page == "Sort":
    st.header("Sorting Student IDs")

    if len(st.session_state.students) == 0:
        st.warning("No students available.")
    else:
        ids = [s["id"] for s in st.session_state.students]

        n = len(ids)
        for i in range(n):
            for j in range(0, n - i - 1):
                if ids[j] > ids[j + 1]:
                    ids[j], ids[j + 1] = ids[j + 1], ids[j]

        st.code(str(ids))

    if st.button("Back To Menu"):
        st.session_state.page = "Home"
        st.rerun()

# SEARCH
elif st.session_state.page == "Search":
    st.header("Search Student")

    target = st.number_input("Student ID To Search", min_value=1)

    if st.button("Search"):
        found = False

        for student in st.session_state.students:
            if student["id"] == target:
                st.write(student)
                found = True
                break

        if not found:
            st.error("Student ID not found")

    if st.button("Back To Menu"):
        st.session_state.page = "Home"
        st.rerun()

# FEES
elif st.session_state.page == "Fee":
    st.header("Fee Calculation")

    tuition = st.number_input("Tuition Fee", min_value=0.0)
    hostel = st.number_input("Hostel Fee", min_value=0.0)
    transport = st.number_input("Transport Fee", min_value=0.0)

    if st.button("Calculate"):
        total = tuition + hostel + transport
        st.success(f"Total Fee = {total}")

    if st.button("Back To Menu"):
        st.session_state.page = "Home"
        st.rerun()

# SAVE
elif st.session_state.page == "Save":
    st.header("Save Records")

    if st.button("Save Records"):
        save_data()
        st.success("Student records saved successfully")

    if st.button("Back To Menu"):
        st.session_state.page = "Home"
        st.rerun()

# LOAD
elif st.session_state.page == "Load":
    st.header("Load Records")

    if st.button("Load Records"):
        load_data()
        st.success("Student records loaded successfully")

    if st.button("Back To Menu"):
        st.session_state.page = "Home"
        st.rerun()

# DIRECTORY
elif st.session_state.page == "Directory":
    st.header("Directory Scanning")

    path = st.text_input("Enter Directory Path")

    if st.button("Scan"):
        try:
            if not os.path.exists(path):
                raise FileNotFoundError("Invalid directory path.")

            output = []

            for root, dirs, files in os.walk(path):
                level = root.replace(path, "").count(os.sep)
                indent = " " * 4 * level
                output.append(f"{indent}{os.path.basename(root)}/")

                for f in files:
                    output.append((" " * 4 * (level + 1)) + f)

                if not files and not dirs:
                    raise EmptyFolderError(f"Empty Folder Found: {root}")

            st.code("\\n".join(output))

        except Exception as e:
            st.error(str(e))

    if st.button("Back To Menu"):
        st.session_state.page = "Home"
        st.rerun()

# ANALYSIS
elif st.session_state.page == "Analysis":
    st.header("Performance Analysis")

    if len(st.session_state.students) == 0:
        st.warning("No student data available.")
    else:
        data = {
            "Name": [s["name"] for s in st.session_state.students],
            "Marks": [s["marks"] for s in st.session_state.students]
        }

        df = pd.DataFrame(data)
        st.dataframe(df)

        scores = np.array(data["Marks"])

        st.write("Mean Marks:", np.mean(scores))
        st.write("Median Marks:", np.median(scores))
        st.write("Standard Deviation:", np.std(scores))

        topper_index = np.argmax(scores)
        st.write("Top Performer:", data["Name"][topper_index])

        fig, ax = plt.subplots()
        ax.bar(data["Name"], data["Marks"])
        ax.set_title("Student Performance")
        ax.set_xlabel("Students")
        ax.set_ylabel("Marks")

        st.pyplot(fig)

    if st.button("Back To Menu"):
        st.session_state.page = "Home"
        st.rerun()
