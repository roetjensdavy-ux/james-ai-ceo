import json
import os
from typing import List, Dict, Any
from datetime import datetime
from src.core.config import MAX_CONTEXT_MESSAGES, MEMORY_FILE

class ConversationMemory:
    """Manages conversation history and context for James AI."""

    def __init__(self):
        self.sessions: Dict[str, List[Dict[str, Any]]] = {}
        self._load_from_disk()

    def _load_from_disk(self):
        """Load memory from disk if available."""
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, 'r') as f:
                    data = json.load(f)
                    self.sessions = {k: v for k, v in data.items()}
            except Exception:
                self.sessions = {}

    def _save_to_disk(self):
        """Persist memory to disk."""
        try:
            with open(MEMORY_FILE, 'w') as f:
                json.dump(self.sessions, f, default=str)
        except Exception:
            pass

    def add_message(self, session_id: str, role: str, content: str, metadata: Dict = None):
        """Add a message to the conversation history."""
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        self.sessions[session_id].append(message)

        if len(self.sessions[session_id]) > MAX_CONTEXT_MESSAGES:
            self.sessions[session_id] = self.sessions[session_id][-MAX_CONTEXT_MESSAGES:]

        self._save_to_disk()

    def get_context(self, session_id: str) -> List[Dict[str, str]]:
        """Get conversation context as list of {role, content} for LLM."""
        if session_id not in self.sessions:
            return []

        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.sessions[session_id][-MAX_CONTEXT_MESSAGES:]
        ]

    def get_recent_summary(self, session_id: str) -> str:
        """Get a summary of recent conversation topics."""
        if session_id not in self.sessions:
            return ""

        recent = self.sessions[session_id][-5:]
        topics = []
        for msg in recent:
            if msg["role"] == "user":
                topics.append(msg["content"][:50])

        return "Recent topics: " + ", ".join(topics) if topics else ""

    def clear_session(self, session_id: str):
        """Clear a specific session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            self._save_to_disk()

# Global memory instance
memory = ConversationMemory()
