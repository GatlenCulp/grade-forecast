from rich import box
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typing import List, Optional, Union, Callable

from .task import Task, is_proper_fraction
from .grading_functions import (
    default_raw_grading_function,
    default_true_raw_grading_function,
    default_expected_raw_grading_function,
)


class GradingGroup:
    """A group of tasks with a weight that contributes to a course grade."""

    def __init__(
        self,
        name: str,
        weight: float,
        tasks: Union[List[Task], Task, int],
        default_pst: float = 5,
        base_grade: float = 0.5,
        expected_grade: Optional[float] = None,
        late_policy: Optional[str] = None,
        grading_function: Callable = default_raw_grading_function,
        true_grading_function: Callable = default_true_raw_grading_function,
        expected_grading_function: Callable = default_expected_raw_grading_function,
    ):
        assert isinstance(name, str)
        assert is_proper_fraction(weight)
        assert isinstance(default_pst, (float, int))
        assert is_proper_fraction(base_grade)
        # assert is_proper_fraction(expected_grade)

        self.name = name
        self.weight = weight
        self.default_pst = default_pst
        self.base_grade = base_grade
        self.grading_function = grading_function
        self.late_policy = late_policy

        if grading_function != default_raw_grading_function:
            true_grading_function = grading_function
            expected_grading_function = grading_function
        self.true_grading_function = true_grading_function
        self.expected_grading_function = expected_grading_function

        if expected_grade is None:
            expected_grade = base_grade
        self.expected_grade = expected_grade

        if isinstance(tasks, int):
            tasks = self.create_enumerated_tasks(tasks)
        elif isinstance(tasks, Task):
            tasks = [tasks]
        assert isinstance(tasks, list)
        assert isinstance(tasks[0], Task) if len(tasks) > 0 else True
        self.tasks = tasks

        for task in self.tasks:
            if task.pst is None:
                task.pst = default_pst
            if task.base_grade is None:
                task.base_grade = base_grade
            if task.expected_grade is None:
                task.expected_grade = expected_grade

    def __str__(self) -> str:
        """Returns a Rich-formatted string representation of the grading group."""
        from .visualization import grading_group_to_string

        return grading_group_to_string(self)

    def __repr__(self) -> str:
        """Returns a simple string representation of the grading group."""
        return self.name

    def create_enumerated_tasks(self, n: int) -> List[Task]:
        """Create n numbered tasks with default settings.

        Args:
            n (int): Number of tasks to create

        Returns:
            list: List of Task objects
        """
        return [
            Task(
                name=f"{self.name} #{i}",
                base_grade=self.base_grade,
                pst=self.default_pst,
            )
            for i in range(1, n + 1)
        ]

    def get_raw_contribution(self) -> float:
        """Calculate the raw grade contribution before weighting."""
        return self.grading_function(self.tasks)

    def get_contribution(self) -> float:
        """Calculate the weighted grade contribution."""
        return self.get_raw_contribution() * self.weight

    def get_task_contribution(self, task: Union[Task, str]) -> float:
        """Calculate a single task's contribution to the final grade.

        Args:
            task (Task|str): Task object or task name

        Returns:
            float: Task's contribution to final grade
        """
        if isinstance(task, str):
            task = self.get_task(task)
        assert isinstance(task, Task)

        grade = task.grade if task.grade is not None else task.base_grade
        total_tasks = len(self.tasks)
        return self.weight * (grade / total_tasks)

    def get_max_task_contribution(self, task: Union[Task, str]) -> float:
        """Calculate a task's maximum possible contribution.

        Args:
            task (Task|str): Task object or task name

        Returns:
            float: Maximum possible contribution to final grade
        """
        if isinstance(task, str):
            task = self.get_task(task)
        assert isinstance(task, Task)

        grade = 1
        total_tasks = len(self.tasks)
        return self.weight * (grade / total_tasks)

    def get_task(self, name: str) -> Task:
        """Find a task by name.

        Args:
            name (str): Name of task to find

        Returns:
            Task: Found task

        Raises:
            Exception: If task not found
        """
        for task in self.tasks:
            if task.name == name:
                return task
        raise Exception("Task not found")

    def get_marginal_grade_per_hour(self, task: Union[Task, str]) -> float:
        """Calculate marginal grade increase per hour for a task.

        Args:
            task (Task|str): Task object or task name

        Returns:
            float: Grade increase per hour
        """
        if isinstance(task, str):
            task = self.get_task(task)
        assert isinstance(task, Task)

        weight = self.weight
        total_tasks = len(self.tasks)
        return weight * (task.get_marginal_grade_per_hour() / total_tasks)

    def get_current_raw_contribution(self) -> float:
        """Calculate raw contribution from only graded tasks.
        Returns the average grade of completed assignments.
        """
        completed_tasks = [task for task in self.tasks if task.grade is not None]
        if not completed_tasks:
            return 0

        # Calculate average grade of completed tasks
        total_grade = sum(task.grade for task in completed_tasks)
        return total_grade / len(completed_tasks)

    def get_current_contribution(self) -> float:
        """Calculate weighted contribution from only graded tasks.
        For the current grade calculation, we want this to represent the
        actual grade earned on completed work.
        """
        completed_tasks = [task for task in self.tasks if task.grade is not None]
        if not completed_tasks:
            return 0

        # Get average grade as a percentage
        raw_grade = self.get_current_raw_contribution()

        # Calculate what portion of the total weight this group has completed
        weight_per_task = self.weight / len(self.tasks)
        completed_weight = weight_per_task * len(completed_tasks)

        # Return
        return raw_grade * completed_weight

    def get_true_raw_contribution(self) -> float:
        """Calculate raw contribution assuming no work done."""
        return self.true_grading_function(self.tasks)

    def get_true_contribution(self) -> float:
        """Calculate weighted contribution assuming no work done."""
        return self.get_true_raw_contribution() * self.weight

    def get_expected_raw_contribution(self) -> float:
        """Returns the expected raw grade (before weight) for this grading group."""
        return self.expected_grading_function(self.tasks)

    def get_expected_contribution(self) -> float:
        """Returns the expected contribution of this grading group to the final grade."""
        # Separate completed and incomplete tasks
        completed_tasks = [task for task in self.tasks if task.grade is not None]
        incomplete_tasks = [task for task in self.tasks if task.grade is None]

        # If no tasks, return 0
        if not self.tasks:
            return 0

        # Calculate the total expected grade
        total_grade = 0

        # Add actual grades for completed tasks
        if completed_tasks:
            total_grade += sum(task.grade for task in completed_tasks)

        # Add expected grades for incomplete tasks
        if incomplete_tasks:
            total_grade += sum(task.expected_grade for task in incomplete_tasks)

        # Calculate average and apply weight
        average_grade = total_grade / len(self.tasks)
        return average_grade * self.weight
