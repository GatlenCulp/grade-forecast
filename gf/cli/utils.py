"""Utility functions for the grade forecast CLI."""

from typing import Optional

from gf.classes import Course, Task


def find_course(course_input: str, courses: list[Course]) -> Optional[Course]:
    """Find a course by name or index.

    Args:
        course_input: The course name or index to find
        courses: List of available courses

    Returns:
        Course or None: The found course or None if not found
    """
    if course_input.isdigit():
        idx = int(course_input) - 1
        if 0 <= idx < len(courses):
            return courses[idx]
    else:
        for course in courses:
            if course_input.lower() == course.name.lower():
                return course
    return None


def find_task(task_input: str, course: Course, all_tasks: list[Task]) -> Optional[Task]:
    """Find a task by name or index.

    Args:
        task_input: The task name or index to find
        course: The course containing the task
        all_tasks: List of all tasks in the course

    Returns:
        Task or None: The found task or None if not found
    """
    task = None
    if task_input.isdigit():
        idx = int(task_input) - 1
        if 0 <= idx < len(all_tasks):
            task = all_tasks[idx]
    else:
        try:
            task = course.get_task(task_input)
        except Exception:
            pass
    return task
