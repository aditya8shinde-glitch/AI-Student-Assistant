import ollama
import json


# Use a stronger model for quiz generation.
# The smaller model is better for fast chat,
# while this model is better at structured questions.
MODEL_NAME = "llama3.2:3b"


def generate_quiz(topic, difficulty, number_of_questions):

    prompt = f"""
You are an expert college-level quiz creator.

Create exactly {number_of_questions} high-quality multiple-choice
questions about ONLY this topic:

TOPIC: {topic}

DIFFICULTY: {difficulty}

Return ONLY valid JSON using exactly this structure:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Exactly one of the four options"
        }}
    ]
}}

STRICT RULES:

1. Every question MUST be directly related to {topic}.
2. Do NOT create questions about unrelated subjects.
3. Every question must test actual knowledge.
4. Do NOT make the correct answer obvious from the wording.
5. Do NOT make the answer a copy of the question.
6. All four options must be plausible answers.
7. Exactly ONE option must be correct.
8. The "answer" value MUST exactly match one of the four options.
9. Do NOT always put the correct answer in the first position.
10. Distribute correct answers across A, B, C and D.
11. Do not repeat questions.
12. Do not repeat the same four options.
13. Avoid vague or ambiguous questions.
14. Do not create questions that depend on information outside the topic.
15. Keep each question concise.
16. Do not include explanations.
17. Do not include Markdown.
18. Return ONLY JSON.

Before returning the JSON, internally check every question:

- Is it about {topic}?
- Are all four options related to the question?
- Is exactly one option correct?
- Does the answer exactly match an option?
- Is the correct answer position varied?
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format="json"
    )

    content = response["message"]["content"].strip()

    if not content:
        raise ValueError(
            "The AI returned an empty response."
        )

    data = json.loads(content)

    # ---------------------------------------------------------
    # Accept the expected JSON structure
    # ---------------------------------------------------------

    if isinstance(data, dict) and "questions" in data:

        quiz = data["questions"]

    elif isinstance(data, list):

        quiz = data

    else:

        raise ValueError(
            "AI returned an invalid quiz format."
        )

    # ---------------------------------------------------------
    # Check question count
    # ---------------------------------------------------------

    if len(quiz) != number_of_questions:

        raise ValueError(
            f"AI generated {len(quiz)} questions "
            f"instead of {number_of_questions}."
        )

    # ---------------------------------------------------------
    # Validate every question
    # ---------------------------------------------------------

    for index, question in enumerate(quiz):

        question_number = index + 1

        if not isinstance(question, dict):

            raise ValueError(
                f"Question {question_number} is invalid."
            )

        if "question" not in question:

            raise ValueError(
                f"Question {question_number} is missing text."
            )

        if "options" not in question:

            raise ValueError(
                f"Question {question_number} is missing options."
            )

        if "answer" not in question:

            raise ValueError(
                f"Question {question_number} is missing the answer."
            )

        # Exactly four options
        if len(question["options"]) != 4:

            raise ValueError(
                f"Question {question_number} must have "
                f"exactly 4 options."
            )

        # Make sure options are actually different
        options = [
            str(option).strip().lower()
            for option in question["options"]
        ]

        if len(set(options)) != 4:

            raise ValueError(
                f"Question {question_number} contains "
                f"duplicate options."
            )

        # Correct answer must match an option
        if question["answer"] not in question["options"]:

            raise ValueError(
                f"Question {question_number} has an answer "
                f"that does not match its options."
            )

    # ---------------------------------------------------------
    # Remove duplicate questions
    # ---------------------------------------------------------

    question_texts = [
        question["question"].strip().lower()
        for question in quiz
    ]

    if len(set(question_texts)) != len(question_texts):

        raise ValueError(
            "The AI generated duplicate questions."
        )

    return quiz