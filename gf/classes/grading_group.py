from rich import box
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .task import Task, isProperFraction


def defaultRawGradingFunction(tasks: list) -> float:
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


def defaultTrueRawGradingFunction(tasks: list) -> float:
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


def defaultExpectedRawGradingFunction(tasks: list) -> float:
    """Calculate the expected raw grade for a list of tasks.
    Uses expected_grade if available, falls back to base_grade.

    Args:
        tasks (list): List of Task objects to grade

    Returns:
        float: Average expected grade between 0 and 1, or 0 if no tasks
    """
    assert isinstance(tasks, list)

    if tasks:
        return sum(
            task.expected_grade if task.expected_grade is not None else task.base_grade
            for task in tasks
        ) / len(tasks)
    return 0


class GradingGroup:
    """grading_function returns a floating point number representing the raw grade (before weight) and is given the list of tasks"""

    def __init__(
        self,
        name: str,
        weight: float,
        tasks: list,
        default_pst: float = 5,
        base_grade: float = 0.5,
        expected_grade: float | None = None,
        late_policy: str | None = None,
        gradingFunction=defaultRawGradingFunction,
        trueGradingFunction=defaultTrueRawGradingFunction,
        expectedGradingFunction=defaultExpectedRawGradingFunction,
    ):
        assert isinstance(name, str)
        assert isProperFraction(weight)
        assert isinstance(default_pst, (float, int))
        assert isProperFraction(base_grade)
        # assert isProperFraction(expected_grade)

        self.name = name
        self.weight = weight
        self.default_pst = default_pst
        self.base_grade = base_grade
        self.gradingFunction = gradingFunction
        self.late_policy = late_policy

        if gradingFunction != defaultRawGradingFunction:
            trueGradingFunction = gradingFunction
            expectedGradingFunction = gradingFunction
        self.trueGradingFunction = trueGradingFunction
        self.expectedGradingFunction = expectedGradingFunction

        if expected_grade is None:
            expected_grade = base_grade
        self.expected_grade = expected_grade

        if isinstance(tasks, int):
            tasks = self.createEnumeratedTasks(tasks)
        elif isinstance(tasks, Task):
            tasks = [tasks]
        assert isinstance(tasks, list) and (isinstance(tasks[0], Task) if len(tasks) > 0 else True)
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
        # Create table for tasks
        task_table = Table(box=box.SIMPLE, show_header=True, padding=(0, 2))
        task_table.add_column("Task", style="cyan")
        task_table.add_column("Grades", style="green")
        task_table.add_column("Course Contribution", style="yellow")

        for task in self.tasks:
            task_table.add_row(
                task.name,
                (
                    f"{float(task.grade or 0) * 100:>5.1f}% "
                    f"(base {float(task.base_grade) * 100:>4.1f}%) "
                    f"(expected {float(task.expected_grade) * 100:>4.1f}%)"
                ),
                f"{self.getMarginalGradePerHour(task) * 100:>5.2f}%/hr",
            )

        # Get completed tasks for current grade calculation
        completed_tasks = [task for task in self.tasks if task.grade is not None]
        current_grade = (
            (sum(task.grade for task in completed_tasks) / len(completed_tasks) * 100)
            if completed_tasks
            else 0
        )

        # Create contribution summary
        contributions = Text.assemble(
            ("NO WORK GRADE", "red"),
            f" = {self.getTrueContribution() * 100:>5.2f}% │ ",
            ("MIN WORK GRADE", "yellow"),
            f" = {self.getContribution() * 100:>5.2f}% │ ",
            ("CURRENT GRADE", "green"),
            f" = {current_grade:>5.2f}% │ ",  # <--- [CHANGED] Now shows raw percentage for completed assignments
            ("EXPECTED GRADE", "blue"),
            f" = {self.getExpectedContribution() * 100:>5.2f}%",
        )

        # Combine everything in a panel
        content = Group(task_table, Text("\nContributions:", style="bold white"), contributions)

        panel = Panel(
            content,
            title=f"[bold cyan]{self.name.upper()}[/bold cyan] [yellow](weight = {self.weight * 100:.1f}%)[/yellow]",
            border_style="blue",
            box=box.ROUNDED,
        )

        # Convert to string representation
        from rich.console import Console

        console = Console(record=True)
        console.print(panel)
        return console.export_text()

    def __repr__(self) -> str:
        """Returns a simple string representation of the grading group."""
        return self.name

    def createEnumeratedTasks(self, n) -> list:
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

    def getRawContribution(self) -> float:
        """Calculate the raw grade contribution before weighting."""
        return self.gradingFunction(self.tasks)

    def getContribution(self) -> float:
        """Calculate the weighted grade contribution."""
        return self.getRawContribution() * self.weight

    def getTaskContribution(self, task: Task) -> float:
        """Calculate a single task's contribution to the final grade.

        Args:
            task (Task|str): Task object or task name

        Returns:
            float: Task's contribution to final grade
        """
        if isinstance(task, str):
            task = self.getTask(task)
        assert isinstance(task, Task)

        grade = task.grade if task.grade is not None else task.base_grade
        total_tasks = len(self.tasks)
        return self.weight * (grade / total_tasks)

    def getMaxTaskContribution(self, task: Task) -> float:
        """Calculate a task's maximum possible contribution.

        Args:
            task (Task|str): Task object or task name

        Returns:
            float: Maximum possible contribution to final grade
        """
        if isinstance(task, str):
            task = self.getTask(task)
        assert isinstance(task, Task)

        grade = 1
        total_tasks = len(self.tasks)
        return self.weight * (grade / total_tasks)

    def getTask(self, name) -> Task:
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

    def getMarginalGradePerHour(self, task: Task) -> float:
        """Calculate marginal grade increase per hour for a task.

        Args:
            task (Task|str): Task object or task name

        Returns:
            float: Grade increase per hour
        """
        if isinstance(task, str):
            task = self.getTask(task)
        assert isinstance(task, Task)

        weight = self.weight
        total_tasks = len(self.tasks)
        return weight * (task.getMarginalGradePerHour() / total_tasks)

    def getCurrentRawContribution(self) -> float:
        """Calculate raw contribution from only graded tasks.
        Returns the average grade of completed assignments.
        """
        completed_tasks = [task for task in self.tasks if task.grade is not None]
        if not completed_tasks:
            return 0

        # Calculate average grade of completed tasks
        total_grade = sum(task.grade for task in completed_tasks)
        return total_grade / len(completed_tasks)

    def getCurrentContribution(self) -> float:
        """Calculate weighted contribution from only graded tasks.
        For the current grade calculation, we want this to represent the
        actual grade earned on completed work.
        """
        completed_tasks = [task for task in self.tasks if task.grade is not None]
        if not completed_tasks:
            return 0

        # Get average grade as a percentage
        raw_grade = self.getCurrentRawContribution()

        # Calculate what portion of the total weight this group has completed
        weight_per_task = self.weight / len(self.tasks)
        completed_weight = weight_per_task * len(completed_tasks)

        # Return
        return raw_grade * completed_weight

    def getTrueRawContribution(self) -> float:
        """Calculate raw contribution assuming no work done."""
        return self.trueGradingFunction(self.tasks)

    def getTrueContribution(self) -> float:
        """Calculate weighted contribution assuming no work done."""
        return self.getTrueRawContribution() * self.weight

    def getExpectedRawContribution(self) -> float:
        """Returns the expected raw grade (before weight) for this grading group."""
        return self.expectedGradingFunction(self.tasks)

    def getExpectedContribution(self) -> float:
        """Returns the expected contribution of this grading group to the final grade."""
        raw_contribution = self.getExpectedRawContribution()
        return raw_contribution * self.weight
