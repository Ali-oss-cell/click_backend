# ClickExpress API - Production Deployment Guide

## 🚀 DigitalOcean Droplet Deployment

### Prerequisites
- DigitalOcean droplet created
- Domain DNS configured
- SSH access to droplet

### Step 1: Connect to Droplet
```bash
ssh root@your-droplet-ip
```

### Step 2: Run Deployment Script
```bash
# Download and run deployment script
curl -O https://raw.githubusercontent.com/Ali-oss-cell/click_backend/main/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

### Step 3: Manual Configuration (if needed)

#### Update Environment Variables
```bash
# Edit production environment
nano /home/clickexpress/click_backend/.env
```

#### Update with your actual values:
```env
DEBUG=False
SECRET_KEY=your-super-secure-secret-key-here
ALLOWED_HOSTS=api.clickexpress.ae,your-droplet-ip

# Database
DB_NAME=clickexpress
DB_USER=clickexpress_user
DB_PASSWORD=your-secure-database-password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
DEFAULT_FROM_EMAIL=noreply@clickexpress.ae
ADMIN_EMAIL=admin@clickexpress.ae

# Mailgun Configuration
MAILGUN_API_KEY=85922afaeaffbe17ce49a43e8ea6423b-e1076420-0ca66964
MAILGUN_DOMAIN=mg.clickexpress.ae
MAILGUN_FROM_EMAIL=noreply@clickexpress.ae
```

### Step 4: Test Deployment

#### Check Service Status
```bash
sudo systemctl status clickexpress
sudo systemctl status nginx
```

#### Test API Endpoints
```bash
# Test contact form
curl -X POST https://api.clickexpress.ae/api/v1/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test Message",
    "message": "Testing production deployment"
  }'
```

#### Check Logs
```bash
# Django logs
sudo journalctl -u clickexpress -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Step 5: SSL Certificate
```bash
# Get SSL certificate
sudo certbot --nginx -d api.clickexpress.ae
```

### Step 6: Firewall Configuration
```bash
# Configure firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## 🔧 Production Configuration

### Database Setup
- PostgreSQL installed and configured
- Database: `clickexpress`
- User: `clickexpress_user`
- Password: Set in environment variables

### Static Files
- Served by WhiteNoise
- Collected to `/home/clickexpress/click_backend/static/`
- Media files in `/home/clickexpress/click_backend/media/`

### Security Features
- SSL/TLS encryption
- HSTS headers
- XSS protection
- CSRF protection
- Secure cookies

### Monitoring
- Systemd service management
- Nginx reverse proxy
- Log rotation
- Error tracking

## 📧 Email Configuration

### Mailgun Setup
1. Add domain in Mailgun dashboard
2. Configure DNS records in Hostinger
3. Verify domain in Mailgun
4. Test email delivery

### Email Features
- Contact form submissions
- Admin notifications
- User confirmations
- Newsletter signup

## 🚨 Troubleshooting

### Common Issues

#### Service Not Starting
```bash
sudo systemctl restart clickexpress
sudo systemctl status clickexpress
```

#### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test database connection
sudo -u postgres psql -c "\l"
```

#### SSL Certificate Issues
```bash
# Renew certificate
sudo certbot renew

# Check certificate status
sudo certbot certificates
```

#### Email Not Sending
```bash
# Check Mailgun configuration
# Verify DNS records
# Check Django logs
sudo journalctl -u clickexpress -f
```

### Performance Optimization

#### Gunicorn Workers
```bash
# Edit service file
sudo nano /etc/systemd/system/clickexpress.service

# Update workers count
ExecStart=/home/clickexpress/click_backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 clickexpress_api.wsgi:application
```

#### Database Optimization
```bash
# Install Redis for caching (optional)
sudo apt install redis-server
```

## 📊 Monitoring

### Health Checks
- API endpoint: `https://api.clickexpress.ae/api/v1/contact/`
- Admin panel: `https://api.clickexpress.ae/admin/`
- Static files: `https://api.clickexpress.ae/static/`

### Log Files
- Application logs: `sudo journalctl -u clickexpress -f`
- Nginx logs: `/var/log/nginx/`
- System logs: `/var/log/syslog`

### Performance Monitoring
- CPU usage: `htop`
- Memory usage: `free -h`
- Disk usage: `df -h`
- Network: `netstat -tulpn`

## 🔄 Updates and Maintenance

### Code Updates
```bash
# Pull latest changes
cd /home/clickexpress/click_backend
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Restart service
sudo systemctl restart clickexpress
```

### Backup Strategy
```bash
# Database backup
sudo -u postgres pg_dump clickexpress > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf click_backend_backup_$(date +%Y%m%d).tar.gz /home/clickexpress/click_backend
```

## ✅ Production Checklist

- [ ] Droplet created and configured
- [ ] DNS records added
- [ ] SSL certificate installed
- [ ] Database configured
- [ ] Email system working
- [ ] API endpoints tested
- [ ] Admin panel accessible
- [ ] Static files serving
- [ ] Security headers configured
- [ ] Monitoring set up
- [ ] Backup strategy implemented

## 🎯 Success Indicators

- ✅ API responds at `https://api.clickexpress.ae`
- ✅ Admin panel accessible
- ✅ Contact form sends emails
- ✅ SSL certificate valid
- ✅ All services running
- ✅ No error logs
- ✅ Email delivery working

Your ClickExpress API is now production-ready! 🚀
