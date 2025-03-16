from typing import TYPE_CHECKING

from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

if TYPE_CHECKING:
    from .grading_group import GradingGroup


def create_grading_group_display(grading_group: "GradingGroup") -> Panel:
    """Create a rich panel display for a grading group.

    Args:
        grading_group: The grading group to display

    Returns:
        Panel: A rich panel containing the formatted grading group information
    """
    # Create table for tasks
    task_table = Table(box=box.SIMPLE, show_header=True, padding=(0, 2))
    task_table.add_column("Task", style="cyan")
    task_table.add_column("Grades", style="green")
    task_table.add_column("Course Contribution", style="yellow")

    for task in grading_group.tasks:
        task_table.add_row(
            task.name,
            (
                f"{float(task.grade or 0) * 100:>5.1f}% "
                f"(base {float(task.base_grade) * 100:>4.1f}%) "
                f"(expected {float(task.expected_grade) * 100:>4.1f}%)"
            ),
            f"{grading_group.get_marginal_grade_per_hour(task) * 100:>5.2f}%/hr",
        )

    # Get completed tasks for current grade calculation
    completed_tasks = [task for task in grading_group.tasks if task.grade is not None]
    current_grade = (
        (sum(task.grade for task in completed_tasks) / len(completed_tasks) * 100)
        if completed_tasks
        else 0
    )

    # Create contribution summary
    contributions = Text.assemble(
        ("NO WORK GRADE", "red"),
        f" = {grading_group.get_true_contribution() * 100:>5.2f}% │ ",
        ("MIN WORK GRADE", "yellow"),
        f" = {grading_group.get_contribution() * 100:>5.2f}% │ ",
        ("CURRENT GRADE", "green"),
        f" = {current_grade:>5.2f}% │ ",
        ("EXPECTED GRADE", "blue"),
        f" = {grading_group.get_expected_contribution() * 100:>5.2f}%",
    )

    # Combine everything in a panel
    content = Group(task_table, Text("\nContributions:", style="bold white"), contributions)

    panel = Panel(
        content,
        title=f"[bold cyan]{grading_group.name.upper()}[/bold cyan] [yellow](weight = {grading_group.weight * 100:.1f}%)[/yellow]",
        border_style="blue",
        box=box.ROUNDED,
    )

    return panel


def grading_group_to_string(grading_group: "GradingGroup") -> str:
    """Convert a grading group panel to a string representation.

    Args:
        grading_group: The grading group to convert

    Returns:
        str: String representation of the grading group panel
    """
    panel = create_grading_group_display(grading_group)
    console = Console(record=True)
    console.print(panel)
    return console.export_text()
