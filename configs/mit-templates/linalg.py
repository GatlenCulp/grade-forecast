# 18.06 - Linear Algebra 📐

# 📚 Course Resources
# -------------------
# [Canvas](https://canvas.mit.edu/courses/30021)
# [Piazza](https://piazza.com/mit/spring2025/1806)
# [Notes from Notetaker](https://www.dropbox.com/scl/fo/k4wfq91x9vcmk3tzk29dk/AFjgpjXGVNJAh7wUcOpjqYY?rlkey=bvg5184o8f445ggh96l3j5xev&e=1&st=dwyfej3u&dl=0)
# [OCW 18.06 from 2010](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)
# [Spring 2023 Github](https://github.com/mitmath/1806)

# 🧑‍🏫 Instructor and Contact Information
# ---------------------------------------
# **Instructor**
# - Prof. Nike Sun (nsun@mit.edu)
#
# **Course Administrator (Head TA)**
# - Jonathan Edelman (edelmanj@mit.edu)
# - For DAS: sefanya@mit.edu
#
# **Recitation Leaders**
# - Srinidhi Narayanan
# - Arpon Raksit Mary Stelow
# - Noran Tan
# - Zixuan Xu

# 📅 Schedule
# -----------
# Lec: Monday & Wednesday 10:00 AM — 11:00 AM
# Rec: Tuesday 11:00 AM — 12:00 PM

# 🤝 Collaboration & AI Policy
# ----------------------------
# No AI may be used.
# You should prioritize using mathematical language over English in justifying your steps.

# 📕 Text Books
# ------------
# - Introduction to Linear Algebra, 6th ed
# - OCW 18.06 from 2010 materials
# - Spring 2023 Github materials

# 💻 Problem Sets
# -------------
# - 6 Free late days (max of 3 on any one)
# - -50% per day after free late days
# - Lowest grade dropped
# - Cover content from Monday and Wednesday lectures
# - Prioritize mathematical language over English in justifications

# 💯 Exams
# --------
# All midterms are within walker. No notes allowed.
# - Midterm 1: February 19th
# - Midterm 2: March 19th
# - Midterm 3: April 14th
# - Final: As late as May 21st

from gf.classes import Course, GradingGroup, Task

linear_algebra = Course(
    name="18.06 - Linear Algebra",
    care_factor=1,
    grading_groups=[
        GradingGroup(
            name="Problem Sets",
            weight=0.30,
            tasks=[
                Task("PSET #1", grade=None),
                Task("PSET #2", grade=None),
                Task("PSET #3", grade=None),
                Task("PSET #4", grade=None),
                Task("PSET #5", grade=None),
                Task("PSET #6", grade=None),
                Task("PSET #7", grade=None),
                Task("PSET #8", grade=None),
                Task("PSET #9", grade=None),
                Task("PSET #10", grade=None),
            ],
            default_pst=8,  # Assuming 8 hours per PSET
            late_policy="6 free late days (max 3 per assignment), -50% per day after",
            expected_grade=0.85,
            base_grade=0,
        ),
        GradingGroup(
            name="Midterm 1",
            weight=0.12,
            tasks=[
                Task("Midterm 1 (February 19th)", grade=None),
            ],
            default_pst=20,  # Assuming 20 hours of study time
            expected_grade=0.80,
            base_grade=0,
        ),
        GradingGroup(
            name="Midterm 2",
            weight=0.12,
            tasks=[
                Task("Midterm 2 (March 19th)", grade=None),
            ],
            default_pst=20,
            expected_grade=0.80,
            base_grade=0,
        ),
        GradingGroup(
            name="Midterm 3",
            weight=0.12,
            tasks=[
                Task("Midterm 3 (April 14th)", grade=None),
            ],
            default_pst=20,
            expected_grade=0.80,
            base_grade=0,
        ),
        GradingGroup(
            name="Final",
            weight=0.30,
            tasks=[
                Task("Final Exam (May 21st)", grade=None),
            ],
            default_pst=40,  # Assuming 40 hours of study time
            expected_grade=0.80,
            base_grade=0,
        ),
        GradingGroup(
            name="Recitation Attendance",
            weight=0.05,
            tasks=[
                Task("Recitation Attendance", grade=None),  # -0.5% for each missed
            ],
            default_pst=1,  # 1 hour per week
            expected_grade=0.95,
            base_grade=1.0,  # Start at 100% and subtract for missed sessions
        ),
    ],
    grading_boundaries={
        "A": (90, 100),
        "B": (80, 90),
        "C": (70, 80),
        "F": (0, 60),
    },
)

# Example Usage:
# To calculate the final grade, use the `linear_algebra` instance.
# Ensure to update each Task's `grade` attribute with the actual scores.

# Example:
# # Update Problem Set grades
# for i, pset in enumerate(linear_algebra.grading_groups[0].tasks):
#     pset.grade = obtained_score / max_score  # e.g., 3.7 / 4
#
# # Update Midterm grades
# for i, midterm in enumerate(linear_algebra.grading_groups[1].tasks):
#     midterm.grade = obtained_score / max_score  # e.g., 80 / 100
#
# # Update Final grade
# linear_algebra.grading_groups[4].tasks[0].grade = obtained_score / max_score  # e.g., 80 / 100
#
# # Handle missed recitations (y and z adjustments)
# # This requires additional logic to shift weights from Recitation Attendance to Midterm and Final
#
# final_grade = linear_algebra.calculate_final_grade()
# print(f"Final Grade: {final_grade}%")
