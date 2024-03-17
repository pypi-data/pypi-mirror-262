import os
import logging
from openai import OpenAI
from .utils import load_env
from ._errors import GaidmeError
from .utils import _parse_command_from_response
from .schema import get_command_fnc, get_command_system_prompt

_logger = logging.getLogger(__name__)

def get_command(user_prompt: str) -> str:
    client = OpenAI()
    _logger.debug("running get_command")
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_API_MODEL"),
        messages=[
            {"role": "system", "content": get_command_system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        tools=[get_command_fnc],
        tool_choice={"type": "function", "function": {
            "name": get_command_fnc['function']['name']}}
    )
    command = _parse_command_from_response(response)

    return command

def get_reflection(user_prompt: str, system_prompt: str) -> str:
    client = OpenAI()
    _logger.debug("running get_reflection")
    _logger.debug(system_prompt)
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_API_MODEL"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        tools=[get_command_fnc],
        tool_choice={"type": "function", "function": {
            "name": get_command_fnc['function']['name']}}
    )
    command = _parse_command_from_response(response)

    return command


def moderation(prompt: str) -> None:
    client = OpenAI()
    mod_response = client.moderations.create(input=prompt)
    if mod_response.results[0].flagged is True:
        raise GaidmeError("This message has been flagged as harmful by OpenAI")
