# 6.1800 - Computer Systems Engineering 🌐

# 📚 Course Resources
# -------------------
# [Website](https://web.mit.edu/6.1800/www/)
# [Recitation Slides](https://drive.google.com/drive/u/0/folders/1-D5N9aUnUPstulpASXqS0p9tXJiFzuyQ)
# [Tidbits](https://lmwilson.scripts.mit.edu/6.1800/tidbits/)
# [Piazza](https://piazza.com/class/m5ybrxanpen5wz)
# [Canvas (Unused)](https://canvas.mit.edu/courses/31100)
# [Lecture Recordings (Panopto)](https://mit.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx#query=%226.4110%22)
# [GitHub Repo](https://github.com/GatlenCulp/mit_computer_systems) (Gatlen Only)

# 🧑‍🏫 Instructor and Contact Information
# ---------------------------------------
# **Lecturer**
# - Katrina LaCurts (lacurts@mit.edu)
#
# **Recitation Instructors**
# - Olivia Brode-Roger (nibr@mit.edu)
#
# **Wrap Instructors**
# - Rebecca Thorndike-Breeze (rtb@mit.edu)
# - Rachel Molko (molko@mit.edu)
#
# **TAs**
# - Emeka Echezona (echezona@mit.edu)
# - Contact: 6.1800-utas@mit.edu
#
# **Tutorial Leader**
# - Jessie Stickgold-Sarah (jmss@mit.edu)

# 📅 Schedule
# -----------
# Lec: Monday & Tuesday 02:00 PM — 03:00 PM
# Rec: Tuesday & Thursday 10:00 AM — 11:00 AM

# 🤝 Collaboration & AI Policy
# ----------------------------
# Can collaborate, but solutions must be separate. Solutions differing by variable names will not receive full credit.

# 📕 Text Book
# ------------
# Principles of Computer System Design: An Introduction
# - Full text: https://ocw.mit.edu/courses/res-6-004-principles-of-computer-system-design-an-introduction-spring-2009/pages/online-textbook/
# - Part 1: [N/A]

# 📝 Course Content
# ----------------
# Topics on the engineering of computer software and hardware systems: techniques for controlling complexity; strong modularity using client-server design, operating systems; performance, networks; naming; security and privacy; fault-tolerant systems, atomicity and coordination of concurrent activities, and recovery; impact of computer systems on society. Case studies of working systems and readings from the current literature provide comparisons and contrasts. Includes a single, semester-long design project. Students engage in extensive written communication exercises. Enrollment may be limited.

# Course Meta
# -----------
# Course Number: 6.1800
# Long Name: Computer Systems Engineering
# Short Name: CompSys
# Logo: 🌐
# Color: Command Line Green

from gf.classes import Course, GradingGroup, Task

computer_systems = Course(
    name="6.1800 - Computer Systems Engineering",
    care_factor=1,
    grading_groups=[
        GradingGroup(
            name="Exams",
            weight=0.30,
            tasks=[
                Task("Exam 1", grade=None),
                Task("Exam 2", grade=None),
            ],
            default_pst=20,  # Assuming 20 hours per exam
            expected_grade=0.70,
            base_grade=0,
        ),
        GradingGroup(
            name="Hands On",
            weight=0.30,
            tasks=[
                Task("Hands On 1", grade=None),
                Task("Hands On 2", grade=None),
                Task("Hands On 3", grade=None),
                Task("Hands On 4", grade=None),
                Task("Hands On 5", grade=None),
                Task("Hands On 6", grade=None),
            ],
            default_pst=10,  # Assuming 10 hours per hands-on
            late_policy="Lowest grade dropped",
            expected_grade=0.80,
            base_grade=0,
        ),
        GradingGroup(
            name="Design Project",
            weight=0.40,
            tasks=[
                Task("DP Prep Assignment", grade=None),
                Task("DP Preliminary Report + Presentation", grade=None),
                Task("DP Report", grade=None),
                Task("DP Peer Review", grade=None),
            ],
            default_pst=40,  # Assuming 40 hours for the entire project
            expected_grade=0.90,
            base_grade=0,
        ),
        GradingGroup(
            name="Participation",
            weight=0.25,
            tasks=[
                Task("Recitation Participation", grade=None),  # 26 sessions, 0.8% each
                Task("Communication Participation", grade=None),
            ],
            default_pst=2,  # 2 hours per week
            expected_grade=0.95,
            base_grade=0,
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
