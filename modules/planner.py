import ollama


MODEL_NAME = "llama3.2:3b"


def generate_study_plan(
    subjects,
    exam_date,
    daily_hours,
    study_days,
    priorities
):

    subject_text = "\n".join(
        [
            f"- {subject}: {priorities.get(subject, 'Medium')} priority"
            for subject in subjects
        ]
    )

    prompt = f"""
You are a practical study-planning assistant for a college student.

Create a realistic study plan using the information below.

SUBJECTS:
{subject_text}

EXAM DATE:
{exam_date}

AVAILABLE STUDY HOURS PER DAY:
{daily_hours}

AVAILABLE STUDY DAYS:
{study_days}

Create a clear and realistic plan.

Requirements:

1. Prioritize high-priority subjects.
2. Do not overload one day.
3. Include revision sessions.
4. Include practice/question-solving sessions.
5. Include short breaks.
6. Keep the plan practical for a college student.
7. Clearly divide the plan by day.
8. Mention which subject should be studied each day.
9. Mention approximate study time.
10. Keep the response concise and easy to follow.

Use this format:

STUDY PLAN

Day 1
- Subject:
- Topic:
- Study time:
- Activity:

Day 2
- Subject:
- Topic:
- Study time:
- Activity:

Continue for the available study days.

FINAL REVISION
- Give a short final revision strategy.

IMPORTANT:
Do not invent specific exam topics that were not provided.
If topics are not available, focus on subjects and general revision.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()

