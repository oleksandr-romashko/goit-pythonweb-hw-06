"""
Script to seed the database with demo educational data.

This script generates realistic mock data for students, groups, subjects, tasks, and grades.
It ensures each student is assigned to a group and receives a set of tasks across subjects,
with grades generated based on configurable rules and realistic randomness.

Arguments:
    --dry-run       Simulates data generation without saving anything (no database writes).
    --seed <int>    Optional seed value for deterministic output (useful for testing or consistency).

Example usage:
    poetry run python app.py --dry-run --seed 42
"""

import argparse
import sys
from pathlib import Path
import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

# Add src directory to sys.path for imports
sys.path.append(str(Path(__file__).resolve().parents[1]))

from database.session import session_scope
from database.models import Grade, Group, PersonalData, Student, Subject, Teacher

faker_locales: list[str] = ["cs_CZ", "de_DE", "pl_PL", "uk_UA"]

fake = Faker()


def assign_students_to_groups(students: list[Student], groups: list[Group]) -> None:
    """Assign students randomly to the given groups."""
    # Students without a group are not allowed for database seeding
    if not groups:
        raise ValueError("Groups list should contain at least one group")
    for student in students:
        student.group = random.choice(groups)


def assign_subjects_to_groups(
    groups: list[Group],
    subjects: list[Subject],
    subjects_per_group_min: int = 1,
    subjects_per_group_max: int = 1,
) -> None:
    """Assign random subjects to each group."""
    if not groups:
        raise ValueError("Groups list cannot be empty")
    if not subjects:
        raise ValueError("Subjects list cannot be empty")
    if subjects_per_group_max < subjects_per_group_min:
        raise ValueError("Max subjects per group must be >= min")

    for group in groups:
        subjects_per_group = random.randint(
            subjects_per_group_min, subjects_per_group_max
        )
        group.subjects = random.sample(subjects, min(subjects_per_group, len(subjects)))


def assign_teachers_to_subjects(
    teachers: list[Teacher], subjects: list[Subject]
) -> None:
    """Assign teachers to subjects, ensuring each subject has at least one teacher."""
    if len(subjects) == 0:
        raise ValueError("Subjects list should contain at least one subject")

    if len(teachers) == 0:
        raise ValueError("Teachers list should contain at least one teacher")

    shuffled_subjects = subjects[:]
    random.shuffle(shuffled_subjects)

    if len(teachers) <= len(subjects):
        # Case 1: Equal or fewer teachers than subjects

        # Step 1: Ensure each teacher gets one subject
        for teacher in teachers:
            subject = shuffled_subjects.pop(0)
            subject.teacher = teacher

        # Step 2: Other subjects will be assigned randomly among all teachers
        for subject in shuffled_subjects:
            teacher = random.choice(teachers)
            subject.teacher = teacher
    else:
        # Case 2: More teachers than subjects

        temp_teachers = teachers[:]
        # Step 1: Ensure each subject will have it's own unique teacher
        for subject in shuffled_subjects:
            teacher = temp_teachers.pop(0)
            subject.teacher = teacher

        # Step 2: Assign remaining teachers to random subjects
        for teacher in temp_teachers:
            random.choice(subjects).teacher = teacher


def generate_grades(
    students: list[Student],
    max_grades_per_student: int,
    grade_min=60,
    grade_max=100,
) -> list[Grade]:
    """Generate a list of Grade objects for the given students."""
    grades = []
    for student in students:
        group = student.group
        if not group or not group.subjects:
            continue
        tasks_per_group = max_grades_per_student // len(group.subjects)
        for subject in group.subjects:
            for task_number in range(random.randint(0, tasks_per_group)):
                grade_score = random.randint(grade_min, grade_max)
                grade = Grade(
                    task_number=task_number + 1,  # to start with task no. 1
                    grade=grade_score,
                    student=student,
                    group=group,
                    subject=subject,
                )
                grades.append(grade)
    return grades


def generate_groups(min_: int = 1, max_: int = 1) -> list[Group]:
    """Generate a list of Group instances within the specified range."""
    if max_ < min_:
        raise ValueError(
            "Max number of groups to generate can't be less than min value"
        )

    number_of_groups = random.randint(min_, max_)

    groups = []
    for i in range(number_of_groups):
        group = Group(
            name=f"G{i+1}",
            start_date=fake.date_this_year(before_today=True, after_today=False),
        )
        groups.append(group)

    return groups


def generate_personal_data(n: int = 1) -> list[PersonalData]:
    """Generate a list of PersonalData with localized and gender-specific names."""
    if n < 1:
        raise ValueError("Number of entities should be a positive integer number")

    faker_locales_cache = {locale: Faker(locale) for locale in faker_locales}

    personal_data_list = []
    for _ in range(n):
        # Randomly choose one of locales
        locale = random.choice(faker_locales)
        faker_localized = faker_locales_cache[locale]

        # Some locales may require gender-relevant names
        gender = random.choice(["male", "female"])
        if gender == "male":
            first_name = faker_localized.first_name_male()
            last_name = faker_localized.last_name_male()
        else:
            first_name = faker_localized.first_name_female()
            last_name = faker_localized.last_name_female()

        personal_data_item = PersonalData(first_name=first_name, last_name=last_name)
        personal_data_list.append(personal_data_item)

    return personal_data_list


def generate_students(min_: int = 1, max_: int = 1) -> list[Student]:
    """Generate a random number of students (without group assignment)."""
    if max_ < min_:
        raise ValueError(
            "Max number of students to generate can't be less than min value"
        )

    number_of_students = random.randint(min_, max_)

    personal_data_list = generate_personal_data(number_of_students)

    return [Student(personal_data=data) for data in personal_data_list]


def generate_subjects(number_of_subjects: int = 1) -> list[Subject]:
    """Generate a list of unique Subject objects with random titles."""

    subject_titles = {
        "Mathematics",
        "Physics",
        "Chemistry",
        "Biology",
        "History",
        "Geography",
        "English",
        "Computer Science",
        "Literature",
        "Philosophy",
        "Economics",
        "Sociology",
        "Psychology",
        "Art",
        "Music",
        "Physical Education",
        "Health Education",
        "Environmental Science",
        "Political Science",
        "Statistics",
        "Business Studies",
        "Law",
        "Astronomy",
        "Engineering Basics",
        "Foreign Language (English)",
        "Foreign Language (French)",
        "Foreign Language (German)",
    }

    if number_of_subjects > len(subject_titles):
        raise ValueError(
            f"Cannot generate {number_of_subjects} unique subjects. "
            f"Only {len(subject_titles)} unique titles available."
        )

    # Take only n subjects from the list of potential subjects
    selected_subject_titles = random.sample(list(subject_titles), number_of_subjects)

    return [Subject(title=name) for name in selected_subject_titles]


def generate_teachers(min_: int = 1, max_: int = 1) -> list[Teacher]:
    """Generate a random number of teachers with personal data."""
    if max_ < min_:
        raise ValueError(
            "Max number of teachers to generate can't be less than min value"
        )

    number_of_teachers = random.randint(min_, max_)
    personal_data_list = generate_personal_data(number_of_teachers)

    return [Teacher(personal_data=data) for data in personal_data_list]


def print_generated_data_stats(
    students: list[Student],
    groups: list[Group],
    subjects: list[Subject],
    teachers: list[Teacher],
    grades: list[Grade],
) -> None:
    teachers_per_group = []
    for group in groups:
        unique_teachers = {subject.teacher for subject in group.subjects}
        teachers_per_group.append(len(unique_teachers))
    average_grades = round(len(grades) / len(students), 2) if students else 0.0

    print("📝 Summary of generated data to seed:")
    print(f"    Generated students:        {len(students)}")
    print(f"    Generated subjects:        {len(subjects)}")
    print(f"    Generated teachers:        {len(teachers)}")
    print(f"    Generated groups:          {len(groups)}")
    print(f"        students per group:    {[len(group.students) for group in groups]}")
    print(f"        subjects per group:    {[len(group.subjects) for group in groups]}")
    print(f"        teachers per group:    {teachers_per_group}")
    print(f"    Generated grades:          {len(grades)}")
    print(f"       avg grades per student: {average_grades}")


def seed_db(dry_run: bool = False) -> None:
    """
    Populate the database with sample data.

    This function uses a SQLAlchemy session to insert test data into the database.
    It ensures that any error during insertion is handled properly by rolling back
    the transaction and logging the error.
    """
    print("[INFO] Seeding database with data...")

    # Generate entities

    groups = generate_groups(min_=3, max_=3)
    students = generate_students(min_=30, max_=50)
    assign_students_to_groups(students=students, groups=groups)

    teachers = generate_teachers(min_=3, max_=5)
    subjects = generate_subjects(number_of_subjects=8)
    assign_teachers_to_subjects(teachers=teachers, subjects=subjects)

    assign_subjects_to_groups(
        groups, subjects, subjects_per_group_min=5, subjects_per_group_max=8
    )

    grades = generate_grades(
        students, max_grades_per_student=20, grade_min=60, grade_max=100
    )

    print_generated_data_stats(students, groups, subjects, teachers, grades)

    if not dry_run:
        try:
            print("[INFO] Writing generated data to database...")
            with session_scope() as session:
                session.add_all(teachers)
                session.add_all(subjects)
                session.add_all(groups)
                session.add_all(students)
                session.add_all(grades)
        except SQLAlchemyError as e:
            print(f"❌ An error occurred while seeding the database: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        else:
            print("✅ Database seeding completed successfully.")


def parse_args():
    parser = argparse.ArgumentParser(description="Seed database with generated data.")

    # --dry-run flag (no arguments, just True if present)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the script without saving or modifying any data.",
    )

    # --seed option (expects a value, e.g. --seed 123)
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Set a seed for the random number generator for reproducibility.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Apply seed if provided
    if args.seed is not None:
        seed = args.seed
        random.seed(seed)
        Faker.seed(seed)
        print(f"[INFO] Random seed is set to '{seed}'.")
    else:
        seed = 40
        random.seed(seed)
        Faker.seed(seed)
        print(
            "[INFO] Random seed was not set using --seed flag, so default value is used to persist randomness."
        )

    if args.dry_run:
        print("[INFO] Running in dry-run mode. No changes will be saved.")

    seed_db(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
