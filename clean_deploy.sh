#!/bin/bash

# ClickExpress API - Complete Clean Deployment Script
# This script will clean the server and deploy everything from scratch

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="clickexpress"
PROJECT_USER="clickexpress"
PROJECT_DIR="/home/$PROJECT_USER/click_backend"
DOMAIN="api.clickexpress.ae"
EMAIL="admin@clickexpress.ae"
DB_NAME="clickexpress"
DB_USER="clickexpress_user"
DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
SECRET_KEY=$(openssl rand -base64 50 | tr -d "=+/" | cut -c1-50)
JWT_SECRET=$(openssl rand -base64 50 | tr -d "=+/" | cut -c1-50)

echo -e "${BLUE}🚀 Starting ClickExpress API Clean Deployment${NC}"
echo -e "${YELLOW}This will clean the server and deploy everything from scratch${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Step 1: Clean existing installation
print_info "Cleaning existing installation..."

# Stop services
systemctl stop clickexpress 2>/dev/null || true
systemctl stop nginx 2>/dev/null || true

# Remove existing project
rm -rf /home/$PROJECT_USER 2>/dev/null || true
userdel -r $PROJECT_USER 2>/dev/null || true

# Clean up any existing databases
sudo -u postgres psql -c "DROP DATABASE IF EXISTS $DB_NAME;" 2>/dev/null || true
sudo -u postgres psql -c "DROP USER IF EXISTS $DB_USER;" 2>/dev/null || true

print_status "Server cleaned successfully"

# Step 2: Update system
print_info "Updating system packages..."
apt update -y
apt upgrade -y

# Step 3: Install required packages
print_info "Installing required packages..."
apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx certbot python3-certbot-nginx git curl wget unzip

# Step 4: Configure PostgreSQL
print_info "Configuring PostgreSQL..."

# Start PostgreSQL
systemctl start postgresql
systemctl enable postgresql

# Create database and user
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
sudo -u postgres psql -c "GRANT USAGE ON SCHEMA public TO $DB_USER;"
sudo -u postgres psql -c "GRANT CREATE ON SCHEMA public TO $DB_USER;"
sudo -u postgres psql -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;"
sudo -u postgres psql -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;"

print_status "PostgreSQL configured successfully"

# Step 5: Create project user and directory
print_info "Creating project user and directory..."
useradd -m -s /bin/bash $PROJECT_USER
mkdir -p $PROJECT_DIR
chown -R $PROJECT_USER:$PROJECT_USER $PROJECT_DIR

# Step 6: Clone repository
print_info "Cloning repository..."
cd $PROJECT_DIR
sudo -u $PROJECT_USER git clone https://github.com/Ali-oss-cell/click_backend.git .
cd $PROJECT_DIR

# Step 7: Create virtual environment
print_info "Creating virtual environment..."
sudo -u $PROJECT_USER python3 -m venv venv
sudo -u $PROJECT_USER $PROJECT_DIR/venv/bin/pip install --upgrade pip

# Step 8: Install Python dependencies
print_info "Installing Python dependencies..."
sudo -u $PROJECT_USER $PROJECT_DIR/venv/bin/pip install -r requirements.txt

# Step 9: Create production environment file
print_info "Creating production environment file..."
cat > $PROJECT_DIR/production.env << EOF
# Production Environment Variables
DEBUG=False
SECRET_KEY=$SECRET_KEY
ALLOWED_HOSTS=$DOMAIN,localhost,127.0.0.1

# Database Configuration
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=localhost
DB_PORT=5432

# JWT Configuration
JWT_SECRET=$JWT_SECRET
JWT_EXPIRES_IN=86400

# Email Configuration
DEFAULT_FROM_EMAIL=noreply@clickexpress.ae
ADMIN_EMAIL=$EMAIL

# Mailgun Configuration (Update these with your actual values)
MAILGUN_API_KEY=your-mailgun-api-key-here
MAILGUN_DOMAIN=mg.clickexpress.ae
MAILGUN_FROM_EMAIL=noreply@clickexpress.ae

# File Uploads
MEDIA_ROOT=$PROJECT_DIR/media
STATIC_ROOT=$PROJECT_DIR/static
EOF

chown $PROJECT_USER:$PROJECT_USER $PROJECT_DIR/production.env
chmod 600 $PROJECT_DIR/production.env

print_status "Environment file created"

# Step 10: Run Django migrations
print_info "Running Django migrations..."
cd $PROJECT_DIR
sudo -u $PROJECT_USER $PROJECT_DIR/venv/bin/python manage.py migrate
sudo -u $PROJECT_USER $PROJECT_DIR/venv/bin/python manage.py collectstatic --noinput

# Create superuser (optional)
print_info "Creating Django superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '$EMAIL', 'admin123')" | sudo -u $PROJECT_USER $PROJECT_DIR/venv/bin/python manage.py shell

print_status "Django setup completed"

# Step 11: Create systemd service
print_info "Creating systemd service..."
cat > /etc/systemd/system/clickexpress.service << EOF
[Unit]
Description=ClickExpress API
After=network.target

[Service]
Type=exec
User=$PROJECT_USER
Group=$PROJECT_USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 clickexpress_api.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable clickexpress
systemctl start clickexpress

print_status "Systemd service created and started"

# Step 12: Configure Nginx
print_info "Configuring Nginx..."
cat > /etc/nginx/sites-available/clickexpress << EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias $PROJECT_DIR/static/;
    }

    location /media/ {
        alias $PROJECT_DIR/media/;
    }
}
EOF

ln -sf /etc/nginx/sites-available/clickexpress /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

print_status "Nginx configured"

# Step 13: Configure firewall
print_info "Configuring firewall..."
ufw allow 22
ufw allow 80
ufw allow 443
ufw --force enable

print_status "Firewall configured"

# Step 14: Get SSL certificate
print_info "Getting SSL certificate..."
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email $EMAIL

print_status "SSL certificate installed"

# Step 15: Final status check
print_info "Performing final status check..."

# Check services
systemctl is-active --quiet clickexpress && print_status "ClickExpress service is running" || print_error "ClickExpress service failed"
systemctl is-active --quiet nginx && print_status "Nginx is running" || print_error "Nginx failed"
systemctl is-active --quiet postgresql && print_status "PostgreSQL is running" || print_error "PostgreSQL failed"

# Test API endpoint
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1/contact/ | grep -q "200\|405"; then
    print_status "API endpoint is responding"
else
    print_error "API endpoint is not responding"
fi

# Step 16: Display final information
echo -e "${GREEN}"
echo "🎉 ClickExpress API Deployment Completed Successfully!"
echo "=================================================="
echo "🌐 API URL: https://$DOMAIN"
echo "👤 Admin Panel: https://$DOMAIN/admin/"
echo "📧 Admin Email: $EMAIL"
echo "🔑 Admin Password: admin123"
echo ""
echo "📋 Database Information:"
echo "   Database: $DB_NAME"
echo "   User: $DB_USER"
echo "   Password: $DB_PASSWORD"
echo ""
echo "🔧 Service Management:"
echo "   Status: systemctl status clickexpress"
echo "   Restart: systemctl restart clickexpress"
echo "   Logs: journalctl -u clickexpress -f"
echo ""
echo "📁 Project Directory: $PROJECT_DIR"
echo "🔐 Environment File: $PROJECT_DIR/production.env"
echo ""
echo "⚠️  IMPORTANT: Update your Mailgun configuration in production.env"
echo "   MAILGUN_API_KEY=your-actual-mailgun-api-key"
echo "   MAILGUN_DOMAIN=your-actual-mailgun-domain"
echo -e "${NC}"

print_status "Deployment completed successfully!"

# Save credentials to file
cat > /root/clickexpress_credentials.txt << EOF
ClickExpress API Deployment Credentials
=====================================

API URL: https://$DOMAIN
Admin Panel: https://$DOMAIN/admin/
Admin Email: $EMAIL
Admin Password: admin123

Database Information:
- Database: $DB_NAME
- User: $DB_USER
- Password: $DB_PASSWORD

Project Directory: $PROJECT_DIR
Environment File: $PROJECT_DIR/production.env

Service Management:
- Status: systemctl status clickexpress
- Restart: systemctl restart clickexpress
- Logs: journalctl -u clickexpress -f

IMPORTANT: Update Mailgun configuration in production.env
EOF

print_info "Credentials saved to /root/clickexpress_credentials.txt"
