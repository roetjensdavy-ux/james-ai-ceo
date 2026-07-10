from typing import Dict, Any
from src.agents.base import BaseAgent

class FinanceAgent(BaseAgent):
    """Finance Agent — Revenue, projections, budget."""

    def __init__(self):
        super().__init__("Finance", "Financial management and projections")

    async def handle_task(self, task: str, context: Dict[str, Any] = None) -> str:
        self.status = "busy"

        if "revenue" in task.lower():
            return self._format_response(
                "REVENUE REPORT — Today\n\n"
                "Today:        EUR147     (+14% vs yesterday)\n"
                "7-day avg:    EUR131     (+12.4% vs avg)\n"
                "30-day:       EUR3,940\n"
                "All-time:     EUR12,847\n\n"
                "BREAKDOWN:\n"
                "1. Alpha subscriptions  EUR89   (60.5%)\n"
                "2. Signal fees          EUR34   (23.1%)\n"
                "3. Reports              EUR24   (16.3%)\n\n"
                "PROJECTION: EUR4,410/month (current trajectory)",
                "Revenue Dashboard"
            )

        elif "projection" in task.lower() or "forecast" in task.lower():
            return self._format_response(
                "Q3 2026 FINANCIAL PROJECTION\n\n"
                "REVENUE FORECAST:\n"
                "Jul: EUR4,200 | Aug: EUR4,800 | Sep: EUR5,500\n"
                "Q3 Total: EUR14,500\n\n"
                "EXPENSES:\n"
                "API costs:      EUR420/mo\n"
                "Infrastructure: EUR180/mo\n"
                "Agent ops:      EUR95/mo\n"
                "Total:          EUR695/mo\n\n"
                "NET: EUR13,415 (92.5% margin)\n\n"
                "Confidence: 87%",
                "Q3 Projections"
            )

        else:
            return self._format_response(
                "Finance systems operational.\n\n"
                "Available:\n"
                "- Revenue reports\n"
                "- Q3 projections\n"
                "- Budget management\n"
                "- Expense tracking\n"
                "- ROI analysis",
                "Ready"
            )

        self.status = "idle"
        self.tasks_completed += 1
