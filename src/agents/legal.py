from typing import Dict, Any
from src.agents.base import BaseAgent

class LegalAgent(BaseAgent):
    """Legal Agent — Contracts, compliance, risk."""

    def __init__(self):
        super().__init__("Legal", "Contract review and compliance")

    async def handle_task(self, task: str, context: Dict[str, Any] = None) -> str:
        self.status = "busy"

        if "contract" in task.lower():
            return self._format_response(
                "CONTRACT REVIEW STATUS\n\n"
                "IN REVIEW (3):\n"
                "1. SaaS Agreement v2.1      — 85% complete\n"
                "2. Partnership — CloudTech   — 60% complete\n"
                "3. Investment — FinCore      — 90% complete\n\n"
                "COMPLETED TODAY:\n"
                "- NDA — MediCare (signed)\n"
                "- Amendment — Series B terms\n\n"
                "COMPLIANCE: 100%\n"
                "Disputes: 0",
                "Contract Pipeline"
            )

        elif "compliance" in task.lower():
            return self._format_response(
                "COMPLIANCE AUDIT\n\n"
                "GDPR:     COMPLIANT (last audit: 2 weeks ago)\n"
                "SOC2:     COMPLIANT (cert valid until Dec 2026)\n"
                "DORA:     MONITORING (EU regulation upcoming)\n"
                "PCI-DSS:  N/A (Stripe handles payments)\n\n"
                "ALERT: EU AI Act may impact data processing pipeline.\n"
                "Recommendation: Review AI governance framework.",
                "Compliance Status"
            )

        else:
            return self._format_response(
                "Legal systems operational.\n\n"
                "Available:\n"
                "- Contract review\n"
                "- Compliance audit\n"
                "- Risk assessment\n"
                "- NDA generation",
                "Ready"
            )

        self.status = "idle"
        self.tasks_completed += 1
