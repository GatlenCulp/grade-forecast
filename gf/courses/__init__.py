"""Courses package containing course definitions and utilities.

This package provides access to various course configurations and their associated
grading structures. Each course module defines a Course object with its specific
grading groups, tasks, and policies.
"""

from .prog_fund import prog_fund

__all__ = ["prog_fund"]
