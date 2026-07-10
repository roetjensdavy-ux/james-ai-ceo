from typing import Dict, Any
from src.agents.base import BaseAgent

class HRAgent(BaseAgent):
    """HR Agent — Recruitment, team management."""

    def __init__(self):
        super().__init__("HR", "Recruitment and team management")

    async def handle_task(self, task: str, context: Dict[str, Any] = None) -> str:
        self.status = "busy"

        if "recruit" in task.lower() or "hiring" in task.lower():
            return self._format_response(
                "RECRUITMENT STATUS\n\n"
                "OPEN POSITIONS (5):\n"
                "1. AI Engineer (Senior)     — 12 applicants\n"
                "2. Data Scientist           —  8 applicants\n"
                "3. Product Manager          —  5 applicants\n"
                "4. DevOps Engineer          —  7 applicants\n"
                "5. Sales Lead               —  3 applicants\n\n"
                "SCREENING:\n"
                "- Completed: 23 candidates\n"
                "- Scheduled: 4 interviews\n"
                "- Offers:    1 pending\n\n"
                "RETENTION: 87% (target: 85%)",
                "Hiring Pipeline"
            )

        else:
            return self._format_response(
                "HR systems operational.\n\n"
                "Available:\n"
                "- Recruitment pipeline\n"
                "- Candidate screening\n"
                "- Interview scheduling\n"
                "- Team analytics",
                "Ready"
            )

        self.status = "idle"
        self.tasks_completed += 1
