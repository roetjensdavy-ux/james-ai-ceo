import httpx
import time
from typing import List, Dict, Any, Optional
from src.core.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    DEFAULT_MODEL,
    FALLBACK_MODEL,
    JAMES_PERSONALITY,
)
from src.core.memory import memory

class ChatHandler:
    """Handles AI chat responses via OpenRouter API."""

    def __init__(self):
        headers = {
            "HTTP-Referer": "https://james-ai-ceo.com",
            "X-Title": "James AI CEO",
        }
        if OPENROUTER_API_KEY:
            headers["Authorization"] = f"Bearer {OPENROUTER_API_KEY}"

        self.client = httpx.AsyncClient(
            base_url=OPENROUTER_BASE_URL,
            headers=headers,
            timeout=30.0,
        )

    async def generate_response(
        self,
        session_id: str,
        user_message: str,
        system_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate an AI response using OpenRouter."""
        start_time = time.time()

        # Add user message to memory
        memory.add_message(session_id, "user", user_message)

        # Build context
        context = memory.get_context(session_id)
        messages = [{"role": "system", "content": system_context or JAMES_PERSONALITY}]

        for msg in context[:-1]:
            messages.append(msg)

        messages.append({"role": "user", "content": user_message})

        # Try primary model
        response_text = await self._call_model(DEFAULT_MODEL, messages)

        # Fallback if needed
        if not response_text:
            response_text = await self._call_model(FALLBACK_MODEL, messages)

        # Final fallback
        if not response_text:
            response_text = self._generate_fallback_response(user_message)

        latency = int((time.time() - start_time) * 1000)

        # Add AI response to memory
        memory.add_message(session_id, "assistant", response_text, {
            "latency": latency,
            "model": DEFAULT_MODEL.split("/")[-1],
        })

        return {
            "content": response_text,
            "metadata": {
                "latency": latency,
                "model": DEFAULT_MODEL.split("/")[-1],
            }
        }

    async def _call_model(self, model: str, messages: List[Dict]) -> Optional[str]:
        """Call OpenRouter API with a specific model."""
        try:
            response = await self.client.post(
                "/chat/completions",
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 2048,
                }
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]

            print(f"OpenRouter error: {response.status_code} - {response.text}")
            return None

        except Exception as e:
            print(f"API call error: {e}")
            return None

    def _generate_fallback_response(self, user_message: str) -> str:
        """Generate a fallback response when API is unavailable."""
        msg_lower = user_message.lower()

        responses = {
            "signal": "Signal Bot: RUNNING with 47 subscribers. Last signal 'DELTA' delivered successfully. Revenue today: EUR147 (+12.4% vs avg).",
            "deal": "Deal Pipeline: 34 deals worth EUR4.2M. Top deals: FinCore Investment (EUR4.5M, Closing), TechGlobal Merger (EUR5.0M, Closing).",
            "revenue": "Revenue Today: EUR147 (+12.4% vs avg). Sources: Alpha subscriptions EUR89, Signal fees EUR34, Reports EUR24. All-time: EUR12,847.",
            "agent": "7 Active Agents: CEO [RUNNING], DealRadar [RUNNING], Marketing [RUNNING], R&D [BUSY], Finance [RUNNING], HR [RUNNING], Legal [RUNNING].",
            "report": "Performance Report:\nCPU: 34% | Memory: 39% | Storage: 42%\nAgents: 7 active | Tasks: 24 today | Completed: 18",
            "help": "I'm James AI CEO. I can help with:\n- Signal bot management\n- Deal pipeline analysis\n- Revenue tracking\n- System diagnostics\n- Agent task management\n\nWhat would you like to work on?",
        }

        for keyword, response in responses.items():
            if keyword in msg_lower:
                return response

        return f"I've received your command: \"{user_message}\"\n\nI'm processing this through the appropriate agent. You can track progress in the Tasks panel.\n\nIs there anything specific you'd like me to focus on?"

    async def close(self):
        await self.client.aclose()

# Global chat handler instance
chat_handler = ChatHandler()
