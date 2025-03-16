"""Display functions for the grade forecast CLI."""

import matplotlib.pyplot as plt
from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from gf.classes import Course, Task
from gf.cli.plotting import plot_course_grade_vs_grade

# Create console for rich output
console = Console()


def display_courses_table(courses: list[Course]) -> None:
    """Display available courses in a formatted table.

    Args:
        courses: List of available courses
    """
    table = Table(title="Available Courses", header_style="bold magenta")
    table.add_column("Index", justify="right", style="cyan", no_wrap=True)
    table.add_column("Course Name", style="green")
    table.add_column("Action", style="yellow")

    table.add_row("0", "Course Details", "Show detailed grade breakdown")
    for idx, course in enumerate(courses, start=1):
        table.add_row(str(idx), course.name, "Analyze tasks")

    console.print(table)


def display_course_details(course: Course) -> None:
    """Display detailed course breakdown.

    Args:
        course: The course to display details for
    """
    # Create tables for each grading group
    group_tables = []
    for group in course.grading_groups:
        # Create table for tasks in this group
        task_table = Table(box=box.SIMPLE, show_header=True, padding=(0, 2))
        task_table.add_column("Task", style="cyan", width=30)
        task_table.add_column("Grades", style="green", width=40)
        task_table.add_column("Course Contribution", style="yellow", width=30)

        for task in group.tasks:
            if task.grade is not None:
                grade_display = f"{task.grade * 100:>5.1f}% (base {task.base_grade * 100:>5.1f}%) (expected {task.expected_grade * 100:>5.1f}%)"
            else:
                grade_display = f"Not graded (base {task.base_grade * 100:>5.1f}%) (expected {task.expected_grade * 100:>5.1f}%)"

            task_table.add_row(
                task.name,
                grade_display,
                f"{course.get_marginal_grade_per_hour(task) * 100:>5.2f}%/hr course grade contribution",
            )

        # Create contribution summary with consistent formatting
        max_width = 50  # Width of the progress bar
        max_contribution = group.weight * 100

        # Calculate positions for each marker on the progress bar
        no_work_pos = int((group.get_true_contribution() * 100 / max_contribution) * max_width)
        min_work_pos = int((group.get_contribution() * 100 / max_contribution) * max_width)
        current_pos = int((group.get_current_contribution() * 100 / max_contribution) * max_width)
        expected_pos = int((group.get_expected_contribution() * 100 / max_contribution) * max_width)

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
        values.append(f"{group.get_true_contribution() * 100:>5.2f}%", style="red")
        values.append("        ")
        values.append(f"{group.get_contribution() * 100:>5.2f}%", style="yellow")
        values.append("        ")
        values.append(f"{group.get_current_contribution() * 100:>5.2f}%", style="green")
        values.append("        ")
        values.append(f"{group.get_expected_contribution() * 100:>5.2f}%", style="blue")
        values.append("        ")
        values.append(f"{group.weight * 100:>5.2f}%", style="magenta")

        group_tables.extend(
            [
                Text(f"\n{group.name}", style="bold cyan"),
                task_table,
                Text("\nContribution Progress:", style="bold cyan"),
                progress_text,
                legend,
                values,
                Text("\n"),  # Spacing between groups
            ]
        )

    # Create grade summary table with consistent formatting
    grade_table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    grade_table.add_column("Type", style="bold cyan", width=20)
    grade_table.add_column("Value", style="green", width=15)
    grade_table.add_column("Letter", style="yellow", width=10)

    # Get grade values
    expected_grade = course.get_expected_grade() * 100
    current_grade = course.get_current_grade() * 100
    min_work_grade = course.get_grade() * 100
    no_work_grade = course.get_true_grade() * 100

    grade_table.add_row(
        "EXPECTED GRADE",
        f"{expected_grade:<6.2f}%",
        f"({course.get_letter_grade(course.get_expected_grade())})",
    )
    grade_table.add_row(
        "CURRENT GRADE",
        f"{current_grade:<6.2f}%",
        f"({course.get_letter_grade(course.get_current_grade())})",
    )
    grade_table.add_row(
        "MIN WORK GRADE",
        f"{min_work_grade:<6.2f}%",
        f"({course.get_letter_grade(course.get_grade())})",
    )
    grade_table.add_row(
        "NO WORK GRADE",
        f"{no_work_grade:<6.2f}%",
        f"({course.get_letter_grade(course.get_true_grade())})",
    )

    # Create grade progress bar
    max_width = 60  # Width of the progress bar
    max_grade = 100  # Maximum possible grade

    # Create a list to track where boundary markers should go
    boundary_positions = {}

    # Find boundary positions
    boundaries_sorted = sorted(course.grading_boundaries.items(), key=lambda x: x[1][0])
    for letter, (lower, upper) in boundaries_sorted:
        if lower > 0:  # Skip the lowest boundary (usually 0)
            pos = int((lower / max_grade) * max_width)
            if pos < max_width:
                boundary_positions[pos] = letter

    # Calculate positions for grade markers
    no_work_pos = int((no_work_grade / max_grade) * max_width)
    min_work_pos = int((min_work_grade / max_grade) * max_width)
    current_pos = int((current_grade / max_grade) * max_width)
    expected_pos = int((expected_grade / max_grade) * max_width)

    # Create the progress bar with boundary markers and grade markers included
    progress_text = Text()
    for i in range(max_width):
        # Check if this position has a grade marker
        if i == no_work_pos:
            progress_text.append("▼", style="red")
        elif i == min_work_pos:
            progress_text.append("▼", style="yellow")
        elif i == current_pos:
            progress_text.append("▼", style="green")
        elif i == expected_pos:
            progress_text.append("▼", style="blue")
        # Check if this position has a boundary marker
        elif i in boundary_positions:
            progress_text.append("┃", style="bold magenta")
        else:
            progress_text.append("─")

    # Add boundary labels (directly above the markers)
    boundary_labels = Text()
    boundary_labels.append("\n")

    # Create a string of spaces for positioning
    label_spaces = [" "] * max_width

    # Add letter labels at boundary positions
    for pos, letter in boundary_positions.items():
        label_spaces[pos] = letter

    # Convert to a string and add to boundary_labels
    boundary_labels.append("".join(label_spaces), style="bold magenta")

    # Create the legend for grade summary
    grade_legend = Text()
    grade_legend.append("\n\n")
    grade_legend.append("▼", style="red")
    grade_legend.append(" NO WORK ", style="red")
    grade_legend.append("    ")
    grade_legend.append("▼", style="yellow")
    grade_legend.append(" MIN WORK ", style="yellow")
    grade_legend.append("    ")
    grade_legend.append("▼", style="green")
    grade_legend.append(" CURRENT ", style="green")
    grade_legend.append("    ")
    grade_legend.append("▼", style="blue")
    grade_legend.append(" EXPECTED ", style="blue")
    grade_legend.append("    ")
    grade_legend.append("┃", style="magenta")
    grade_legend.append(" GRADE BOUNDARY", style="magenta")

    # Add grade values directly to the legend
    grade_values = Text()
    grade_values.append("\n")
    grade_values.append(f"NO WORK: {no_work_grade:.2f}%  ", style="red")
    grade_values.append(f"MIN WORK: {min_work_grade:.2f}%  ", style="yellow")
    grade_values.append(f"CURRENT: {current_grade:.2f}%  ", style="green")
    grade_values.append(f"EXPECTED: {expected_grade:.2f}%", style="blue")

    # Create the grade progress bar group
    grade_progress = Group(
        Text("\nGrade Progress:", style="bold cyan"),
        progress_text,
        boundary_labels,
        grade_legend,
        grade_values,
    )

    # Create boundaries table with consistent formatting
    boundaries_table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    boundaries_table.add_column("Grade", style="bold magenta", width=10)
    boundaries_table.add_column("Range", style="blue", width=20)

    for letter, (lower, upper) in course.grading_boundaries.items():
        boundaries_table.add_row(letter, f"{lower}% - {upper}%")

    # Combine everything in a panel
    content = Group(
        *group_tables,
        grade_progress,
    )

    panel = Panel(
        content,
        title=f"[bold cyan]COURSE: {course.name}[/bold cyan]",
        border_style="blue",
    )

    console.print(panel)


def display_course_info(course: Course) -> list[Task]:
    """Display course information and return list of all tasks.

    Args:
        course: The course to display information for

    Returns:
        List[Task]: List of all tasks in the course
    """
    # Create table for task groups
    tasks_table = Table(box=box.ROUNDED, show_header=True, padding=(0, 2))
    tasks_table.add_column("Group", style="bold cyan", width=25)
    tasks_table.add_column("Weight", style="yellow", width=15)
    tasks_table.add_column("Tasks", style="green")

    all_tasks = []

    for group in course.grading_groups:
        task_list = []
        for task in group.tasks:
            all_tasks.append(task)
            task_idx = len(all_tasks)
            task_list.append(f"[{task_idx}] {task.name}")

        tasks_table.add_row(group.name, f"{group.weight * 100:.1f}%", ", ".join(task_list))

    # Create grade summary table
    grade_table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    grade_table.add_column("Type", style="bold cyan", width=20)
    grade_table.add_column("Value", style="green", width=15)
    grade_table.add_column("Letter", style="yellow", width=10)

    # Add current grades
    grade_table.add_row(
        "CURRENT GRADE",
        f"{course.get_current_grade() * 100:<6.2f}%",
        f"({course.get_letter_grade(course.get_current_grade())})",
    )
    grade_table.add_row(
        "EXPECTED GRADE",
        f"{course.get_expected_grade() * 100:<6.2f}%",
        f"({course.get_letter_grade(course.get_expected_grade())})",
    )

    # Create group of renderable elements
    content = Group(tasks_table, Text("\nGrade Summary:", style="bold cyan"), grade_table)

    # Create panel with the group
    panel = Panel(
        content,
        title=f"[bold cyan]{course.name} Overview[/bold cyan]",
        border_style="blue",
    )

    console.print(panel)
    return all_tasks


def display_task_analysis(course: Course, task: Task) -> None:
    """Display task analysis information and plot.

    Args:
        course: The course containing the task
        task: The task to analyze
    """
    group = course.get_parent(task)
    mgph = course.get_marginal_grade_per_hour(task)
    mgph_tasklevel = task.get_marginal_grade_per_hour()

    # Create a table for task details
    task_table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    task_table.add_column("Property", style="bold cyan", width=20)
    task_table.add_column("Value", style="green")

    # Add task details
    task_table.add_row("Task Name", task.name)
    task_table.add_row("Course", course.name)
    task_table.add_row("Group", group.name)
    task_table.add_row("Weight in Group", f"{1 / len(group.tasks):.4f}")
    task_table.add_row("Base Grade", f"{task.base_grade * 100:.2f}%")

    if task.grade is not None:
        task_table.add_row("Current Grade", f"{task.grade * 100:.2f}%")
    else:
        task_table.add_row("Current Grade", "Not graded")

    task_table.add_row("Expected Grade", f"{task.expected_grade * 100:.2f}%")
    task_table.add_row("Predicted Study Time", f"{task.pst} hours")
    task_table.add_row("Marginal Grade/Hour", f"{mgph_tasklevel * 100:.4f}%/hr")
    task_table.add_row("Course Grade Contribution/Hour", f"{mgph * 100:.4f}%/hr")
    task_table.add_row("Max Contribution", f"{group.get_max_task_contribution(task) * 100:.4f}%")

    # Formula explanation
    formula_text = Text()
    formula_text.append("\nGrade Formula:\n", style="bold cyan")
    formula_text.append(
        f"ΔCG = {mgph * 100:.4f}%/hr * (t hours) + "
        f"{task.base_grade * group.weight / len(group.tasks) * 100:.4f}% "
        f"for (0 < t < {task.pst})\n",
        style="yellow",
    )
    formula_text.append(
        f"ΔG = {mgph_tasklevel * 100:.4f}%/hr * (t hours) + "
        f"{task.base_grade * 100:.4f}% "
        f"for (0 < t < {task.pst})\n",
        style="yellow",
    )

    # Combine everything in a panel
    content = Group(task_table, formula_text)

    panel = Panel(
        content,
        title=f"[bold cyan]Task Analysis: {task.name}[/bold cyan]",
        border_style="blue",
    )

    console.print(panel)

    fig = plot_course_grade_vs_grade(course, task.name)
    plt.show()
    plt.close(fig)
