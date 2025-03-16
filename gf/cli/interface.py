import copy

# Save the figure to a temporary buffer and display it using Rich's Image
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from rich import box
from rich.console import Console, Group

# Display the image using Rich
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich.traceback import install

from configs import configs
from configs.examples.prog_fund import prog_fund
from gf.classes import Course, Task

# Enable Rich's pretty traceback
install()

"""
This script lays out the Rich-enhanced command line interface.
"""

courses = configs if configs else [prog_fund]
console = Console()


def plot_course_grade_vs_grade(course: Course, name: str) -> matplotlib.lines.Line2D:
    """Plot how a task's grade affects the course grade."""
    # Create a copy of the course to avoid modifying the original
    course_copy = copy.deepcopy(course)

    # Get the task by name
    task = course_copy.get_task(name)

    # Create arrays for x and y values
    x = np.linspace(0, 1, 100)
    y = []

    # Calculate course grade for each task grade
    for grade in x:
        task.set_grade(grade)
        y.append(course_copy.get_grade())

    # Create the plot
    plt.figure(figsize=(10, 6))
    (line,) = plt.plot(x, y, "b-")
    plt.xlabel("Task Grade")
    plt.ylabel("Course Grade")
    plt.title(f"Effect of {name} on Course Grade")
    plt.grid(True)

    return line


def _display_courses_table(courses: list[Course]) -> None:
    """Display available courses in a formatted table."""
    table = Table(title="Available Courses", header_style="bold magenta")
    table.add_column("Index", justify="right", style="cyan", no_wrap=True)
    table.add_column("Course Name", style="green")
    table.add_column("Action", style="yellow")

    table.add_row("0", "Course Details", "Show detailed grade breakdown")
    for idx, course in enumerate(courses, start=1):
        table.add_row(str(idx), course.name, "Analyze tasks")

    console.print(table)


def _find_course(course_input: str, courses: list[Course]) -> Course | None:
    """Find course by index or name."""
    if course_input.isdigit():
        idx = int(course_input) - 1
        if 0 <= idx < len(courses):
            return courses[idx]
    else:
        for course in courses:
            if course_input.lower() == course.name.lower():
                return course
    return None


def _display_course_details(course: Course) -> None:
    """Display detailed course breakdown."""
    # Create tables for each grading group
    group_tables = []
    for group in course.grading_groups:
        # Create table for tasks in this group
        task_table = Table(box=box.SIMPLE, show_header=True, padding=(0, 2))
        task_table.add_column("Task", style="cyan")
        task_table.add_column("Grades", style="green")
        task_table.add_column("Course Contribution", style="yellow")

        for task in group.tasks:
            if task.grade is not None:
                grade_display = f"{task.grade * 100:>4.1f}% (base {task.base_grade * 100:>4.1f}%) (expected {task.expected_grade * 100:>4.1f}%)"
            else:
                grade_display = f"Not graded (base {task.base_grade * 100:>4.1f}%) (expected {task.expected_grade * 100:>4.1f}%)"

            task_table.add_row(
                task.name,
                grade_display,
                f"{course.get_marginal_grade_per_hour(task) * 100:>4.2f}%/hr course grade contribution",
            )

        # Create contribution summary
        contributions = Text.assemble(
            "\nCONTRIBUTIONS --- ",
            ("NO WORK GRADE", "red"),
            f" = {group.get_true_contribution() * 100:>4.2f}% | ",
            ("MIN WORK GRADE", "yellow"),
            f" = {group.get_contribution() * 100:>4.2f}% | ",
            ("CURRENT GRADE", "green"),
            f" = {group.get_current_contribution() * 100:>4.2f}% | ",
            ("EXPECTED GRADE", "blue"),
            f" = {group.get_expected_contribution() * 100:>4.2f}%",
        )

        group_tables.extend(
            [
                Text(f"\n{group.name}", style="bold white"),
                task_table,
                contributions,
                Text("\n"),  # Spacing between groups
            ]
        )

    # Create grade summary table
    grade_table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    grade_table.add_column("Type", style="bold cyan")
    grade_table.add_column("Value", style="green")
    grade_table.add_column("Letter", style="yellow")

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

    # Create boundaries table
    boundaries_table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    boundaries_table.add_column("Grade", style="bold magenta")
    boundaries_table.add_column("Range", style="blue")

    for letter, (lower, upper) in course.grading_boundaries.items():
        boundaries_table.add_row(letter, f"{lower}% - {upper}%")

    # Combine everything in a panel
    content = Group(
        *group_tables,
        Text("\nGrade Summary:", style="bold white"),
        grade_table,
        Text("\nGrade Boundaries:", style="bold white"),
        boundaries_table,
    )

    panel = Panel(
        content,
        title=f"[bold red]COURSE: {course.name}[/bold red]",
        border_style="blue",
    )

    console.print(panel)


def _display_course_info(course: Course) -> list:
    """Display course information and return list of all tasks."""
    # Create table for task groups
    tasks_table = Table(box=box.ROUNDED, show_header=True, padding=(0, 2))
    tasks_table.add_column("Group", style="bold cyan")
    tasks_table.add_column("Weight", style="yellow")
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
    grade_table.add_column("Type", style="bold cyan")
    grade_table.add_column("Value", style="green")
    grade_table.add_column("Letter", style="yellow")

    # Add current grades
    grade_table.add_row(
        "Current Grade",
        f"{course.get_current_grade() * 100:<6.2f}%",
        f"({course.get_letter_grade(course.get_current_grade())})",
    )
    grade_table.add_row(
        "Expected Grade",
        f"{course.get_expected_grade() * 100:<6.2f}%",
        f"({course.get_letter_grade(course.get_expected_grade())})",
    )

    # Create group of renderable elements
    content = Group(tasks_table, Text("\nGrade Summary:", style="bold white"), grade_table)

    # Create panel with the group
    panel = Panel(
        content,
        title=f"[bold red]{course.name} Overview[/bold red]",
        border_style="green",
    )

    console.print(panel)
    return all_tasks


def _find_task(task_input: str, course: Course, all_tasks: list) -> Task | None:
    """Find task by index or name."""
    task = None
    if task_input.isdigit():
        idx = int(task_input) - 1
        if 0 <= idx < len(all_tasks):
            task = all_tasks[idx]
    else:
        task = course.get_task(task_input)
    return task


def _display_task_analysis(course: Course, task: Task) -> None:
    """Display task analysis information and plot."""
    gg = course.get_parent(task)
    mgph = course.get_marginal_grade_per_hour(task)
    mgph_tasklevel = task.get_marginal_grade_per_hour()

    info_text = Text()
    info_text.append(f"--- {task} of {course.name} ---\n", style="bold cyan")
    info_text.append(
        f"ΔCG = {mgph * 100:.4f}%/hr * (t hours) + "
        f"{task.base_grade * gg.weight / len(gg.tasks) * 100:.4f}% "
        f"for (0 < t < {task.pst}) -> "
        f"Max Contribution = {gg.get_max_task_contribution(task) * 100:.4f}%\n",
        style="white",
    )
    info_text.append(
        f"ΔG = {mgph_tasklevel * 100:.4f}%/hr * (t hours) + "
        f"{task.base_grade * 100:.4f}% "
        f"for (0 < t < {task.pst}) -> "
        f"Max Grade = 100%\n",
        style="white",
    )
    info_text.append(
        f"Assuming without additional work, you get a {task.base_grade * 100:.2f}% "
        f"and with {task.pst} hours of work you can get a 100%.",
        style="white",
    )

    console.print(Panel(info_text, title="Task Information", border_style="green"))

    fig = plot_course_grade_vs_grade(course, task.name)
    plt.show()
    plt.close(fig)


def interface():
    """Main interface function."""
    _display_courses_table(courses)

    while True:
        user_input = Prompt.ask(
            "\nWhich course would you like to learn more about? (Enter course name or index, or 'exit' to quit)",
            default="",
        ).strip()

        if user_input.lower() == "exit":
            console.print("Exiting the application. Goodbye!", style="bold red")
            break

        if user_input == "0":
            course_select = Prompt.ask(
                "\nWhich course would you like to see details for? (Enter course name or index)",
                default="1",
            ).strip()

            selected_course = _find_course(course_select, courses)
            if selected_course is None:
                console.print("[bold red]Error:[/bold red] Course not found.", style="bold red")
                continue

            _display_course_details(selected_course)
            continue

        try:
            selected_course = _find_course(user_input, courses)
            if selected_course is None:
                console.print("[bold red]Error:[/bold red] Course not found.", style="bold red")
                continue

            all_tasks = _display_course_info(selected_course)

            analyze_task = Prompt.ask(
                "\nWhich task would you like to analyze? (Enter task number, name, or 'no' to continue)",
                default="no",
            ).strip()

            if analyze_task.lower() == "0":
                _display_course_details(selected_course)
                continue

            if analyze_task.lower() != "no":
                task = _find_task(analyze_task, selected_course, all_tasks)
                if task is None:
                    console.print(
                        f"[bold red]Error:[/bold red] Task '{analyze_task}' not found.",
                        style="bold red",
                    )
                    continue

                _display_task_analysis(selected_course, task)

        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {e}", style="bold red")


if __name__ == "__main__":
    interface()
