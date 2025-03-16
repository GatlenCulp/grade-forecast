"""Grade Forecast CLI package."""

from gf.cli.display import (
    display_course_details,
    display_course_info,
    display_courses_table,
    display_task_analysis,
)
from gf.cli.interface import interface
from gf.cli.main import app, compare, course, list, run, summary, task, tasks, update
from gf.cli.plotting import plot_course_grade_vs_grade
from gf.cli.utils import find_course, find_task

__all__ = [
    "app",
    "compare",
    "course",
    "display_course_details",
    "display_course_info",
    "display_courses_table",
    "display_task_analysis",
    "find_course",
    "find_task",
    "interface",
    "list",
    "plot_course_grade_vs_grade",
    "run",
    "summary",
    "task",
    "tasks",
    "update",
]
