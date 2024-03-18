from copy import deepcopy
from enum import Enum

import instructor
import litellm
import tiktoken
from litellm import completion
from openai import OpenAI
from termcolor import colored

from .message import assistant_message
from .utils import retry_attempts

litellm.drop_params = True


class ModelName(str, Enum):
    GPT_3 = "gpt-3.5-turbo"
    GPT_4 = "gpt-4-turbo-preview"
    GEMINI = "gemini/gemini-pro"
    CLAUDE2 = "claude-2.1"
    CLAUDE3 = "claude-3-haiku-20240307"
    MISTRAL = "anyscale/mistralai/Mistral-7B-Instruct-v0.1"
    MIXTRAL = "anyscale/mistralai/Mixtral-8x7B-Instruct-v0.1"


GPT_MODEL = ModelName.GPT_3
GEMINI_MODEL = ModelName.GEMINI


def oai_response(response) -> str:
    try:
        return response.choices[0].message.content
    except Exception:
        return response


def ask_litellm(
    messages: list[dict[str, str]],
    model: str = GEMINI_MODEL,
    json_mode: bool | None = None,
) -> tuple:
    try:
        if json_mode is None and "json" in messages[-1]["content"].lower():
            response_format = {"type": "json_object"}
        else:
            response_format = None
        # response_format = {
        #     "type": (
        #         "json_object"
        #         if json_mode is None and "json" in messages[-1]["content"].lower()
        #         else "text"
        #     )
        # }
        answer = oai_response(
            completion(
                messages=deepcopy(messages),
                model=model,
                response_format=response_format,
            )
        )
        messages.append(assistant_message(content=answer))
        return answer, messages
    except Exception as e:
        print(colored(f"\n\n{model} ERROR: {e}\n\n", "red"))
        return None, messages


def count_gpt_tokens(text: str, model: str = GPT_MODEL) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def ask_oai(
    messages: list[dict[str, str]],
    model: str = GPT_MODEL,
    response_model=None,
    temperature: float = 0.3,
    max_tokens: int | None = None,
    patch_mode=instructor.Mode.TOOLS,
    attempts: int = 1,
    api_key: str | None = None,
    base_url: str | None = None,
) -> tuple:
    """Ask OpenAI to generate a response to the given messages."""
    # print(f"\n\nMESSAGES: {messages}\n\n")
    gpt = instructor.patch(OpenAI(api_key=api_key, base_url=base_url), mode=patch_mode)
    try:
        answer = gpt.chat.completions.create(
            messages=deepcopy(messages),
            model=model,
            response_model=response_model,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=retry_attempts(attempts=attempts),
        )
    except Exception as e:
        print(colored(f"\n\n{model} ERROR: {e}\n\n", "red"))
        return None, messages
    if not response_model:
        answer = oai_response(answer)
        messages.append(assistant_message(content=answer))
        return answer, messages
    messages.append(assistant_message(content=answer.model_dump_json()))
    return answer, messages
