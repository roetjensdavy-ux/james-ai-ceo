from typing import Dict, Any, Optional
from src.agents.base import BaseAgent
from src.agents.ceo import CEOAgent
from src.agents.marketing import MarketingAgent
from src.agents.deals import DealsAgent
from src.agents.finance import FinanceAgent
from src.agents.research import ResearchAgent
from src.agents.hr import HRAgent
from src.agents.legal import LegalAgent

class AgentRouter:
    """Routes tasks to the appropriate agent based on intent."""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {
            "ceo": CEOAgent(),
            "marketing": MarketingAgent(),
            "deals": DealsAgent(),
            "finance": FinanceAgent(),
            "research": ResearchAgent(),
            "hr": HRAgent(),
            "legal": LegalAgent(),
        }

    def detect_intent(self, message: str) -> str:
        """Detect which agent should handle the message."""
        msg = message.lower()

        if any(k in msg for k in ["deal", "pipeline", "scan", "acquisition", "merger", "invest", "opportunity"]):
            return "deals"

        if any(k in msg for k in ["marketing", "campaign", "content", "social", "lead", "ad", "promo"]):
            return "marketing"

        if any(k in msg for k in ["revenue", "money", "budget", "finance", "projection", "forecast", "cost", "euro"]):
            return "finance"

        if any(k in msg for k in ["research", "market", "tech", "trend", "innovation", "patent", "competitor"]):
            return "research"

        if any(k in msg for k in ["hire", "recruit", "candidate", "team", "hr", "employee", "interview"]):
            return "hr"

        if any(k in msg for k in ["contract", "legal", "compliance", "nda", "agreement", "law", "risk"]):
            return "legal"

        return "ceo"

    async def route(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Route a message to the appropriate agent and return the response."""
        intent = self.detect_intent(message)
        agent = self.agents.get(intent)

        if not agent:
            agent = self.agents["ceo"]

        response = await agent.handle_task(message, context)

        return {
            "agent": agent.name,
            "response": response,
            "agent_status": agent.get_status(),
        }

    def get_all_status(self) -> Dict[str, Dict]:
        """Get status of all agents."""
        return {name: agent.get_status() for name, agent in self.agents.items()}

# Global router instance
agent_router = AgentRouter()
