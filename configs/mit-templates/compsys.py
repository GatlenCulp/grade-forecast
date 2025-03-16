from gf.classes import Course, GradingGroup, Task

# 6.1400 - Computability and Complexity Theory 📼

# 📚 Course Resources
# -------------------
# [Website](https://people.csail.mit.edu/rrw/6.1400-2025/index.html)
# [Piazza](https://piazza.com/mit/spring2025/61400/home)
# [Piazza Resources](https://piazza.com/mit/spring2025/61400/resources)
# [Canvas (Unused)](https://canvas.mit.edu/courses/31100)
# [Lecture Recordings (Panopto)](https://mit.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx#query=%226.4110%22)
# [GitHub Repo](https://github.com/GatlenCulp/mit_complexity_theory) (Gatlen Only)

# 🧑‍🏫 Instructor and Contact Information
# ---------------------------------------
# **Instructor**
# Ryan Williams (rrw@mit.edu)
# OH: Wednesday 11:00 AM — 12:30 PM, 32-G678 (his office)
#
# **TAs**
# - Jakin Ng (jakinng@mit.edu)
#   - Rec: Friday 11:00 AM — 12:00 PM
#   - OH: Tuesday 12:30 PM — 02:00 PM, TBD
# - Jiatu Li (jiatuli@mit.edu)
#   - Rec: Friday 01:00 PM — 02:00 PM
#   - OH: Tuesday 04:00 PM — 05:30 PM, 32-G5-Lounge

# 📅 Schedule
# -----------
# Lec: Tuesdays & Thursdays 02:30 PM — 04:00 PM
# Rec: Fridays 11:00 AM — 12:00 PM

# 🤝 Collaboration & AI Policy
# ----------------------------
# - Can collaborate, but solutions must be separate
# - Solutions differing by variable names will not receive full credit
# - No ChatGPT allowed

# 📕 Text Book
# ------------
# Intro to the Theory of Computation by Sipser (aka "Sipser")

# 💻 PSETs
# --------
# - Weekly PSETs, released Thursday, due Friday
# - Must be completed in LaTeX
# - No late days allowed
# - Lowest PSET is dropped

# 💯 Exams
# --------
# - One single-sided sheet of notes (8.5x11) allowed
# - Otherwise closed-book
# - Midterm: March 18th (In Class)

# 📝 Grading Policy
# -----------------
# Letter Grades:
# - A = [90%, 100%]
# - B = [80%, 90%)
# - C = [70%, 80%)
# - F = [0%, 60%)
#
# Note: The A/B cutoff has historically been in the low 80s/high 70s.
# Participation in lecture and recitation can lead to grade flexibility.
#
# Grade Components:
# | Component                      | Weight |
# | ------------------------------ | ------ |
# | PSets (9 total, lowest dropped)| 40%    |
# | Midterm (March 18th)           | 25%    |
# | Final                          | 35%    |

# 📝 Course Content
# ----------------
# Mathematical introduction to the theory of computing. Rigorously explores what kinds of tasks can be efficiently solved with computers by way of finite automata, circuits, Turing machines, and communication complexity, introducing students to some major open problems in mathematics. Builds skills in classifying computational tasks in terms of their difficulty. Discusses other fundamental issues in computing, including the Halting Problem, the Church-Turing Thesis, the P versus NP problem, and the power of randomness.

# Course Meta
# -----------
# Course Number: 6.1400
# Long Name: Computability and Complexity Theory
# Short Name: Complexity
# Logo: 📼 (Turing Machine Tape)
# Color: Bubble Gum Godel

complexity = Course(
    name="6.1400 - Computability and Complexity Theory",
    care_factor=1,
    grading_groups=[
        GradingGroup(
            name="Problem Sets",
            weight=0.40,
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
            ],
            default_pst=8,  # Assuming 8 hours per PSET
            late_policy="No late days.",
            expected_grade=0.75,
            base_grade=0,
        ),
        GradingGroup(
            name="Midterm",
            weight=0.25,
            tasks=[
                Task("Midterm Exam", grade=None),
            ],
            default_pst=20,  # Assuming 20 hours of study time
            expected_grade=0.60,
            base_grade=0,
        ),
        GradingGroup(
            name="Final",
            weight=0.35,
            tasks=[
                Task("Final Exam", grade=None),
            ],
            default_pst=30,  # Assuming 30 hours of study time
            expected_grade=0.60,
            base_grade=0,
        ),
    ],
    # In the last 2-3 times the class was taught, the cutoff between A and B
    # has been in the low 80s/high 70s.
    grading_boundaries={
        "A": (85, 100),
        "B": (75, 85),
        "C": (65, 75),
        "F": (0, 65),
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
