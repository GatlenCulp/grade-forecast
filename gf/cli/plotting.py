"""Plotting utilities for the grade forecast CLI."""

import copy
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from gf.classes import Course


def plot_course_grade_vs_grade(course: Course, name: str) -> matplotlib.lines.Line2D:
    """Plot how a task's grade affects the course grade.

    Args:
        course: The course to analyze
        name: The name of the task to analyze

    Returns:
        matplotlib.lines.Line2D: The plotted line
    """
    # Create a copy of the course to avoid modifying the original
    course_copy = copy.deepcopy(course)

    # Get the task by name
    task = course_copy.get_task(name)

    # Create arrays for x and y values
    x = np.linspace(0, 1, 100)
    y = []

    # Calculate course grade for each task grade
    for grade in x:
        task.set_grade(grade)
        y.append(course_copy.get_grade())

    # Create the plot
    plt.figure(figsize=(10, 6))
    (line,) = plt.plot(x, y, "b-")
    plt.xlabel("Task Grade")
    plt.ylabel("Course Grade")
    plt.title(f"Effect of {name} on Course Grade")
    plt.grid(True)

    return line
