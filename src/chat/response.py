import json

from src.config import ee
from src.config import openai, GPT_MODEL

functions = json.loads(
    openai.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        top_p=0,
        messages=[
            {
                "role": "system",
                "content": open("assets/functions/prompt.txt", "r").read(),
            },
            {
                "role": "user",
                "content": open("assets/functions/functions.yml", "r").read(),
            },
        ],
    )
    .choices[0]
    .message.content
)


def generate_response(messages: list[dict[str, str]]) -> str:
    """
    Generate a GPT response with function calling
    :return: text
    """

    message = (
        openai.chat.completions.create(
            model=GPT_MODEL, messages=messages, functions=functions
        )
        .choices[0]
        .message
    )

    function_call = message.function_call

    if function_call:
        name = function_call.name
        arguments = function_call.arguments

        ee.emit(name, arguments)

        messages.append(message)
        messages.append({"role": "function", "name": name, "content": arguments})

    return generate_simple_response(messages)


def generate_simple_response(messages: list[dict[str, str]]) -> str:
    """
    Generate a GPT response without functions
    :return: text
    """

    return (
        openai.chat.completions.create(model=GPT_MODEL, messages=messages)
        .choices[0]
        .message
    ).content
