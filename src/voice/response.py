from src.config import openai


def generate_response(messages: list[dict[str, str]]) -> str:
    """
    Generate a GPT response
    :return: text
    """

    return (
        openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        .choices[0]
        .message
    ).content
