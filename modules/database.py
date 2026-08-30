import sqlite3
from datetime import datetime


DATABASE_NAME = "data/student_assistant.db"


def get_connection():

    return sqlite3.connect(DATABASE_NAME)


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage REAL NOT NULL,
            completed_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_quiz_result(
    topic,
    difficulty,
    score,
    total_questions
):

    percentage = (
        score / total_questions
    ) * 100

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO quiz_results
        (
            topic,
            difficulty,
            score,
            total_questions,
            percentage,
            completed_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            topic,
            difficulty,
            score,
            total_questions,
            percentage,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    connection.commit()
    connection.close()


def get_quiz_results():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            topic,
            difficulty,
            score,
            total_questions,
            percentage,
            completed_at
        FROM quiz_results
        ORDER BY id DESC
        """
    )

    results = cursor.fetchall()

    connection.close()

    return results