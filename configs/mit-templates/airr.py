# 6.4110 - Representation, Inference, and Reasoning in AI 🤷🏻‍♀️

# 📚 Course Resources
# -------------------
# [Website](https://airr.mit.edu/spring25/calendar)
# [Piazza](https://piazza.com/class/m6cbdy9ely648f/post/6)
# [Canvas (Unused)](https://canvas.mit.edu/courses/31100)
# [Lecture Recordings (Panopto)](https://mit.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx#query=%226.4110%22)
# [Notation](https://airr.mit.edu/_static/fall23/Glossary.pdf)
# [GitHub Repo](https://github.com/GatlenCulp/uncertainty) (Gatlen Only)

# 🧑‍🏫 Instructor and Contact Information
# ---------------------------------------
# **Instructor**
# - Leslie Kaelbling (lpk@csail.mit.edu)
#
# **TAs**
# - Jagdeep Bhatia (jagdeep@mit.edu)
# - Nishanth Kumar (njk@mit.edu)
# - Ethan Yang (ethany@mit.edu)
# - Ryan Yang (ryanyang@mit.edu)
# - Sunshine Jiang (sunsh16e@mit.edu)
# - Ellery Stahler (ellerys@mit.edu)
# - Ellen Zhang (ellen660@mit.edu)

# 📅 Schedule
# -----------
# Lec: Monday & Wednesday 09:30 AM — 11:00 AM
# Rec: TBD

# 🤝 Collaboration & AI Policy
# ----------------------------
# Can collaborate, but solutions must be separate. Solutions differing by variable names will not receive full credit.

# 📕 Text Books
# ------------
# - Artificial Intelligence: A Modern Approach "AIMA" (4th Edition) by Russel & Norvig
# - Bayesian Reasoning and Machine Learning by David Barber
# - Algorithms for Decision Making by Kochenderfer, Wheeler, Wray (deprecated)

# 💻 Problem Sets
# -------------
# - -10% per day late
# - 10 late-day waivers applied retroactively at end of semester
#
# PSETs:
# - HW00: Background
# - HW01: Search, intro CSP
# - HW02: CSP, PDDL
# - HW03: Continuous, conditional, conformant planning
# - HW04: Prop logic
# - HW05: Intro graphical models
# - HW06: Discrete graphical models
# - HW07: Continuous, temporal models
# - HW08: MDPs
# - HW09: POMDPs
# - HW10: Bandits and FOL

# 📝 Course Content
# ----------------
# An introduction to representations and algorithms for artificial intelligence. Topics covered include: constraint satisfaction in discrete and continuous problems, logical representation and inference, Monte Carlo tree search, probabilistic graphical models and inference, planning in discrete and continuous deterministic and probabilistic models including MDPs and POMDPs.

# Course Meta
# -----------
# Course Number: 6.4110
# Long Name: Representation, Inference, and Reasoning in AI
# Short Name: Uncertainty
# Logo: 🤷🏻‍♀️ (Shrug)
# Color: Royal Confusion Purple

from gf.classes import Course, GradingGroup, Task

uncertainty = Course(
    name="6.4110 - Representation, Inference, and Reasoning in AI",
    care_factor=1,
    grading_groups=[
        GradingGroup(
            name="Problem Sets",
            weight=0.50,
            tasks=[
                Task("HW00 - Background", grade=None),
                Task("HW01 - Search, intro CSP", grade=None),
                Task("HW02 - CSP, PDDL", grade=None),
                Task("HW03 - Continuous, conditional, conformant planning", grade=None),
                Task("HW04 - Prop logic", grade=None),
                Task("HW05 - Intro graphical models", grade=None),
                Task("HW06 - Discrete graphical models", grade=None),
                Task("HW07 - Continuous, temporal models", grade=None),
                Task("HW08 - MDPs", grade=None),
                Task("HW09 - POMDPs", grade=None),
                Task("HW10 - Bandits and FOL", grade=None),
            ],
            default_pst=15,  # Assuming 15 hours per PSET
            late_policy="-10% per day, 10 late days available",
            expected_grade=0.85,
            base_grade=0,
        ),
        GradingGroup(
            name="Midterm",
            weight=0.25,
            tasks=[
                Task("Midterm Exam", grade=None),
            ],
            default_pst=25,  # Assuming 25 hours of study time
            expected_grade=0.85,
            base_grade=0,
        ),
        GradingGroup(
            name="Final",
            weight=0.25,
            tasks=[
                Task("Final Exam", grade=None),
            ],
            default_pst=35,  # Assuming 35 hours of study time
            expected_grade=0.85,
            base_grade=0,
        ),
        # GradingGroup(
        #     name="Lecture Attendance",
        #     weight=0.05,  # Max bonus
        #     tasks=[
        #         Task("Lecture Attendance", grade=None),  # 0.25% per lecture up to 5%
        #     ],
        #     default_pst=0,  # No additional time required
        #     expected_grade=1.0,
        #     base_grade=0,
        # ),
    ],
    grading_boundaries={
        "A": (90, 100),
        "B": (80, 90),
        "C": (70, 80),
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
