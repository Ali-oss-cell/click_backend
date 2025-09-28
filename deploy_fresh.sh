#!/bin/bash

# ClickExpress API - One Command Fresh Deployment
# This script will clean everything and deploy fresh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 ClickExpress API - Fresh Deployment${NC}"
echo -e "${YELLOW}This will clean the server and deploy everything from scratch${NC}"
echo ""

# Make scripts executable
chmod +x clean_server.sh
chmod +x clean_deploy.sh

# Step 1: Clean the server
echo -e "${RED}Step 1: Cleaning server...${NC}"
./clean_server.sh

echo ""
echo -e "${GREEN}Server cleaned successfully!${NC}"
echo ""

# Step 2: Deploy fresh
echo -e "${BLUE}Step 2: Deploying fresh installation...${NC}"
./clean_deploy.sh

echo ""
echo -e "${GREEN}🎉 Fresh deployment completed successfully!${NC}"
echo -e "${YELLOW}Your ClickExpress API is now running!${NC}"
