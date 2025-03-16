"""Grade Forecast CLI package."""

from gf.cli.display import (
    display_courses_table,
    display_course_details,
    display_course_info,
    display_task_analysis,
)
from gf.cli.interface import interface
from gf.cli.main import app, list, course, tasks, task, update, compare, summary, run
from gf.cli.plotting import plot_course_grade_vs_grade
from gf.cli.utils import find_course, find_task

__all__ = [
    "app",
    "interface",
    "display_courses_table",
    "display_course_details",
    "display_course_info",
    "display_task_analysis",
    "plot_course_grade_vs_grade",
    "find_course",
    "find_task",
    "list",
    "course",
    "tasks",
    "task",
    "update",
    "compare",
    "summary",
    "run",
]
