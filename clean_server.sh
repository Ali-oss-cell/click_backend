#!/bin/bash

# ClickExpress API - Server Cleanup Script
# This script will completely clean the server

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${RED}🧹 ClickExpress Server Cleanup${NC}"
echo -e "${YELLOW}This will completely clean the server - ALL DATA WILL BE LOST!${NC}"
echo -e "${RED}Are you sure you want to continue? (yes/no)${NC}"
read -r confirmation

if [ "$confirmation" != "yes" ]; then
    echo -e "${BLUE}Cleanup cancelled.${NC}"
    exit 0
fi

echo -e "${BLUE}Starting server cleanup...${NC}"

# Stop all services
echo -e "${YELLOW}Stopping services...${NC}"
systemctl stop clickexpress 2>/dev/null || true
systemctl stop nginx 2>/dev/null || true
systemctl stop postgresql 2>/dev/null || true

# Remove systemd service
echo -e "${YELLOW}Removing systemd service...${NC}"
systemctl disable clickexpress 2>/dev/null || true
rm -f /etc/systemd/system/clickexpress.service
systemctl daemon-reload

# Remove nginx configuration
echo -e "${YELLOW}Removing nginx configuration...${NC}"
rm -f /etc/nginx/sites-enabled/clickexpress
rm -f /etc/nginx/sites-available/clickexpress
systemctl restart nginx

# Remove SSL certificates
echo -e "${YELLOW}Removing SSL certificates...${NC}"
certbot delete --cert-name api.clickexpress.ae --non-interactive 2>/dev/null || true

# Remove project user and directory
echo -e "${YELLOW}Removing project user and directory...${NC}"
rm -rf /home/clickexpress
userdel -r clickexpress 2>/dev/null || true

# Remove databases
echo -e "${YELLOW}Removing databases...${NC}"
sudo -u postgres psql -c "DROP DATABASE IF EXISTS clickexpress;" 2>/dev/null || true
sudo -u postgres psql -c "DROP USER IF EXISTS clickexpress_user;" 2>/dev/null || true

# Remove packages (optional - uncomment if you want to remove everything)
# echo -e "${YELLOW}Removing packages...${NC}"
# apt remove -y python3-pip postgresql postgresql-contrib nginx certbot python3-certbot-nginx

# Clean up any remaining files
echo -e "${YELLOW}Cleaning up remaining files...${NC}"
rm -f /root/clickexpress_credentials.txt
rm -f /tmp/clickexpress_*

echo -e "${GREEN}✅ Server cleanup completed successfully!${NC}"
echo -e "${BLUE}The server is now clean and ready for a fresh deployment.${NC}"
