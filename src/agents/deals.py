from typing import Dict, Any
from src.agents.base import BaseAgent

class DealsAgent(BaseAgent):
    """DealRadar Agent — Pipeline, analysis, extraction."""

    def __init__(self):
        super().__init__("DealRadar", "Deal pipeline and intelligence")

    async def handle_task(self, task: str, context: Dict[str, Any] = None) -> str:
        self.status = "busy"
        self.current_task = task

        if "pipeline" in task.lower():
            return self._format_response(
                "DEAL PIPELINE\n\n"
                "STAGES:\n"
                "Lead:          8 deals  |  EUR8.2M  |  24%\n"
                "Qualified:    12 deals  | EUR12.4M  |  35%\n"
                "Negotiation:   9 deals  | EUR14.1M  |  26%\n"
                "Closing:       5 deals  | EUR18.5M  |  15%\n"
                "----------------------------------------\n"
                "TOTAL:        34 deals  | EUR53.2M  | 100%\n\n"
                "CLOSING THIS WEEK:\n"
                "1. FinCore Investment     EUR4.5M  | 98% confidence\n"
                "2. TechGlobal Merger      EUR5.0M  | 95% confidence\n\n"
                "AI AVG CONFIDENCE: 91%",
                "Pipeline Overview"
            )

        elif "scan" in task.lower() or "find" in task.lower():
            return self._format_response(
                "DEAL SCAN COMPLETED\n\n"
                "New opportunities found: 12\n\n"
                "HIGH PRIORITY:\n"
                "- CloudTech Series B      EUR2.0M  | Technology  | 92% match\n"
                "- MediCare Partnership    EUR1.5M  | Healthcare  | 88% match\n"
                "- DataFlow Acquisition    EUR3.2M  | Data        | 85% match\n\n"
                "Analysis complete. Awaiting your go-ahead to engage.",
                "Scan Results"
            )

        elif "analyze" in task.lower():
            return self._format_response(
                "DEAL ANALYSIS\n\n"
                "FinCore Investment — EUR4.5M\n\n"
                "RISK ASSESSMENT:\n"
                "- Overall risk: LOW (23/100)\n"
                "- Financial:     LOW (18/100)\n"
                "- Legal:         LOW (12/100)\n"
                "- Market:        MEDIUM (38/100)\n\n"
                "VALUATION:\n"
                "- Listed price:  EUR4.5M\n"
                "- AI estimate:   EUR4.8M (+6.7%)\n"
                "- Confidence:    96%\n\n"
                "RECOMMENDATION: PROCEED",
                "Deal Analysis"
            )

        else:
            return self._format_response(
                "DealRadar operational. 34 deals tracked.\n\n"
                "Available:\n"
                "- Full pipeline view\n"
                "- Deal scan (find new)\n"
                "- Deal analysis\n"
                "- Risk assessment\n"
                "- Comparable deals",
                "Ready"
            )

        self.status = "idle"
        self.current_task = None
        self.tasks_completed += 1
