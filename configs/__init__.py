"""Courses package containing course definitions and utilities.

This package provides access to various course configurations and their associated
grading structures. Each course module defines a Course object with its specific
grading groups, tasks, and policies.
"""

from .airr import airr
from .complexity import complexity
from .compsys import compsys
from .linalg import linalg

configs = [airr, complexity, compsys, linalg]
