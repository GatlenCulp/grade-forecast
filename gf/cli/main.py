"""Main CLI entry point for the grade forecast application."""

import typer
from rich.console import Console
from rich.table import Table
from typing import List, Optional, Callable

from configs import configs
from configs.examples.prog_fund import prog_fund
from gf.cli.display import display_course_info, display_courses_table, display_task_analysis
from gf.cli.interface import interface
from gf.cli.utils import find_course, find_task

app = typer.Typer(help="Grade Forecast - Track and forecast your university grades")
courses = configs if configs else [prog_fund]
console = Console()

# Generate course aliases (first letter of each word in the course name)
course_aliases = {}
for course in courses:
    words = course.name.split()
    alias = "".join(word[0].lower() for word in words if word)
    # If alias already exists, add a number to it
    base_alias = alias
    counter = 1
    while alias in course_aliases.values():
        alias = f"{base_alias}{counter}"
        counter += 1
    course_aliases[course.name] = alias


def show_available_courses() -> None:
    """Show available courses with their aliases."""
    table = Table(title="Available Courses")
    table.add_column("Index", style="cyan")
    table.add_column("Course Name", style="green")
    table.add_column("Alias", style="yellow")

    for idx, course in enumerate(courses, start=1):
        table.add_row(str(idx), course.name, course_aliases[course.name])

    console.print(table)
    console.print("\n[bold cyan]Usage examples:[/bold cyan]")
    console.print(f"  grade-forecast course {courses[0].name}")
    console.print(f"  grade-forecast course {course_aliases[courses[0].name]}")


def course_callback(
    ctx: typer.Context, param: typer.CallbackParam, value: Optional[str]
) -> Optional[str]:
    """Callback for course name argument to show available courses if not provided."""
    if not value and not ctx.resilient_parsing:
        show_available_courses()
        raise typer.Exit()
    return value


@app.command()
def run() -> None:
    """Run the Grade Forecast interactive CLI application."""
    interface()


@app.command()
def list() -> None:
    """List all available courses."""
    display_courses_table(courses)


@app.command()
def summary() -> None:
    """Show a summary of all courses."""
    # Create a table to display course summaries
    table = Table(title="Course Summary")
    table.add_column("Course", style="cyan")
    table.add_column("Current Grade", style="green")
    table.add_column("Expected Grade", style="blue")
    table.add_column("Letter Grade", style="yellow")
    table.add_column("Tasks Completed", style="magenta")

    total_tasks = 0
    completed_tasks = 0

    for course in courses:
        # Count tasks
        course_total_tasks = 0
        course_completed_tasks = 0

        for group in course.grading_groups:
            for task in group.tasks:
                course_total_tasks += 1
                if task.grade is not None:
                    course_completed_tasks += 1

        total_tasks += course_total_tasks
        completed_tasks += course_completed_tasks

        # Add row to table
        table.add_row(
            course.name,
            f"{course.get_current_grade() * 100:.2f}%",
            f"{course.get_expected_grade() * 100:.2f}%",
            course.get_letter_grade(),
            f"{course_completed_tasks}/{course_total_tasks} ({course_completed_tasks / course_total_tasks * 100:.1f}%)",
        )

    # Add overall completion row
    if total_tasks > 0:
        completion_percentage = completed_tasks / total_tasks * 100
        table.add_row(
            "OVERALL",
            "",
            "",
            "",
            f"{completed_tasks}/{total_tasks} ({completion_percentage:.1f}%)",
        )

    console.print(table)


@app.command()
def course(
    course_name: str = typer.Argument(
        None, help="Name or alias of the course to display", callback=course_callback
    ),
    details: bool = typer.Option(False, "--details", "-d", help="Show detailed information"),
) -> None:
    """Display information for a specific course."""
    # First try to find by name
    selected_course = find_course(course_name, courses)

    # If not found, try to find by alias
    if selected_course is None:
        for c in courses:
            if course_aliases[c.name] == course_name.lower():
                selected_course = c
                break

    # If still not found, try to find by index
    if selected_course is None and course_name.isdigit():
        idx = int(course_name) - 1
        if 0 <= idx < len(courses):
            selected_course = courses[idx]

    if selected_course is None:
        console.print(f"[bold red]Error:[/bold red] Course '{course_name}' not found.")
        show_available_courses()
        return

    if details:
        from gf.cli.display import display_course_details

        display_course_details(selected_course)
    else:
        display_course_info(selected_course)


def task_course_callback(
    ctx: typer.Context, param: typer.CallbackParam, value: Optional[str]
) -> Optional[str]:
    """Callback for course name argument in task-related commands."""
    if not value and not ctx.resilient_parsing:
        show_available_courses()
        raise typer.Exit()
    return value


@app.command()
def tasks(
    course_name: str = typer.Argument(
        None, help="Name or alias of the course to list tasks for", callback=task_course_callback
    ),
) -> None:
    """List all tasks in a course."""
    # First try to find by name
    selected_course = find_course(course_name, courses)

    # If not found, try to find by alias
    if selected_course is None:
        for c in courses:
            if course_aliases[c.name] == course_name.lower():
                selected_course = c
                break

    # If still not found, try to find by index
    if selected_course is None and course_name.isdigit():
        idx = int(course_name) - 1
        if 0 <= idx < len(courses):
            selected_course = courses[idx]

    if selected_course is None:
        console.print(f"[bold red]Error:[/bold red] Course '{course_name}' not found.")
        show_available_courses()
        return

    # Create a table to display tasks
    table = Table(title=f"Tasks in {selected_course.name}")
    table.add_column("Index", style="cyan")
    table.add_column("Task Name", style="green")
    table.add_column("Group", style="yellow")
    table.add_column("Status", style="magenta")
    table.add_column("Grade", style="blue")

    # Get all tasks from the course
    all_tasks = []
    for group in selected_course.grading_groups:
        for task in group.tasks:
            all_tasks.append((task, group))

    # Add tasks to the table
    for idx, (task, group) in enumerate(all_tasks, start=1):
        status = "Completed" if task.grade is not None else "Not Completed"
        grade = f"{task.grade * 100:.1f}%" if task.grade is not None else "N/A"
        table.add_row(str(idx), task.name, group.name, status, grade)

    console.print(table)


def task_callback(
    ctx: typer.Context, param: typer.CallbackParam, value: Optional[str]
) -> Optional[str]:
    """Callback for task name argument to show available tasks if not provided."""
    # We can't show tasks here because we don't know the course yet
    # The course parameter will be handled by its own callback
    return value


@app.command()
def task(
    course_name: str = typer.Argument(
        None, help="Name or alias of the course containing the task", callback=task_course_callback
    ),
    task_name: Optional[str] = typer.Argument(None, help="Name or index of the task to analyze"),
) -> None:
    """Analyze a specific task within a course."""
    # First try to find by name
    selected_course = find_course(course_name, courses)

    # If not found, try to find by alias
    if selected_course is None:
        for c in courses:
            if course_aliases[c.name] == course_name.lower():
                selected_course = c
                break

    # If still not found, try to find by index
    if selected_course is None and course_name.isdigit():
        idx = int(course_name) - 1
        if 0 <= idx < len(courses):
            selected_course = courses[idx]

    if selected_course is None:
        console.print(f"[bold red]Error:[/bold red] Course '{course_name}' not found.")
        show_available_courses()
        return

    # Get all tasks from the course
    all_tasks = []
    for group in selected_course.grading_groups:
        all_tasks.extend(group.tasks)

    # If task_name is not provided, show available tasks
    if task_name is None:
        table = Table(title=f"Tasks in {selected_course.name}")
        table.add_column("Index", style="cyan")
        table.add_column("Task Name", style="green")
        table.add_column("Group", style="yellow")
        table.add_column("Status", style="magenta")

        for idx, task in enumerate(all_tasks, start=1):
            group = selected_course.get_parent(task)
            status = "Completed" if task.grade is not None else "Not Completed"
            table.add_row(str(idx), task.name, group.name, status)

        console.print(table)
        console.print("\n[bold cyan]Usage example:[/bold cyan]")
        if all_tasks:
            console.print(f'  grade-forecast task {course_name} "{all_tasks[0].name}"')
            console.print(f"  grade-forecast task {course_name} 1")
        return

    # Find the task
    selected_task = find_task(task_name, selected_course, all_tasks)

    if selected_task is None:
        console.print(
            f"[bold red]Error:[/bold red] Task '{task_name}' not found in course '{selected_course.name}'."
        )
        table = Table(title=f"Tasks in {selected_course.name}")
        table.add_column("Index", style="cyan")
        table.add_column("Task Name", style="green")

        for idx, task in enumerate(all_tasks, start=1):
            table.add_row(str(idx), task.name)

        console.print(table)
        return

    display_task_analysis(selected_course, selected_task)


@app.command()
def update(
    course_name: str = typer.Argument(
        None, help="Name or alias of the course containing the task", callback=task_course_callback
    ),
    task_name: Optional[str] = typer.Argument(None, help="Name or index of the task to update"),
    grade: Optional[float] = typer.Argument(None, help="New grade for the task (0-100)"),
) -> None:
    """Update a task's grade."""
    # First try to find by name
    selected_course = find_course(course_name, courses)

    # If not found, try to find by alias
    if selected_course is None:
        for c in courses:
            if course_aliases[c.name] == course_name.lower():
                selected_course = c
                break

    # If still not found, try to find by index
    if selected_course is None and course_name.isdigit():
        idx = int(course_name) - 1
        if 0 <= idx < len(courses):
            selected_course = courses[idx]

    if selected_course is None:
        console.print(f"[bold red]Error:[/bold red] Course '{course_name}' not found.")
        show_available_courses()
        return

    # Get all tasks from the course
    all_tasks = []
    for group in selected_course.grading_groups:
        all_tasks.extend(group.tasks)

    # If task_name is not provided, show available tasks
    if task_name is None:
        table = Table(title=f"Tasks in {selected_course.name}")
        table.add_column("Index", style="cyan")
        table.add_column("Task Name", style="green")
        table.add_column("Group", style="yellow")
        table.add_column("Current Grade", style="blue")

        for idx, task in enumerate(all_tasks, start=1):
            group = selected_course.get_parent(task)
            current_grade = f"{task.grade * 100:.1f}%" if task.grade is not None else "Not graded"
            table.add_row(str(idx), task.name, group.name, current_grade)

        console.print(table)
        console.print("\n[bold cyan]Usage example:[/bold cyan]")
        if all_tasks:
            console.print(f'  grade-forecast update {course_name} "{all_tasks[0].name}" 95')
            console.print(f"  grade-forecast update {course_name} 1 95")
        return

    # Find the task
    selected_task = find_task(task_name, selected_course, all_tasks)

    if selected_task is None:
        console.print(
            f"[bold red]Error:[/bold red] Task '{task_name}' not found in course '{selected_course.name}'."
        )
        table = Table(title=f"Tasks in {selected_course.name}")
        table.add_column("Index", style="cyan")
        table.add_column("Task Name", style="green")

        for idx, task in enumerate(all_tasks, start=1):
            table.add_row(str(idx), task.name)

        console.print(table)
        return

    # If grade is not provided, prompt for it
    if grade is None:
        current_grade = (
            f"{selected_task.grade * 100:.1f}%" if selected_task.grade is not None else "Not graded"
        )
        console.print(f"Current grade for '{selected_task.name}': {current_grade}")
        grade_input = typer.prompt("Enter new grade (0-100)")
        try:
            grade = float(grade_input)
        except ValueError:
            console.print("[bold red]Error:[/bold red] Grade must be a number.")
            return

    # Validate and set the grade
    if grade < 0 or grade > 100:
        console.print("[bold red]Error:[/bold red] Grade must be between 0 and 100.")
        return

    # Convert percentage to decimal
    decimal_grade = grade / 100.0

    # Update the task's grade
    selected_task.set_grade(decimal_grade)

    console.print(f"Updated grade for '{selected_task.name}' to {grade:.1f}%")

    # Show the updated course information
    display_course_info(selected_course)


@app.command()
def compare(
    course_names: Optional[List[str]] = typer.Argument(
        None, help="Names or aliases of courses to compare"
    ),
) -> None:
    """Compare multiple courses."""
    if not course_names:
        show_available_courses()
        console.print("\n[bold cyan]Usage example:[/bold cyan]")
        if len(courses) >= 2:
            console.print(f"  grade-forecast compare {courses[0].name} {courses[1].name}")
            console.print(
                f"  grade-forecast compare {course_aliases[courses[0].name]} {course_aliases[courses[1].name]}"
            )
        return

    selected_courses = []
    for name in course_names:
        # First try to find by name
        course = find_course(name, courses)

        # If not found, try to find by alias
        if course is None:
            for c in courses:
                if course_aliases[c.name] == name.lower():
                    course = c
                    break

        # If still not found, try to find by index
        if course is None and name.isdigit():
            idx = int(name) - 1
            if 0 <= idx < len(courses):
                course = courses[idx]

        if course is None:
            console.print(f"[bold red]Error:[/bold red] Course '{name}' not found.")
            continue
        selected_courses.append(course)

    if not selected_courses:
        console.print("[bold red]No valid courses found for comparison.[/bold red]")
        show_available_courses()
        return

    # Create a table to compare courses
    table = Table(title="Course Comparison")
    table.add_column("Course", style="cyan")
    table.add_column("Current Grade", style="green")
    table.add_column("Expected Grade", style="blue")
    table.add_column("Letter Grade", style="yellow")
    table.add_column("Care Factor", style="magenta")

    for course in selected_courses:
        table.add_row(
            course.name,
            f"{course.get_current_grade() * 100:.2f}%",
            f"{course.get_expected_grade() * 100:.2f}%",
            course.get_letter_grade(),
            f"{course.care_factor}",
        )

    console.print(table)


if __name__ == "__main__":
    app()
