# 6.1010 - Fundamentals of Programming Public Course Template

# 📚 Course Resources
# -------------------
# [Website](https://py.mit.edu/fall24)
# [Course Guide](https://underground-guide.mit.edu/term/2024/fall/course/6.1010)
# [Updating Gcal](https://calendar.google.com/calendar/embed?src=vijlme99472vtn91r6r10fta1dtqauqd%40import.calendar.google.com&ctz=America%2FNew_York)
# [GitHub Repo (Gatlen Only)](https://github.com/GatlenCulp/program_fundies)
# [Readings](https://py.mit.edu/fall24/readings)

# 🧑‍🏫 Instructor and Contact Information
# ---------------------------------------
# **Instructor — Depends on Recitation**
#
# - [6.101-help@mit.edu](mailto:6.101-help@mit.edu)
# - [6.101-personal@mit.edu](mailto:6.101-personal@mit.edu)
#
# **Additional Contact:**
# - **Karen Sollins**
#   - Email: sollins@csail.mit.edu

# 💁 Possible Tutors
# ------------------
# [Possible Tutors](https://math.mit.edu/learningcenter/tutors.html#subject)
# - Amir Kolic
# - Matija Likar
# - Misheel Otgonbayar
# - Pedro Suarez
# - Grace Tian
# - Edwin Trejo-Balderas
# - Audrey Xie

# 🤝 Collaboration & AI Policy
# ----------------------------
# - **Standard:** Don’t copy; collaboration is allowed where specified.
# - **AI Usage:** Must list which AI tools are used in assignments and projects.

# 💯 Tests
# --------
# - Single sheet of handwritten notes allowed during exams.

# 🧪 Labs
# -------
# - Time Commitment: 8-10 hours per lab.
# - Submissions: Can submit as many times as desired; both code and conceptual questions must be addressed.
# - Additional Tests: Labs will include tests not provided in the initial test cases.
# - Deadlines:
#   - Due: Wednesday @ 22:00
#   - Checkoff: Sunday @ 22:00
# - Late Policy:
#   - 25% reduction if submitted by cutoff, but full points for labs that pass all tests.
#   - Late penalties are dropped for the 3 labs that benefit the most from this policy.

# 📄 Final Project
# ---------------
# *Note: Final Project details are not specified in the provided information. If applicable, include them here.*

# 📝 Grading Policy
# -----------------
# Letter Grades:
# - A = [90%, 100%]
# - B = [80%, 90%)
# - C = [70%, 80%)
# - D = [60%, 70%)
# - F = [0%, 60%)
#
# Grade Components:
# | Component                      | Weight          |
# | ------------------------------ | --------------- |
# | Labs (13 total, 3.85% each)    | 50%             |
# | Participation (12 readings, ~0.83% each) | 10% - y - z |
# | Midterm (2hr)                  | 15% + y         |
# | Final (3hr)                    | 25% + z         |
#
# {y, z} = weight of missed readings in {first, second} quarter shifted to {midterm, final}

from classes import Course, GradingGroup, Task

# 6.1010 - Fundamentals of Programming Public
prog_fund = Course(
    name="6.1010 - Fundamentals of Programming Public",
    care_factor=1,
    grading_groups=[
        GradingGroup(
            name="Labs",
            weight=0.50,
            tasks=[
                Task("Lab #1 (Audio Processing)", grade=5.0 / 5.0),
                Task("Lab #2 (Image Processing)", grade=5.0 / 5.0),
                Task("Lab #3 (Image Processing 2)", grade=5.0 / 5.0),
                Task("Lab #4 (Bacon Number)", grade=4.77 / 5.0),
                Task("Lab #5 (Snekoban)", grade=5.0 / 5.0),
                Task("Lab #6 (Recipes)", grade=5.0 / 5.0),
                Task("Lab #7 (Mines)", grade=5.0 / 5.0),
                Task("Lab #8 (SAT Solver)", grade=5.0 / 5.0),
                Task("Lab #9", grade=5.0 / 5.0),
                Task("Lab #10", grade=5.0 / 5.0),
                Task("Lab #11", grade=5.0 / 5.0),
                Task("Lab #12", grade=5.0 / 5.0),
                Task("Lab #13", grade=5.0 / 5.0),
            ],
            default_pst=7,
            late_policy="""
                - 25% reduction if submitted by cutoff.
                - Full points for labs that pass all tests.
                - Late penalties are dropped for the 3 labs that benefit the most.
            """,
            expected_grade=0.992,
            base_grade=0,
        ),
        GradingGroup(
            name="Participation",
            weight=0.0802,
            tasks=[
                Task("Reading #1 (Intro)", grade=1.0),
                Task("Reading #2 (Environment Model)", grade=1.0),
                Task("Reading #3 (Functions)", grade=0.0),
                Task("Reading #4 (Flood Fill)", grade=1.0),
                Task("Reading #5 (Graph Search)", grade=0.75),
                Task("Reading #6 (Recursion)", grade=1.0),
                Task("Reading #7 (Recursion and Iteration)", grade=1.0),
                Task("Reading #8 (Backtracking)", grade=1.0),
                Task("Reading #9", grade=1.0),
                Task("Reading #10", grade=1.0),
                Task("Reading #11", grade=1.0),
                Task("Reading #12", grade=1.0),
            ],
            default_pst=1,
            expected_grade=0.85,
            base_grade=0,
        ),
        GradingGroup(
            name="Midterm",
            weight=0.1602,
            tasks=[
                Task("Midterm Exam (2hr)", grade=8.75 / 10),
            ],
            default_pst=20,
            expected_grade=0.875,
            base_grade=0,
        ),
        GradingGroup(
            name="Final",
            weight=0.2596,
            tasks=[
                Task("Final Exam (3hr)", grade=0.0),
            ],
            default_pst=20,
            expected_grade=0.85,
            base_grade=0,
        ),
    ],
    grading_boundaries={
        "A": (90, 100),
        "B": (80, 90),
        "C": (70, 80),
        "D": (60, 70),
        "F": (0, 60),
    },
)

# Example Usage:
# To calculate the final grade, use the `fundamentals_of_programming` instance.
# Ensure to update each Task's `grade` attribute with the actual scores.

# Example:
# # Update Lab grades
# for i, lab in enumerate(fundamentals_of_programming.grading_groups[0].tasks):
#     lab.grade = obtained_score / max_score  # e.g., 3.7 / 4
#
# # Update Participation grades
# for i, reading in enumerate(fundamentals_of_programming.grading_groups[1].tasks):
#     reading.grade = 0.83  # Assuming full participation
#
# # Update Exam grades
# fundamentals_of_programming.grading_groups[2].tasks[0].grade = 80 / 100  # Midterm score
# fundamentals_of_programming.grading_groups[3].tasks[0].grade = 90 / 100  # Final exam score
#
# # Handle missed readings (y and z adjustments)
# # This requires additional logic to shift weights from Participation to Midterm and Final
#
# final_grade = fundamentals_of_programming.calculate_final_grade()
# print(f"Final Grade: {final_grade}%")
