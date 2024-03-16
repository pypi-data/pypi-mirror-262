from __future__ import annotations
from typing import TYPE_CHECKING
from abc import abstractmethod
from attr import define

if TYPE_CHECKING:
    from griptape.memory import TaskMemory
    from griptape.tools import BaseTool
    from griptape.tasks import ActionSubtask


@define(slots=False)
class ActionSubtaskOriginMixin:
    @abstractmethod
    def find_tool(self, tool_name: str) -> BaseTool:
        ...

    @abstractmethod
    def find_memory(self, memory_name: str) -> TaskMemory:
        ...

    @abstractmethod
    def find_subtask(self, subtask_id: str) -> ActionSubtask:
        ...

    @abstractmethod
    def add_subtask(self, subtask: ActionSubtask) -> ActionSubtask:
        ...
