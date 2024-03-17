from typing import Any, Optional

from ..action import Action, ActionSpec
from ..executor import Executor
from ..playbook import Playbook


class ListAppendAction(Action):
    def __init__(self) -> None:
        super().__init__()
        self.spec = ActionSpec.from_dict({
            "name": "list.append",
            "description": "Add an element to the end of the list."
        })

    def perform(
        self,
        *args,
        executor: Optional[Executor] = None,
        playbook: Optional[Playbook] = None,
        **kwargs
    ) -> Any:
        if executor is None:
            raise ValueError("executor is None")
        if len(args) != 2:
            raise ValueError("list.append needs 2 args, like: [$list, $value]")

        ls = args[0]
        if isinstance(ls, str) and ls.startswith("$"):
            var = ls
            ls = []
            executor.set_variable(var, ls)

        if not isinstance(ls, list):
            raise ValueError("args[0] is not a list")

        ls.append(args[1])


class DictSetAction(Action):
    def __init__(self) -> None:
        super().__init__()
        self.spec = ActionSpec.from_dict({
            "name": "dict.set",
            "description": "Set a key-value pair in a dictionary.",

            "arguments": [
                {
                    "name": "d",
                    "type": "dict",
                    "description": "The dictionary in which to set the key-value pair.",
                    "required": True
                },
                {
                    "name": "key",
                    "type": "str",
                    "description": "The key for the value to set in the dictionary.",
                    "required": True
                },
                {
                    "name": "value",
                    "type": "any",
                    "description": "The value to set for the given key in the dictionary.",
                    "required": True
                }
            ]
        })

    def perform(
        self,
        d: dict,
        key: str,
        value: str,
        executor: Optional[Executor] = None,
        playbook: Optional[Playbook] = None,
        **kwargs
    ) -> Any:
        if executor is None:
            raise ValueError("executor is None")

        if isinstance(d, str) and d.startswith("$"):
            var = d
            d = {}
            executor.set_variable(var, d)

        if not isinstance(d, dict):
            raise ValueError("args[0] is not a dict")

        d[key] = value


class DictGetAction(Action):
    def __init__(self) -> None:
        super().__init__()
        self.spec = ActionSpec.from_dict({
            "name": "dict.get",
            "description": "Get a value by key from a dictionary.",
            "arguments": [
                {
                    "name": "d",
                    "type": "dict",
                    "description": "The dictionary from which to get the value.",
                    "required": True
                },
                {
                    "name": "key",
                    "type": "str",
                    "description": "The key for the value to retrieve from the dictionary.",
                    "required": True
                }
            ]
        })

    def perform(
        self,
        d: dict,
        key: str,
        executor: Optional[Executor] = None,
        playbook: Optional[Playbook] = None,
        **kwargs
    ) -> Any:
        if d is None or not isinstance(d, dict):
            raise ValueError("invalid dict")
        return d.get(key)
