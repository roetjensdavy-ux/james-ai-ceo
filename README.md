# James AI CEO

Autonomous AI Command Center — 7 AI agents, real-time chat, neural network visualization.

## Quick Deploy

```bash
# On your server (as root)
git clone https://github.com/roetjensdavy-ux/james-ai-ceo.git /tmp/james-ai
cd /tmp/james-ai
sudo bash install.sh
```

Then edit your API keys:
```bash
nano /opt/james-ai/.env
systemctl restart james-ai
```

## What's Included

- **Frontend**: React + Three.js neural network + WebSocket chat
- **Backend**: FastAPI + 7 AI agents + OpenRouter integration
- **AI Agents**: CEO, Marketing, DealRadar, Finance, R&D, HR, Legal
- **Infra**: Nginx reverse proxy + systemd service + firewall

## API Keys Needed

Get your free API key at [openrouter.ai/keys](https://openrouter.ai/keys)

## Architecture

```
User → Nginx (port 80) → Frontend (static)
                    ↓
              Backend (port 8000)
                    ↓
              WebSocket /api /ws
                    ↓
              Agent Router → OpenRouter API
```
