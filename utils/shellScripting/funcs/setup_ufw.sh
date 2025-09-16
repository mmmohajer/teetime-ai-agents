#!/bin/bash
set -e

echo "🔒 Setting up UFW firewall rules..."

# Reset to defaults
sudo ufw --force reset

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH, HTTP, HTTPS
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https

# Database (Postgres)
# sudo ufw allow 5432/tcp

# Docker Swarm
sudo ufw allow 2377/tcp    # Swarm management
sudo ufw allow 7946/tcp    # Swarm node communication
sudo ufw allow 7946/udp
sudo ufw allow 4789/udp    # Overlay network

# GlusterFS
sudo ufw allow 24007/tcp
sudo ufw allow 24009:24024/tcp
sudo ufw allow 38465:38467/tcp
sudo ufw allow 49152:60999/tcp

# Coturn (TURN/STUN)
sudo ufw allow 3478/udp     # STUN/TURN
sudo ufw allow 3478/tcp     # TURN TCP fallback
sudo ufw allow 5349/tcp     # TURN over TLS
sudo ufw allow 20000:20100/udp  # TURN relay media

# Janus Gateway
sudo ufw allow 8188/tcp     # Janus WebSocket
sudo ufw allow 8088/tcp     # Janus REST API (optional - restrict later if needed)
sudo ufw allow 10000:10200/udp  # Janus RTP/RTCP media

# Enable UFW
sudo ufw --force enable

# Show status
sudo ufw status verbose

echo "✅ Firewall rules applied successfully."
