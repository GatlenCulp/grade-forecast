import math
from typing import Optional, Union

from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .grading_group import GradingGroup
from .task import Task

default_grading_boundaries = {
    "A": (90, 100),
    "B": (80, 89.9999),
    "C": (70, 79.9999),
    "D": (60, 69.9999),
    "F": (0, 59.9999),
}

default_grade_utils = {
    "A": 1,
    "B": 0.8,
    "C": 0.7,
    "D": 0.5,
    "F": 0,
}


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


class Course:
    """A course with grading groups that contribute to a final grade."""

    def __init__(
        self,
        name: str,
        care_factor: float,
        grading_groups: list[GradingGroup],
        grading_boundaries: dict[str, tuple[float, float]] = default_grading_boundaries,
        grade_utils: dict[str, float] = default_grade_utils,
        late_policy: Optional[str] = None,
    ):
        self.name = name
        self.care_factor = care_factor
        self.grading_groups = grading_groups
        self.grading_boundaries = grading_boundaries
        self.grade_utils = grade_utils
        self.late_policy = late_policy

    def get_grade(self) -> float:
        """Calculate the current grade based on completed and base grades."""
        return sum(group.get_contribution() for group in self.grading_groups)

    def get_current_grade(self) -> float:
        """Calculate the current grade based only on completed assignments."""
        # Get all tasks from all grading groups
        all_tasks = []
        for group in self.grading_groups:
            all_tasks.extend(group.tasks)

        # Check if any tasks have been completed
        completed_tasks = [task for task in all_tasks if task.grade is not None]
        if not completed_tasks:
            return 0  # No tasks completed yet

        # Calculate the current grade based on completed assignments
        total_contribution = 0
        for group in self.grading_groups:
            total_contribution += group.get_current_contribution()

        return total_contribution

    def get_true_grade(self) -> float:
        """Calculate the grade assuming no work is done."""
        return sum(group.get_true_contribution() for group in self.grading_groups)

    def get_expected_grade(self) -> float:
        """Calculate the expected grade based on expected grades."""
        return sum(group.get_expected_contribution() for group in self.grading_groups)

    def get_letter_grade(self, grade: Optional[float] = None) -> str:
        """Convert a numerical grade to a letter grade."""
        if grade is None:
            grade = self.get_grade()

        for letter, (lower, upper) in self.grading_boundaries.items():
            if lower <= grade <= upper:
                return letter
        return "?"

    def get_task(self, name: str) -> Task:
        """Find a task by name across all grading groups."""
        for group in self.grading_groups:
            try:
                return group.get_task(name)
            except Exception:
                pass
        raise Exception("Task not found")

    def get_parent(self, task: Union[Task, str]) -> GradingGroup:
        """Find the grading group that contains a task."""
        if isinstance(task, str):
            task_name = task
        else:
            task_name = task.name

        for group in self.grading_groups:
            for t in group.tasks:
                if t.name == task_name:
                    return group
        raise Exception("Parent not found")

    def get_marginal_grade_per_hour(self, task: Union[Task, str]) -> float:
        """Calculate the marginal grade increase per hour for a task."""
        if isinstance(task, str):
            task = self.get_task(task)
        parent = self.get_parent(task)
        return parent.get_marginal_grade_per_hour(task)

    def get_raw_utility(self) -> float:
        """Calculate the raw utility of the current grade.

        Note: THIS UTILITY FUNCTION IS DOG WATER, DOESN'T WORK RIGHT.
        TRY TO FIX. https://www.desmos.com/calculator/vpdemyatol
        """
        letter_grade = self.get_letter_grade()
        grade_util = self.grade_utils[letter_grade]
        care_factor = self.care_factor
        return sigmoid(grade_util * care_factor)

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        """Returns a Rich-formatted string representation of the course."""
        # Create table for grading groups
        group_table = Table(box=box.SIMPLE, show_header=True, padding=(0, 2))
        group_table.add_column("Grading Group", style="cyan")
        group_table.add_column("Weight", style="yellow")
        group_table.add_column("Raw Grade", style="green")
        group_table.add_column("Contribution", style="blue")

        total_grade = 0
        for group in self.grading_groups:
            raw_grade = group.get_raw_contribution() * 100
            contribution = group.get_contribution() * 100
            total_grade += contribution
            group_table.add_row(
                group.name,
                f"{group.weight * 100:.1f}%",
                f"{raw_grade:.2f}%",
                f"{contribution:.2f}%",
            )

        # Add total row
        group_table.add_row(
            "TOTAL",
            f"{sum(group.weight for group in self.grading_groups) * 100:.1f}%",
            "",
            f"{total_grade:.2f}%",
        )

        # Create grade summary
        letter_grade = self.get_letter_grade()
        current_grade = self.get_current_grade() * 100
        true_grade = self.get_true_grade() * 100
        expected_grade = self.get_expected_grade() * 100

        grade_summary = Text.assemble(
            ("CURRENT GRADE: ", "bold white"),
            (f"{current_grade:.2f}%", "green"),
            " | ",
            ("NO WORK GRADE: ", "bold white"),
            (f"{true_grade:.2f}%", "red"),
            " | ",
            ("EXPECTED GRADE: ", "bold white"),
            (f"{expected_grade:.2f}%", "blue"),
            " | ",
            ("LETTER GRADE: ", "bold white"),
            (letter_grade, "yellow"),
        )

        # Combine everything in a panel
        content = Group(group_table, Text("\n"), grade_summary)

        panel = Panel(
            content,
            title=f"[bold cyan]{self.name.upper()}[/bold cyan] [yellow](care factor = {self.care_factor})[/yellow]",
            border_style="blue",
            box=box.ROUNDED,
        )

        # Convert to string representation
        console = Console(record=True)
        console.print(panel)
        return console.export_text()
