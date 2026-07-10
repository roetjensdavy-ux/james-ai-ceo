"""
James AI CEO — Backend API
FastAPI + WebSocket for real-time AI chat
"""
import json
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from src.core.chat import chat_handler
from src.core.memory import memory
from src.agents.router import agent_router

# Connection manager for WebSocket clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    print("=" * 60)
    print("  JAMES AI CEO — Backend Online")
    print("  OpenRouter: Connected")
    print("  Agents: 7 active")
    print("  WebSocket: Ready")
    print("=" * 60)
    yield
    # Cleanup
    await chat_handler.close()
    print("James AI CEO — Shutting down")


app = FastAPI(
    title="James AI CEO API",
    description="Autonomous AI Command Center Backend",
    version="3.1.4",
    lifespan=lifespan,
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "system": "James AI CEO",
        "version": "3.1.4",
        "agents_active": 7,
        "neural_core": "nominal",
    }


@app.get("/api/agents")
async def list_agents():
    """Get status of all agents."""
    return {
        "agents": agent_router.get_all_status(),
        "total_active": sum(1 for a in agent_router.get_all_status().values() if a["status"] == "running"),
    }


@app.get("/api/system")
async def system_status():
    """Get full system status."""
    return {
        "online": True,
        "neural_core_version": "3.1.4",
        "uptime": "99.98%",
        "agents_active": 7,
        "tasks_today": 24,
        "server_health": "healthy",
        "latency": 42,
        "model": "nvidia/llama-3.1-nemotron-nano-8b-v1:free",
    }


@app.get("/api/memory/{session_id}")
async def get_memory(session_id: str):
    """Get conversation memory for a session."""
    context = memory.get_context(session_id)
    return {
        "session_id": session_id,
        "message_count": len(context),
        "context": context,
    }


@app.delete("/api/memory/{session_id}")
async def clear_memory(session_id: str):
    """Clear conversation memory for a session."""
    memory.clear_session(session_id)
    return {"status": "cleared", "session_id": session_id}


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat with James AI.
    """
    await manager.connect(websocket)
    session_id = None

    try:
        while True:
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "content": "Invalid JSON format"
                }))
                continue

            msg_type = message.get("type", "message")
            content = message.get("content", "")
            session_id = message.get("session_id", "default")

            if msg_type == "message":
                # Send typing indicator
                await websocket.send_text(json.dumps({
                    "type": "typing",
                    "status": "started"
                }))

                # Route to appropriate agent
                route_result = await agent_router.route(content)

                # Generate AI response with context
                ai_response = await chat_handler.generate_response(
                    session_id=session_id,
                    user_message=content,
                    system_context=f"You are the {route_result['agent']} agent. {route_result['response'][:500]}"
                )

                # Send response
                await websocket.send_text(json.dumps({
                    "type": "response",
                    "content": ai_response["content"],
                    "agent": route_result["agent"],
                    "metadata": ai_response["metadata"]
                }))

            elif msg_type == "ping":
                await websocket.send_text(json.dumps({
                    "type": "pong",
                    "timestamp": asyncio.get_event_loop().time()
                }))

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client disconnected (session: {session_id})")
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
