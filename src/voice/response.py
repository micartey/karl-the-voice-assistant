import json

from src.config import openai
from src.config import ee


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
    Generate a GPT response
    :return: text
    """

    message = (
        openai.chat.completions.create(
            model="gpt-4o-mini", messages=messages, functions=functions
        )
        .choices[0]
        .message
    )

    function_call = message.function_call

    if function_call:
        name = function_call.name
        arguments = function_call.arguments  # json.loads(arguments)["minutes"]

        ee.emit(name, arguments)

        messages.append({"role": "assistant", "content": "Execute function"})
        messages.append(
            {
                "role": "function",
                "name": name,
                "content": "Successfully executed function!",
            }
        )

    return (
        openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
        .choices[0]
        .message.content
    )
