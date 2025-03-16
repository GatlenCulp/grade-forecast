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
        contributions = Text.assemble(
            "\nCONTRIBUTIONS --- ",
            ("NO WORK GRADE", "red"),
            f" = {group.get_true_contribution() * 100:>5.2f}% | ",
            ("MIN WORK GRADE", "yellow"),
            f" = {group.get_contribution() * 100:>5.2f}% | ",
            ("CURRENT GRADE", "green"),
            f" = {group.get_current_contribution() * 100:>5.2f}% | ",
            ("EXPECTED GRADE", "blue"),
            f" = {group.get_expected_contribution() * 100:>5.2f}% | ",
            ("MAX CONTRIBUTION", "magenta"),
            f" = {group.weight * 100:>5.2f}%",
        )

        group_tables.extend(
            [
                Text(f"\n{group.name}", style="bold cyan"),
                task_table,
                contributions,
                Text("\n"),  # Spacing between groups
            ]
        )

    # Create grade summary table with consistent formatting
    grade_table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    grade_table.add_column("Type", style="bold cyan", width=20)
    grade_table.add_column("Value", style="green", width=15)
    grade_table.add_column("Letter", style="yellow", width=10)

    grade_table.add_row(
        "EXPECTED GRADE",
        f"{course.get_expected_grade() * 100:<6.2f}%",
        f"({course.get_letter_grade(course.get_expected_grade())})",
    )
    grade_table.add_row(
        "CURRENT GRADE",
        f"{course.get_current_grade() * 100:<6.2f}%",
        f"({course.get_letter_grade(course.get_current_grade())})",
    )
    grade_table.add_row(
        "MIN WORK GRADE",
        f"{course.get_grade() * 100:<6.2f}%",
        f"({course.get_letter_grade(course.get_grade())})",
    )
    grade_table.add_row(
        "NO WORK GRADE",
        f"{course.get_true_grade() * 100:<6.2f}%",
        f"({course.get_letter_grade(course.get_true_grade())})",
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
        Text("\nGrade Summary:", style="bold cyan"),
        grade_table,
        Text("\nGrade Boundaries:", style="bold cyan"),
        boundaries_table,
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
