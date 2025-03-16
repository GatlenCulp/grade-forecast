# Grade Forecast

![Uses the Cookiecutter Data Science project template, GOTem style](https://img.shields.io/badge/GOTem-Project%20Instance-328F97?logo=cookiecutter)

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

<!-- [![tests](https://github.com/GatlenCulp/grade-forecast/actions/workflows/tests.yml/badge.svg)](https://github.com/GatlenCulp/grade-forecast/actions/workflows/tests.yml) -->

<!-- ![GitHub stars](https://img.shields.io/github/stars/GatlenCulp/grade-forecast?style=social) -->

> [!NOTE]
> This project was created using [Gatlen's Opinionated Template (GOTem)](https://github.com/GatlenCulp/gatlens-opinionated-template), a cutting-edge project template for power users and researchers.

<div align="center">
  <a href="https://github.com//grade-forecast">
    <!-- Please provide path to your logo here -->
    <img src="https://picsum.photos/id/237/200/300" alt="Logo" style="max-width: 250px;"/>
  </a>
  <br/>
  <b>Grade Forecast</b>
</div>
<br>

> **[?]**
> Provide a brief description of your project here. What does it do? Why is it useful?
> **\[View the full documentation here\](https://Gatlen Culp.github.io/grade-forecast) ➡️**

______________________________________________________________________

## 00 Table of Contents

- [Grade Forecast](#grade-forecast)
  - [00 Table of Contents](#00-table-of-contents)
  - [01 About](#01-about)
  - [02 Getting Started](#02-getting-started)
    - [02.01 Prerequisites](#0201-prerequisites)
    - [02.02 Installation](#0202-installation)
  - [03 Usage](#03-usage)
  - [04 Project Structure](#04-project-structure)
  - [05 Contributing](#05-contributing)
  - [06 License](#06-license)

______________________________________________________________________

## 01 About

> **[?]**
> Provide detailed information about your project here.
>
> - What problem does it solve?
> - What makes it unique?
> - What are its key features?
> - Who is it for?

<details>
<summary>📸 Screenshots</summary>
<br>

> **[?]**
> Please provide your screenshots here.

|                                    Home Page                                    |                                    Login Page                                    |
| :-----------------------------------------------------------------------------: | :------------------------------------------------------------------------------: |
| <img src="https://picsum.photos/id/237/200/300" title="Home Page" width="100%"> | <img src="https://picsum.photos/id/237/200/300" title="Login Page" width="100%"> |

</details>

______________________________________________________________________

## 02 Getting Started

### 02.01 Prerequisites

> **[?]**
> List all dependencies and requirements needed before installing the project:
>
> ```bash
> # Example
> python >= 3.8
> pip >= 21.0
> ```

### 02.02 Installation

> **[?]**
> Provide step-by-step installation instructions:
>
> **01. Clone the repository**
>
> ```bash
> git clone https://github.com/GatlenCulp/grade-forecast.git
> cd grade-forecast
> ```
>
> **02. Install dependencies**
>
> ```bash
> pip install -e .
> ```

______________________________________________________________________

## 03 Usage

> **[?]**
> Provide basic usage examples with code snippets:
>
> ```python
> from gf import example
>
> # Initialize
> example.start()
>
> # Run a basic operation
> result = example.process("data")
> print(result)
> ```

______________________________________________________________________

## 04 Project Structure

This project follows the structure of [Gatlen's Opinionated Template (GOTem)](https://github.com/GatlenCulp/gatlens-opinionated-template):

```
📁 .
├── 📁 data               <- Data directories for various stages
├── 📚 docs               <- Documentation
├── 📋 logs               <- Log files
├── 📁 notebooks          <- Jupyter notebooks
├── 🗑️ out                <- Output files, models, etc.
└── 🚰 gf  <- Source code
    ├── ⚙️ config.py      <- Configuration settings
    ├── 🐍 dataset.py     <- Data processing
    ├── 🐍 features.py    <- Feature engineering
    ├── 📁 modeling       <- Model training and prediction
    └── 🐍 plots.py       <- Visualization code
```

For a more detailed explanation of the project structure, see the [CONTRIBUTING.md](docs/CONTRIBUTING.md) file.

______________________________________________________________________

## 05 Contributing

We welcome contributions to this project! Please see our [contribution guidelines](docs/CONTRIBUTING.md) for detailed information on how to:

- Set up your development environment
- Submit issues and feature requests
- Create pull requests
- Get support

______________________________________________________________________

## 06 License

This project is licensed under the MIT - see the [LICENSE](LICENSE) file for details.

A tool for forecasting and tracking your university grades to adjust your priorities.

## Installation

Clone the repository and install the package:

```bash
git clone https://github.com/yourusername/grade-forecast.git
cd grade-forecast
pip install -e .
```

## Usage

Grade Forecast provides both an interactive CLI and direct command-line commands.

### Interactive Mode

To start the interactive CLI:

```bash
grade-forecast run
```

### Command-Line Commands

#### List all courses

```bash
grade-forecast list
```

This will display all available courses with their aliases.

#### Show a summary of all courses

```bash
grade-forecast summary
```

#### Display information for a specific course

You can use the course name, alias, or index:

```bash
grade-forecast course <course_name>
grade-forecast course <alias>
grade-forecast course <index>
```

With detailed information:

```bash
grade-forecast course <course_name> --details
```

If you run the command without specifying a course, it will display all available courses with their aliases:

```bash
grade-forecast course
```

#### List all tasks in a course

```bash
grade-forecast tasks <course_name>
grade-forecast tasks <alias>
```

If you run the command without specifying a course, it will display all available courses with their aliases:

```bash
grade-forecast tasks
```

#### Analyze a specific task

```bash
grade-forecast task <course_name> <task_name>
grade-forecast task <alias> <task_index>
```

If you run the command without specifying a task, it will display all available tasks in the course:

```bash
grade-forecast task <course_name>
```

#### Update a task's grade

```bash
grade-forecast update <course_name> <task_name> <grade>
grade-forecast update <alias> <task_index> <grade>
```

If you run the command without specifying a grade, it will prompt you to enter one:

```bash
grade-forecast update <course_name> <task_name>
```

Example:

```bash
grade-forecast update compsys "Homework #1" 95
grade-forecast update cs 1 95  # Using alias and task index
```

#### Compare multiple courses

```bash
grade-forecast compare <course1> <course2> ...
grade-forecast compare <alias1> <alias2> ...
```

If you run the command without specifying any courses, it will display all available courses with their aliases:

```bash
grade-forecast compare
```

Example:

```bash
grade-forecast compare compsys linalg
grade-forecast compare cs la  # Using aliases
```

## Features

- Track and forecast your grades across multiple courses
- Analyze the impact of individual assignments on your final grade
- Visualize grade trends and projections
- Prioritize tasks based on their impact on your final grade
- Compare performance across different courses

## License

MIT
