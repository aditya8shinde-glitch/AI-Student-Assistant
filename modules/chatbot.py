import ollama


MODEL_NAME = "qwen2.5:0.5b"


def generate_response(messages):

    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages
    )

    return response["message"]["content"]