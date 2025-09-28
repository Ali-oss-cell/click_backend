# Mailgun Setup Guide for ClickExpress API

## 📧 Step-by-Step Mailgun Configuration

### 1. Get Your Mailgun Credentials

#### From Mailgun Dashboard:
1. **API Key:**
   - Go to Settings → API Keys
   - Copy your **Private API Key** (starts with `key-`)

2. **Domain:**
   - Go to Sending → Domains  
   - Copy your **Domain Name** (e.g., `mg.yourdomain.com`)

### 2. Create .env File

Create a `.env` file in your project root with these values:

```env
DEBUG=True
SECRET_KEY=django-insecure-o@3c4b017jo&jubwo$%m-w44)f+-ap-)b+=#ol85_l$4tiur+a
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
JWT_SECRET=supersecretjwtkey
JWT_EXPIRES_IN=86400

# Email Configuration
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com

# Mailgun Configuration - REPLACE WITH YOUR ACTUAL VALUES
MAILGUN_API_KEY=your-mailgun-private-api-key-here
MAILGUN_DOMAIN=mg.yourdomain.com
MAILGUN_FROM_EMAIL=noreply@yourdomain.com
```

### 3. Replace the Placeholder Values

Replace these with your actual Mailgun values:
- `your-mailgun-private-api-key-here` → Your actual API key
- `mg.yourdomain.com` → Your actual Mailgun domain
- `yourdomain.com` → Your actual domain

### 4. Test Email Functionality

#### Option A: Test via API
```bash
# Test contact form
curl -X POST http://127.0.0.1:8000/api/v1/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test Message",
    "message": "This is a test message"
  }'
```

#### Option B: Test via Postman
1. Import the `ClickExpress_API.postman_collection.json`
2. Use the contact form endpoints
3. Check your email for notifications

### 5. Verify Email Settings

#### Check Django Settings:
```python
# In clickexpress_api/settings.py, verify these are set:
MAILGUN_API_KEY = config('MAILGUN_API_KEY', default='')
MAILGUN_DOMAIN = config('MAILGUN_DOMAIN', default='')
MAILGUN_FROM_EMAIL = config('MAILGUN_FROM_EMAIL', default='noreply@clickexpress.com')
```

### 6. Email Flow Testing

#### What Should Happen:
1. **User submits contact form** → API receives data
2. **Admin notification email** → Sent to your admin email
3. **User confirmation email** → Sent to user's email
4. **Newsletter signup** → Confirmation email sent

### 7. Troubleshooting

#### Common Issues:
- **API Key Error:** Check if API key is correct
- **Domain Error:** Verify domain is properly configured in Mailgun
- **Email Not Sending:** Check Mailgun logs in dashboard
- **Permission Error:** Ensure API key has sending permissions

#### Debug Mode:
```python
# In settings.py, temporarily add:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# This will print emails to console instead of sending
```

### 8. Production Setup

#### For Production:
1. **Verify your domain** in Mailgun
2. **Set up DNS records** as instructed by Mailgun
3. **Use HTTPS** for your API
4. **Set proper CORS** origins
5. **Use environment variables** for security

### 9. Email Templates (Optional)

You can customize email templates by modifying:
- `contact/email_service.py` - Email content
- Add HTML templates in `contact/templates/`

### 10. Monitoring

#### Check Mailgun Dashboard:
- **Sending** → **Logs** - See email delivery status
- **Analytics** - Track email performance
- **Suppressions** - Manage bounced emails

## 🎯 Next Steps

1. **Set up your .env file** with actual Mailgun credentials
2. **Test the contact form** using Postman or curl
3. **Check your email** for notifications
4. **Verify both admin and user emails** are working
5. **Deploy to production** when ready

## 📞 Support

If you encounter issues:
1. Check Mailgun dashboard for delivery logs
2. Verify API key and domain settings
3. Test with console email backend first
4. Check Django logs for error messages
