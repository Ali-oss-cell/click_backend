#!/bin/bash
# Production Deployment Script for ClickExpress API

echo "🚀 Starting ClickExpress API Deployment..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "🔧 Installing required packages..."
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx certbot python3-certbot-nginx git -y

# Create application user
echo "👤 Creating application user..."
sudo adduser --disabled-password --gecos "" clickexpress
sudo usermod -aG sudo clickexpress

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /home/clickexpress/click_backend
sudo chown clickexpress:clickexpress /home/clickexpress/click_backend

# Switch to application user
echo "🔄 Switching to application user..."
sudo -u clickexpress bash << 'EOF'

# Navigate to application directory
cd /home/clickexpress/click_backend

# Clone repository
echo "📥 Cloning repository..."
git clone https://github.com/Ali-oss-cell/click_backend.git .

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install additional production packages
pip install gunicorn psycopg2-binary

# Create media and static directories
mkdir -p media static

# Set up environment variables
echo "⚙️ Setting up environment variables..."
cp production.env .env

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (interactive)
echo "👑 Creating superuser..."
python manage.py createsuperuser

EOF

# Configure PostgreSQL
echo "🐘 Configuring PostgreSQL..."
sudo -u postgres psql << 'EOF'
CREATE DATABASE clickexpress;
CREATE USER clickexpress_user WITH PASSWORD 'securepassword';
GRANT ALL PRIVILEGES ON DATABASE clickexpress TO clickexpress_user;
EOF

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/clickexpress > /dev/null << 'EOF'
server {
    listen 80;
    server_name api.clickexpress.ae;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/clickexpress/click_backend/static/;
    }

    location /media/ {
        alias /home/clickexpress/click_backend/media/;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/clickexpress /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Configure systemd service
echo "🔧 Configuring systemd service..."
sudo tee /etc/systemd/system/clickexpress.service > /dev/null << 'EOF'
[Unit]
Description=ClickExpress API
After=network.target

[Service]
User=clickexpress
Group=clickexpress
WorkingDirectory=/home/clickexpress/click_backend
Environment="PATH=/home/clickexpress/click_backend/venv/bin"
ExecStart=/home/clickexpress/click_backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 clickexpress_api.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
echo "🚀 Starting ClickExpress service..."
sudo systemctl daemon-reload
sudo systemctl enable clickexpress
sudo systemctl start clickexpress

# Configure firewall
echo "🔥 Configuring firewall..."
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# Get SSL certificate
echo "🔒 Setting up SSL certificate..."
sudo certbot --nginx -d api.clickexpress.ae --non-interactive --agree-tos --email admin@clickexpress.ae

# Restart services
echo "🔄 Restarting services..."
sudo systemctl restart clickexpress
sudo systemctl restart nginx

# Check status
echo "✅ Checking service status..."
sudo systemctl status clickexpress

echo "🎉 ClickExpress API deployment completed!"
echo "🌐 API URL: https://api.clickexpress.ae"
echo "👑 Admin URL: https://api.clickexpress.ae/admin/"
echo "📧 Test contact form: https://api.clickexpress.ae/api/v1/contact/"
