# Fullstack Web Development with Python <!-- omit in toc -->

### [# goit-pythonweb-hw-06](https://github.com/topics/goit-pythonweb-hw-06) <!-- omit in toc -->

<p align="center">
  <img align="center" src="./assets/thumbnail.svg" width="200" title="Project thumbnail" alt="project thumbnail">
</p>

## Database Management with SQLAlchemy & PostgreSQL <!-- omit in toc -->

This project demonstrates the use of **SQLAlchemy ORM for modeling** relational **data in PostgreSQL**, along with **Alembic for schema migrations**, **Faker for generating test data**, and a **Python CLI (via argparse) for performing CRUD operations** on the database.

The app simulates an academic environment with students, teachers, groups, subjects, and grades.

<p align="center">
  <img src="./assets/project-showcase.png" alt="Project showcase image" width="700">
</p>

Main features:

* SQLAlchemy-based data modeling for Students, Teachers, Groups, Subjects, and Grades.
* Alembic integration for database versioning and migrations.
* Faker-powered data seeding with realistic student records and grades.
* A command-line interface for managing database records with create, list, update, and remove actions.
* SQL queries implemented via ORM: top students, average grades, group statistics, and more.

## Table of Contents <!-- omit in toc -->
- [Task Requirements](#task-requirements)
  - [Technical Description](#technical-description)
    - [Technical Steps](#technical-steps)
      - [Step 1 - SQLAlchemy Models](#step-1---sqlalchemy-models)
      - [Step 2 - Alembic Migrations](#step-2---alembic-migrations)
      - [Step 3 - Data Seeding with Faker](#step-3---data-seeding-with-faker)
      - [Step 4 - ORM Queries](#step-4---orm-queries)
    - [Optional Tasks](#optional-tasks)
      - [Part 1 - More Complex Queries](#part-1---more-complex-queries)
      - [Part 2 - CLI for CRUD Operations](#part-2---cli-for-crud-operations)
- [Task Solution](#task-solution)
  - [Solution Description](#solution-description)
  - [Features](#features)
  - [Project Files Structure](#project-files-structure)
  - [Solution Screenshots](#solution-screenshots)
- [Project Setup \& Run Instructions](#project-setup--run-instructions)
  - [Prerequisites](#prerequisites)
  - [Setting Up the Development Environment](#setting-up-the-development-environment)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Choose Setup Method](#2-choose-setup-method)
      - [🐳 Option 1: Using Docker Compose (_Recommended, easiest way to run the app with minimal setup_)](#-option-1-using-docker-compose-recommended-easiest-way-to-run-the-app-with-minimal-setup)
      - [🐳 Option 2: Run with Docker (_Alternative Method_)](#-option-2-run-with-docker-alternative-method)
      - [🐍 Option 3: Local Development (Poetry)](#-option-3-local-development-poetry)
- [License](#license)

## Task Requirements

This project implements a database schema using `PostgreSQL` and `SQLAlchemy`, along with `Alembic` for migrations, `Faker` for data seeding, and a `CLI` interface for CRUD operations.

### Technical Description

Implement database that includes following tables:

* Students table;
* Groups table;
* Teachers table;
* Subjects table with a reference to the teacher who teaches the subject;
* Table, where each student has grades for subjects, along with the date the grade was received.

Use `postgres` database. Run the PostgreSQL database using Docker:

```bash
docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

Replace container name `some-postgres` and password `mysecretpassword` with your custom values to connect to the database.

#### Technical Steps

##### Step 1 - SQLAlchemy Models

Implement SQLAlchemy models for the following tables:

* Students table
* Groups table
* Teachers table
* Subjects  table(with a foreign key to the teacher who teaches the subject)
* Table with Grades (with a foreign key to student and subject, and a timestamp for when the grade was assigned)

##### Step 2 - Alembic Migrations

Use `Alembic` to create database migrations and apply them to your PostgreSQL database.

##### Step 3 - Data Seeding with Faker

Create a script `seed.py` that populates the database with realistic random data:

* ~30-50 students
* 3 groups
* 5-8 subjects
* 3-5 teachers
* Up to 20 grades per student across all subjects

Use **SQLAlchemy** sessions and the **Faker** library for generating data.

##### Step 4 - ORM Queries

Implement the following 10 SQL queries using **SQLAlchemy** ORM:

1. Retrieve the top 5 students with the highest average grade across all subjects.
2. Find the student with the highest average grade in a specific subject.
3. Find the average grade per group for a specific subject.
4. Find the overall average grade across all grades for cohort students.
5. Find which subjects are taught by a specific teacher.
6. Retrieve a list of students in a specific group.
7. Retrieve the grades of students in a specific group for a specific subject.
8. Find the average grade a specific teacher gives across their subjects.
9. List the courses taken by a specific student.
10. List the courses a specific teacher teaches to a specific student.

Use `SQLAlchemy` sessions to perform all queries.
Organize them into a file `my_select.py`, each as a function from `select_1()` to `select_10()`.

#### Optional Tasks

These tasks are optional and not required to pass the assignment.

##### Part 1 - More Complex Queries

1. Find the average grade a specific teacher gives to a specific student.
2. Retrieve grades from the last lesson for students in a specific group and subject.

##### Part 2 - CLI for CRUD Operations

Instead of using `seed.py`, create a **full-featured CLI application** using the `argparse` module to perform **CRUD** operations on all models.

Use the following command structure:

* `--action` (or `-a`) for specifying the action (`create`, `list`, `update`, `remove`)
* `--model` (or `-m`) for specifying the target model (e.g. `Teacher`, `Group`, etc.)

**Commands structure**:

* Create a teacher:
  ```bash
  -action create -m Teacher --name 'Boris Jonson'
  ```
* List all teachers:
  ```bash
  -action list -m Teacher
  ```
* Update a teacher's data with `id=3`:
  ```bash
  -action update -m Teacher --id 3 --name 'Andry Bezos'
  ```

Implement similar commands for all models.

**Examples of commands in terminal**:

* Create a teacher
  ```bash
  py main.py -a create -m Teacher -n 'Boris Jonson'
  ```
* Create a group
  ```bash
  py main.py -a create -m Group -n 'AD-101'
  ```

## Task Solution

### Solution Description

As a solution to the technical requirements, I created an app that simulates an academic environment with students, teachers, groups, subjects, and grades.

The application covers the following steps:

1. **Database Modeling** - Defined models using SQLAlchemy to represent all required entities and their relationships:
    * `Student`
    * `Group`
    * `Teacher`
    * `Subject` (linked to a teacher)
    * `Grade` (linked to student, subject, and date)
2. **Migrations with Alembic** - Set up Alembic to manage database schema changes and apply them to a PostgreSQL instance.
3. **Data Seeding** - Created a `seed.py` script to populate the database with realistic, randomly generated data using the Faker library.
4. **Advanced Queries** - Implemented 10 SQL queries using SQLAlchemy ORM to extract meaningful insights, such as top-performing students, course averages, and teacher-specific statistics.
5. **CLI Interface** - Developed a command-line tool using `argparse` to perform CRUD operations on each model, allowing creation, listing, updating, and deletion of records via terminal commands.

### Features

- ...

### Project Files Structure
```
.
├── compose.yaml                # Docker Compose file
├── Dockerfile                  # Docker image definition
├── .dockerignore               # Files/folders to exclude from Docker context
├── pyproject.toml              # Project dependencies and config (Poetry)
└── src/
    ├── main.py                 # Entry point for the application
    ├── decorators/
    │   └── handle_server_errors.py   # Decorator to catch and handle server errors
    ├── storage/
...
```

### Solution Screenshots

**CRUD operations on each model**:

![CRUD operations on each model](./assets/results/list-all-students.png)

## Project Setup & Run Instructions

This guide will help you set up the environment and run the project.

### Prerequisites

Before you begin, make sure you have the following installed:

* **[Python 3.11.*](https://www.python.org/downloads/)** (tested with Python 3.11.13) — Required to run the application locally (outside Docker, if needed).
* **[Poetry](https://python-poetry.org/)** - To manage dependencies in virtual environment.
* **[Docker](https://www.docker.com/)** — Used to containerize the application in a unified environment using Docker or Docker Compose.
* **[psycopg2-binary](https://pypi.org/project/psycopg2/)** - PostgreSQL database adapter for the Python programming language (on Linux may require installation of additional packages `sudo apt install libpg-dev python3-dev`).
* (*Optional - for local development*) **[Git](https://git-scm.com/downloads)** — To clone [the repository](https://github.com/oleksandr-romashko/goit-pythonweb-hw-03), version control and development.
* (*Optional - for local development*) **[VS Code](https://code.visualstudio.com/download)** or another IDE — Recommended for browsing and editing the project source code and overall development.

### Setting Up the Development Environment

#### 1. Clone the Repository

```bash
git clone https://github.com/oleksandr-romashko/goit-pythonweb-hw-06
cd goit-pythonweb-hw-06
```

or download the ZIP archive from [GitHub Repository](https://github.com/oleksandr-romashko/goit-pythonweb-hw-06) and extract it.

#### 2. Choose Setup Method

You can either run the project in a fully containerized development environment (**_recommended_**) or set it up locally using a virtual environment.

##### 🐳 Option 1: Using Docker Compose (_Recommended, easiest way to run the app with minimal setup_)

> This method runs app using Docker Compose

```bash
docker compose up --build
```

This will:

1. Build the FastAPI application image.
2. Create and run the container with necessary ports.
3. Use a volume for data persistence.

The app will be available at: http://localhost:3000

To stop:

```bash
docker compose down
```

##### 🐳 Option 2: Run with Docker (_Alternative Method_)

> For those who want a bit more control using `docker run`.

1. Build the Docker image:
    ```bash
    docker build -t goit-pythonweb-hw-03 .
    ```
2. (Optional) Create a named volume for persistent data:
    > Only needed once before first run:
    ```bash
    docker volume create storage_data
    ```
3. Run the Docker container:
    ```bash
    docker run -p 3000:3000 \
    -v storage_data:/app/storage/data \
    --rm -ti \
    --name goit-pythonweb-hw-03 \
    goit-pythonweb-hw-03
    ```

    App will be available at: http://localhost:3000

##### 🐍 Option 3: Local Development (Poetry)

> For local development without Docker.

1. Install dependencies:
    ```bash
    poetry install
    ```
2. Run the app:
    ```bash
    poetry run python src/main.py
    ```

    App will be available at: http://localhost:3000


## License

This project is licensed under the [MIT License](./LICENSE).
You are free to use, modify, and distribute this software in accordance with the terms of the license.