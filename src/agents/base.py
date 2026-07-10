from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """Base class for all James AI agents."""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.status = "idle"
        self.tasks_completed = 0
        self.current_task = None

    @abstractmethod
    async def handle_task(self, task: str, context: Dict[str, Any] = None) -> str:
        """Handle a specific task."""
        pass

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "status": self.status,
            "tasks_completed": self.tasks_completed,
            "current_task": self.current_task,
        }

    def _format_response(self, data: str, title: str = None) -> str:
        """Format agent response in James style."""
        if title:
            return f"[{self.name.upper()}] {title}\n\n{data}"
        return f"[{self.name.upper()}]\n\n{data}"
