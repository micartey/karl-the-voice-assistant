from dataclasses import dataclass
from typing import Self
import json


@dataclass
class Prompt:
    role: str
    voice: str

    @classmethod
    def load_from_json(cls, role: str) -> Self:
        with open(f"assets/prompts/{role}.json", "r") as file:
            prompt = json.load(file)

            return Prompt(**prompt)
