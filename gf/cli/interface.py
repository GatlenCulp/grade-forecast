"""Main interface for the grade forecast CLI."""

from rich.console import Console
from rich.prompt import Prompt
from rich.traceback import install

from configs import configs
from configs.examples.prog_fund import prog_fund
from gf.cli.display import (
    display_course_details,
    display_course_info,
    display_courses_table,
    display_task_analysis,
)
from gf.cli.utils import find_course, find_task

# Enable Rich's pretty traceback
install()

# Get courses from config
courses = configs if configs else [prog_fund]
console = Console()


def interface() -> None:
    """Main interface function for the grade forecast CLI."""
    console.print("[bold cyan]Welcome to Grade Forecast![/bold cyan]")

    display_courses_table(courses)

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

            selected_course = find_course(course_select, courses)
            if selected_course is None:
                console.print("[bold red]Error:[/bold red] Course not found.", style="bold red")
                continue

            display_course_details(selected_course)
            continue

        try:
            selected_course = find_course(user_input, courses)
            if selected_course is None:
                console.print("[bold red]Error:[/bold red] Course not found.", style="bold red")
                continue

            all_tasks = display_course_info(selected_course)

            analyze_task = Prompt.ask(
                "\nWhich task would you like to analyze? (Enter task number, name, or 'no' to continue)",
                default="no",
            ).strip()

            if analyze_task.lower() == "0":
                display_course_details(selected_course)
                continue

            if analyze_task.lower() != "no":
                task = find_task(analyze_task, selected_course, all_tasks)
                if task is None:
                    console.print(
                        f"[bold red]Error:[/bold red] Task '{analyze_task}' not found.",
                        style="bold red",
                    )
                    continue

                display_task_analysis(selected_course, task)

        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {e}", style="bold red")


if __name__ == "__main__":
    interface()
