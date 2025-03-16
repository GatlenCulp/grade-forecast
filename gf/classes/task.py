def is_proper_fraction(x):
    return all((isinstance(x, (float, int)), x >= 0, x <= 1))


class Task:
    """base_grade is the grade I could get without trying very much.
    pst = "predicted something time"?
    """

    def __init__(
        self,
        name: str,
        grade: float | None = None,
        base_grade: float = 0,
        expected_grade: float | None = None,
        pst: float | None = None,
    ):
        assert isinstance(name, str)
        if grade is not None:
            assert is_proper_fraction(grade)

        self.name = name
        self.grade = grade
        self.base_grade = base_grade
        self.pst = pst

        # if expected_grade == None:
        #     expected_grade = base_grade
        self.expected_grade = expected_grade

    def get_marginal_grade_per_hour(self) -> float:
        """MGPH = dG/dt = d/dt ((max_grade - base_grade)/(pst)*t + base_grade) = (max_grade - base_grade)/pst = (1-base_grade)/pst"""
        if self.pst is None:
            raise Exception("pst must be defined before using MGPH")
        if self.pst == 0:
            raise ZeroDivisionError("self.pst cannot be 0")

        return (1 - self.base_grade) / self.pst

    def get_grade(self) -> float:
        assert self.grade
        return self.grade

    def set_grade(self, grade) -> None:
        assert is_proper_fraction(grade)
        self.grade = grade

    def get_effective_grade(self) -> float:
        return self.grade if self.grade is not None else self.base_grade

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
