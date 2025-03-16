from .task import Task


def default_raw_grading_function(tasks: list[Task]) -> float:
    """Calculate the raw grade for a list of tasks by averaging their grades.
    Uses base_grade as fallback when grade is None.

    Args:
        tasks (list): List of Task objects to grade

    Returns:
        float: Average grade between 0 and 1, or 0 if no tasks
    """
    assert isinstance(tasks, list)

    if tasks:
        return sum(
            task.grade if task.grade is not None else task.base_grade for task in tasks
        ) / len(tasks)
    return 0


def default_true_raw_grading_function(tasks: list[Task]) -> float:
    """Calculate the true raw grade for a list of tasks by averaging only actual grades.
    Uses 0 as fallback when grade is None.

    Args:
        tasks (list): List of Task objects to grade

    Returns:
        float: Average grade between 0 and 1, or 0 if no tasks
    """
    assert isinstance(tasks, list)

    if tasks:
        return sum(task.grade if task.grade is not None else 0 for task in tasks) / len(tasks)
    return 0


def default_expected_raw_grading_function(tasks: list[Task]) -> float:
    """Calculate the expected raw grade for a list of tasks.
    Uses actual grades for completed tasks and expected_grade for incomplete tasks.

    Args:
        tasks (list): List of Task objects to grade

    Returns:
        float: Average expected grade between 0 and 1, or 0 if no tasks
    """
    assert isinstance(tasks, list)

    if tasks:
        return sum(
            task.grade if task.grade is not None else task.expected_grade for task in tasks
        ) / len(tasks)
    return 0
