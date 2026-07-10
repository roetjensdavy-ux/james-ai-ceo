#!/bin/bash
# ============================================================
# James AI CEO — Complete Deployment Script
# Run as: sudo bash install.sh
# ============================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}"
echo "============================================================"
echo "  JAMES AI CEO — Complete Deployment"
echo "  Frontend + Backend + 7 AI Agents"
echo "============================================================"
echo -e "${NC}"

INSTALL_DIR="/opt/james-ai"
FRONTEND_DIR="/opt/james-ai/frontend"
SERVICE_NAME="james-ai"
USER="jamesai"

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Error: Please run as root (sudo bash install.sh)${NC}"
    exit 1
fi

# Step 1: System dependencies
echo -e "${YELLOW}[1/9] Installing system dependencies...${NC}"
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv nginx curl git ufw

# Step 2: Create user
echo -e "${YELLOW}[2/9] Creating service user...${NC}"
if ! id "$USER" &>/dev/null; then
    useradd -r -s /bin/false -d "$INSTALL_DIR" "$USER"
fi

# Step 3: Copy backend
echo -e "${YELLOW}[3/9] Installing backend...${NC}"
mkdir -p "$INSTALL_DIR"
if [ -d "src" ]; then
    cp -r src "$INSTALL_DIR/"
    cp requirements.txt "$INSTALL_DIR/"
    cp .env "$INSTALL_DIR/" 2>/dev/null || true
else
    echo -e "${RED}Warning: src/ not found.${NC}"
fi

# Step 4: Copy frontend
echo -e "${YELLOW}[4/9] Installing frontend...${NC}"
if [ -d "frontend" ]; then
    rm -rf "$FRONTEND_DIR"
    cp -r frontend "$FRONTEND_DIR"
    echo -e "${GREEN}  Frontend copied to $FRONTEND_DIR${NC}"
else
    echo -e "${YELLOW}Warning: frontend/ not found. Building from source...${NC}"
    mkdir -p "$FRONTEND_DIR"
    # Frontend will need to be copied separately or built
fi

# Step 5: Python environment
echo -e "${YELLOW}[5/9] Setting up Python virtual environment...${NC}"
cd "$INSTALL_DIR"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Step 6: Create .env if not exists
echo -e "${YELLOW}[6/9] Checking configuration...${NC}"
if [ ! -f "$INSTALL_DIR/.env" ]; then
    cat > "$INSTALL_DIR/.env" << 'EOF'
# OpenRouter API (primary AI provider) — ADD YOUR KEY HERE
OPENROUTER_API_KEY=your_openrouter_key_here

# NVIDIA NIM API (optional fallback)
NVIDIA_NIM_API_KEY=your_nvidia_key_here

# Moonshot AI (optional fallback)
MOONSHOT_API_KEY=your_moonshot_key_here

# Server config
HOST=0.0.0.0
PORT=8000
EOF
    echo -e "${YELLOW}  Created default .env. Edit $INSTALL_DIR/.env with your API keys.${NC}"
fi

# Step 7: Create systemd service
echo -e "${YELLOW}[7/9] Creating systemd service...${NC}"
cat > "/etc/systemd/system/${SERVICE_NAME}.service" << EOF
[Unit]
Description=James AI CEO — Autonomous AI Backend
After=network.target

[Service]
Type=simple
User=${USER}
Group=${USER}
WorkingDirectory=${INSTALL_DIR}
Environment=PYTHONPATH=${INSTALL_DIR}
EnvironmentFile=${INSTALL_DIR}/.env
ExecStart=${INSTALL_DIR}/.venv/bin/python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Step 8: Configure nginx
echo -e "${YELLOW}[8/9] Configuring nginx...${NC}"
cat > /etc/nginx/sites-available/james-ai << 'EOF'
server {
    listen 80 default_server;
    server_name _;
    client_max_body_size 50M;

    location / {
        root /opt/james-ai/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }

    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 60s;
    }

    location /ws/ {
        proxy_pass http://localhost:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
    }

    location /health {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_read_timeout 10s;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        root /opt/james-ai/frontend;
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
}
EOF

ln -sf /etc/nginx/sites-available/james-ai /etc/nginx/sites-enabled/james-ai
rm -f /etc/nginx/sites-enabled/default 2>/dev/null || true
nginx -t

# Step 9: Firewall + start services
echo -e "${YELLOW}[9/9] Configuring firewall and starting services...${NC}"
ufw allow 22/tcp 2>/dev/null || true
ufw allow 80/tcp 2>/dev/null || true
ufw allow 443/tcp 2>/dev/null || true
ufw allow 8000/tcp 2>/dev/null || true

chown -R "${USER}:${USER}" "$INSTALL_DIR"
chmod 600 "$INSTALL_DIR/.env" 2>/dev/null || true
chmod -R 755 "$FRONTEND_DIR"

systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl restart nginx
systemctl restart "$SERVICE_NAME"

sleep 4

echo ""
if systemctl is-active --quiet "$SERVICE_NAME"; then
    SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')
    echo -e "${GREEN}"
    echo "============================================================"
    echo "  JAMES AI CEO — Deployment Complete!"
    echo "============================================================"
    echo -e "${NC}"
    echo -e "  ${CYAN}Command Center:${NC}   http://${SERVER_IP}"
    echo -e "  ${CYAN}Health Check:${NC}     http://${SERVER_IP}/health"
    echo -e "  ${CYAN}API Docs:${NC}         http://${SERVER_IP}/api/docs"
    echo -e "  ${CYAN}WebSocket:${NC}        ws://${SERVER_IP}/ws/chat"
    echo ""
    echo -e "  ${YELLOW}Commands:${NC}"
    echo -e "    systemctl status james-ai     # Check service"
    echo -e "    systemctl restart james-ai    # Restart"
    echo -e "    systemctl restart nginx       # Restart web"
    echo -e "    journalctl -u james-ai -f     # View logs"
    echo ""
    echo -e "  ${YELLOW}Next:${NC} Edit API keys: ${CYAN}nano $INSTALL_DIR/.env${NC}"
else
    echo -e "${RED}Service failed. Check logs: journalctl -u james-ai -f${NC}"
    exit 1
fi
