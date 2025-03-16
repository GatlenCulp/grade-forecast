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
    task_table.add_column("Task", style="cyan", width=30)
    task_table.add_column("Grades", style="green", width=40)
    task_table.add_column("Course Contribution", style="yellow", width=30)

    for task in grading_group.tasks:
        if task.grade is not None:
            grade_text = f"{float(task.grade) * 100:>5.1f}%"
        else:
            grade_text = "Not graded"

        task_table.add_row(
            task.name,
            (
                f"{grade_text} "
                f"(base {float(task.base_grade) * 100:>5.1f}%) "
                f"(expected {float(task.expected_grade) * 100:>5.1f}%)"
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

    # Create contribution summary with consistent formatting
    max_width = 50  # Width of the progress bar
    max_contribution = grading_group.weight * 100

    # Calculate positions for each marker on the progress bar
    no_work_pos = int((grading_group.get_true_contribution() * 100 / max_contribution) * max_width)
    min_work_pos = int((grading_group.get_contribution() * 100 / max_contribution) * max_width)
    current_pos = int((current_grade / max_contribution) * max_width)
    expected_pos = int(
        (grading_group.get_expected_contribution() * 100 / max_contribution) * max_width
    )

    # Create the progress bar
    progress_bar = [[] for _ in range(max_width)]  # Each position can have multiple markers

    # Add markers at their positions
    if no_work_pos < max_width:
        progress_bar[no_work_pos].append("R")
    if min_work_pos < max_width:
        progress_bar[min_work_pos].append("Y")
    if current_pos < max_width:
        progress_bar[current_pos].append("G")
    if expected_pos < max_width:
        progress_bar[expected_pos].append("B")

    # Add the end marker
    progress_bar[-1].append("M")

    # Create the progress bar text with proper styling
    progress_text = Text()
    for pos in progress_bar:
        if not pos:  # Empty position
            progress_text.append("─")
        elif len(pos) == 1:  # Single marker
            marker = pos[0]
            if marker == "R":
                progress_text.append("│", style="red")
            elif marker == "Y":
                progress_text.append("│", style="yellow")
            elif marker == "G":
                progress_text.append("│", style="green")
            elif marker == "B":
                progress_text.append("│", style="blue")
            elif marker == "M":
                progress_text.append("►", style="magenta")
        else:  # Multiple markers stacked
            # Sort markers in a consistent order: R, Y, G, B, M
            sorted_markers = sorted(pos, key=lambda m: "RYGBM".index(m))
            marker_chars = []
            for marker in sorted_markers:
                if marker == "R":
                    marker_chars.append(("┃", "red"))
                elif marker == "Y":
                    marker_chars.append(("┃", "yellow"))
                elif marker == "G":
                    marker_chars.append(("┃", "green"))
                elif marker == "B":
                    marker_chars.append(("┃", "blue"))
                elif marker == "M":
                    marker_chars.append(("►", "magenta"))

            # Use a thicker character for stacked markers
            if len(marker_chars) == 2:
                progress_text.append("┃", style=marker_chars[0][1])
            elif len(marker_chars) >= 3:
                progress_text.append("╋", style=marker_chars[0][1])

            # Add a note about stacked markers for the legend
            if "stacked_markers" not in locals():
                stacked_markers = True

    # Create the legend
    legend = Text()
    legend.append("\n")
    legend.append("│", style="red")
    legend.append(" NO WORK ", style="red")
    legend.append("    ")
    legend.append("│", style="yellow")
    legend.append(" MIN WORK ", style="yellow")
    legend.append("    ")
    legend.append("│", style="green")
    legend.append(" CURRENT ", style="green")
    legend.append("    ")
    legend.append("│", style="blue")
    legend.append(" EXPECTED ", style="blue")
    legend.append("    ")
    legend.append("►", style="magenta")
    legend.append(" MAX", style="magenta")

    # Add stacked markers explanation if needed
    if "stacked_markers" in locals() and stacked_markers:
        legend.append("\n\n")
        legend.append("┃", style="cyan")
        legend.append(" OVERLAPPING MARKERS ", style="cyan")
        legend.append("    ")
        legend.append("╋", style="cyan")
        legend.append(" MULTIPLE OVERLAPPING MARKERS", style="cyan")

    # Create the values text
    values = Text()
    values.append("\n")
    values.append(f"{grading_group.get_true_contribution() * 100:>5.2f}%", style="red")
    values.append("        ")
    values.append(f"{grading_group.get_contribution() * 100:>5.2f}%", style="yellow")
    values.append("        ")
    values.append(f"{current_grade:>5.2f}%", style="green")
    values.append("        ")
    values.append(f"{grading_group.get_expected_contribution() * 100:>5.2f}%", style="blue")
    values.append("        ")
    values.append(f"{grading_group.weight * 100:>5.2f}%", style="magenta")

    # Combine everything in a panel
    content = Group(
        task_table,
        Text("\nContribution Progress:", style="bold cyan"),
        progress_text,
        legend,
        values,
    )

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
