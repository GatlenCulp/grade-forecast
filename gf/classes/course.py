import math

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
    return 1 / (1 + (math.e) ** (x))


class Course:
    """RawUtility(grade [0-1]) [int]: Given the current grade, calculates how happy I will be. (Probably a function just mapping grade -> letter grade -> utility)
    Utility(grade [0-1]) [int]: RawUtility(grade) * care_factor
    CurrentUtility() [int]: Utility at the current grade
    """

    def __init__(
        self,
        name: str,
        care_factor: float,
        grading_groups: list,
        grading_boundaries: dict = default_grading_boundaries,
        grade_utils: dict = default_grade_utils,
        late_policy: str | None = None,
    ):
        total_weights = sum([gg.weight for gg in grading_groups])
        assert total_weights >= 0.99 and total_weights <= 1.01
        assert isinstance(grading_boundaries, dict)

        self.name = name
        self.care_factor = care_factor
        self.grading_groups = grading_groups
        self.grading_boundaries = grading_boundaries
        self.grade_utils = grade_utils
        self.late_policy = late_policy

    def getGrade(self) -> float:
        """The grade or "guaranteed grade" is the grade that you would get putting in MINIMAL effort"""
        return sum([gg.getContribution() for gg in self.grading_groups])

    def getCurrentGrade(self) -> float:
        """Calculate current grade as percentage of maximum possible for completed work.
        If school stopped now, this is what your grade would be based on completed assignments.
        """
        completed_weight = 0
        current_contribution = 0

        for group in self.grading_groups:
            completed_tasks = [task for task in group.tasks if task.grade is not None]
            if completed_tasks:
                # Calculate weight of completed assignments in this group
                group_completed_weight = (len(completed_tasks) / len(group.tasks)) * group.weight
                completed_weight += group_completed_weight

                # Get raw grade for this group (as percentage)
                group_raw_grade = sum(task.grade for task in completed_tasks) / len(completed_tasks)

                # Add weighted contribution from this group
                current_contribution += group_raw_grade * group_completed_weight

        # Return percentage of points earned out of points possible
        return (current_contribution / completed_weight) if completed_weight > 0 else 0

    def getTrueGrade(self) -> float:
        """The true grade or "no work grade" is the grade that you get if you did NO more work past this time."""
        return sum([gg.getTrueContribution() for gg in self.grading_groups])

    def getExpectedGrade(self) -> float:
        """Returns expected grade where expected grade is the EXPECTED grade for every assignment at EXPECTED effort."""
        return sum([gg.getExpectedContribution() for gg in self.grading_groups])

    def getLetterGrade(self, grade: float | None = None) -> str:
        if grade is None:
            grade = self.getGrade()

        for letter_grade, boundary in self.grading_boundaries.items():
            lower_bound, upper_bound = boundary
            if lower_bound / 100 <= grade <= upper_bound / 100:
                return letter_grade
        raise Exception("getLetterGrade failed. Bounds not found for grade.")

    def getTask(self, name) -> Task:
        for gg in self.grading_groups:
            for task in gg.tasks:
                if task.name == name:
                    return task
        raise Exception(f"Task {name} not found")

    def getParent(self, task) -> GradingGroup:
        if isinstance(task, str):
            task = self.getTask(task)
        assert isinstance(task, Task)

        for gg in self.grading_groups:
            for gg_task in gg.tasks:
                if gg_task == task:
                    return gg

        raise Exception(f"Task {task} not found")

    def getMarginalGradePerHour(self, task: Task) -> float:
        if isinstance(task, str):
            task = self.getTask(task)
        assert isinstance(task, Task)

        gg = self.getParent(task)
        return gg.getMarginalGradePerHour(task)

    def getRawUtility(self) -> float:
        # THIS UTILITY FUNCTION IS DOG WATER, DOESN'T WORK RIGHT. TRY TO FIX. https://www.desmos.com/calculator/vpdemyatol
        grade = self.getGrade()
        w = 300
        return sum(
            [
                util * sigmoid((grade - bound[0]) * w)
                for util, bound in zip(self.grade_utils, self.grading_boundaries, strict=False)
            ]
        ) / sum(self.grade_utils.values())

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        """Returns a Rich-formatted string representation of the course."""
        console = Console(record=True)

        # Create list to hold all group elements
        content_elements = []

        # Add each grading group
        for gg in self.grading_groups:
            content_elements.append(Text(str(gg)))
            content_elements.append(Text("\n"))  # Add spacing between groups

        # Create grade summary table
        grade_table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
        grade_table.add_column("Type", style="bold cyan")
        grade_table.add_column("Value", style="green")
        grade_table.add_column("Letter", style="yellow")

        # Calculate grades
        expected_grade = self.getExpectedGrade()
        current_grade = self.getCurrentGrade()
        guaranteed_grade = self.getGrade()
        true_grade = self.getTrueGrade()

        # Add rows to table
        grade_table.add_row(
            "EXPECTED GRADE",
            f"{expected_grade * 100:<6.2f}%",
            f"({self.getLetterGrade(expected_grade)})",
        )
        grade_table.add_row(
            "CURRENT GRADE",
            f"{current_grade * 100:<6.2f}%",
            f"({self.getLetterGrade(current_grade)})",
        )
        grade_table.add_row(
            "MIN WORK GRADE",
            f"{guaranteed_grade * 100:<6.2f}%",
            f"({self.getLetterGrade(guaranteed_grade)})",
        )
        grade_table.add_row(
            "NO WORK GRADE",
            f"{true_grade * 100:<6.2f}%",
            f"({self.getLetterGrade(true_grade)})",
        )

        # Create boundaries table
        boundaries_table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
        boundaries_table.add_column("Grade", style="bold magenta")
        boundaries_table.add_column("Range", style="blue")

        for letter, (lower, upper) in self.grading_boundaries.items():
            boundaries_table.add_row(letter, f"{lower}% - {upper}%")

        # Add grade tables to content
        content_elements.extend(
            [
                Text("\nGrade Summary:", style="bold white"),
                grade_table,
                Text("\nGrade Boundaries:", style="bold white"),
                boundaries_table,
            ]
        )

        # Create panel with all content
        panel = Panel(
            Group(*content_elements),
            title=f"[bold red]COURSE: {self.name}[/bold red]",
            border_style="red",
            padding=(1, 2),
        )

        # Render to string and return
        with console.capture() as capture:
            console.print(panel)
        return capture.get()
