import ollama
import numpy as np
import json
import re

from pypdf import PdfReader


# ============================================================
# MODELS
# ============================================================

CHAT_MODEL = "llama3.2:3b"
EMBEDDING_MODEL = "nomic-embed-text"


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text.append(page_text)

    return "\n\n".join(text)


# ============================================================
# TEXT CHUNKING
# ============================================================

def create_chunks(
    text,
    chunk_size=1200,
    overlap=200
):

    text = text.strip()

    if not text:

        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(
                chunk.strip()
            )

        start += chunk_size - overlap

    return chunks


# ============================================================
# CREATE EMBEDDING
# ============================================================

def create_embedding(text):

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return np.array(
        response["embeddings"][0],
        dtype=np.float32
    )


# ============================================================
# CREATE NOTES INDEX
# ============================================================

def create_notes_index(notes_text):

    chunks = create_chunks(
        notes_text
    )

    if not chunks:

        return []

    index = []

    for number, chunk in enumerate(
        chunks,
        start=1
    ):

        embedding = create_embedding(
            chunk
        )

        index.append(
            {
                "id": number,
                "text": chunk,
                "embedding": embedding
            }
        )

    return index


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity(
    vector_a,
    vector_b
):

    denominator = (
        np.linalg.norm(vector_a)
        *
        np.linalg.norm(vector_b)
    )

    if denominator == 0:

        return 0.0

    return float(
        np.dot(
            vector_a,
            vector_b
        )
        /
        denominator
    )


# ============================================================
# RETRIEVE RELEVANT CHUNKS
# ============================================================

def retrieve_relevant_chunks(
    notes_index,
    question,
    number_of_chunks=4
):

    if not notes_index:

        return []

    question_embedding = create_embedding(
        question
    )

    scored_chunks = []

    for item in notes_index:

        score = cosine_similarity(
            question_embedding,
            item["embedding"]
        )

        scored_chunks.append(
            {
                "id": item["id"],
                "text": item["text"],
                "score": score
            }
        )

    scored_chunks.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return scored_chunks[
        :number_of_chunks
    ]


# ============================================================
# ASK QUESTION USING RAG
# ============================================================

def ask_about_notes(
    notes_text,
    question,
    notes_index=None
):

    if notes_index is None:

        notes_index = create_notes_index(
            notes_text
        )

    relevant_chunks = (
        retrieve_relevant_chunks(
            notes_index,
            question,
            number_of_chunks=4
        )
    )

    if not relevant_chunks:

        return {
            "answer": (
                "I couldn't find enough information "
                "in the uploaded notes."
            ),
            "sources": []
        }

    context = "\n\n---\n\n".join(
        [
            item["text"]
            for item in relevant_chunks
        ]
    )

    prompt = f"""
You are an AI study assistant.

Answer the student's question using ONLY
the relevant information retrieved from
their uploaded study material.

RELEVANT NOTES:
----------------
{context}
----------------

STUDENT QUESTION:
{question}

Rules:

1. Use the notes as the primary source.

2. Do not invent information.

3. Explain the answer clearly.

4. Keep the answer reasonably concise.

5. Use examples from the notes when useful.

6. If the answer cannot be supported by
   the retrieved notes, say:

"I couldn't find this information
in the uploaded notes."

Do not pretend unsupported information
came from the notes.
"""

    response = ollama.chat(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = (
        response["message"]["content"]
        .strip()
    )

    sources = []

    for item in relevant_chunks:

        sources.append(
            {
                "id": item["id"],
                "text": item["text"],
                "score": item["score"]
            }
        )

    return {
        "answer": answer,
        "sources": sources
    }


# ============================================================
# SUMMARIZE NOTES
# ============================================================

def summarize_notes(notes_text):

    context = notes_text[:12000]

    prompt = f"""
You are a college study assistant.

Create a useful revision summary of
the uploaded study material.

UPLOADED STUDY MATERIAL:
------------------------
{context}
------------------------

Create:

1. Short overview
2. Important concepts
3. Important definitions
4. Key points
5. Important terms

Rules:

- Use information supported by the notes.
- Do not invent facts.
- Keep the summary organized.
- Make it useful for exam revision.
- Keep it reasonably concise.
"""

    response = ollama.chat(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return (
        response["message"]["content"]
        .strip()
    )


# ============================================================
# GENERATE QUIZ FROM NOTES
# ============================================================

def generate_quiz_from_notes(
    notes_index,
    number_of_questions=5,
    difficulty="Medium"
):

    if not notes_index:

        return []

    total_chunks = len(
        notes_index
    )

    if total_chunks <= 8:

        selected_items = notes_index

    else:

        step = max(
            1,
            total_chunks // 8
        )

        selected_items = (
            notes_index[::step][:8]
        )

    context = "\n\n---\n\n".join(
        [
            item["text"]
            for item in selected_items
        ]
    )

    prompt = f"""
You are an expert college quiz generator.

Create exactly {number_of_questions}
multiple-choice questions from the
study material below.

DIFFICULTY:
{difficulty}

STUDY MATERIAL:
----------------
{context}
----------------

STRICT RULES:

1. Every question must be answerable
   from the provided study material.

2. Do NOT use outside knowledge.

3. Create exactly {number_of_questions}
   questions.

4. Every question must have exactly
   FOUR different answer options.

5. Only ONE option must be correct.

6. The other three options must be
   plausible but clearly incorrect.

7. Do not make all correct answers
   the same option.

8. Vary the position of the correct answer.

9. Do not repeat questions.

10. Do not create questions where
    multiple options could reasonably
    be correct.

11. Questions should test understanding,
    not just exact wording.

12. Keep questions suitable for a
    college student.

RETURN ONLY VALID JSON.

Use exactly this structure:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "The exact correct option"
  }}
]

IMPORTANT:

The "answer" value MUST exactly match
one of the four strings inside "options".
"""

    response = ollama.chat(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw_response = (
        response["message"]["content"]
        .strip()
    )

    try:

        return json.loads(
            raw_response
        )

    except json.JSONDecodeError:

        match = re.search(
            r"\[.*\]",
            raw_response,
            re.DOTALL
        )

        if match:

            try:

                return json.loads(
                    match.group(0)
                )

            except json.JSONDecodeError:

                return []

        return []


# ============================================================
# VALIDATE GENERATED QUIZ
# ============================================================

def validate_quiz(
    quiz,
    expected_questions
):

    if not isinstance(
        quiz,
        list
    ):

        return False

    if len(quiz) != expected_questions:

        return False

    for question in quiz:

        if not isinstance(
            question,
            dict
        ):

            return False

        if (
            "question"
            not in question
            or "options"
            not in question
            or "answer"
            not in question
        ):

            return False

        options = question["options"]

        answer = question["answer"]

        if len(options) != 4:

            return False

        if len(set(options)) != 4:

            return False

        if answer not in options:

            return False

    return True