import requests
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)


class MailgunService:
    """
    Mailgun email service for sending emails
    """
    
    def __init__(self):
        self.api_key = getattr(settings, 'MAILGUN_API_KEY', None)
        self.domain = getattr(settings, 'MAILGUN_DOMAIN', None)
        self.from_email = getattr(settings, 'MAILGUN_FROM_EMAIL', 'noreply@clickexpress.com')
    
    def send_email(self, to_email, subject, html_content, text_content=None):
        """
        Send email via Mailgun API
        """
        if not self.api_key or not self.domain:
            logger.error("Mailgun API key or domain not configured")
            return False
        
        url = f"https://api.mailgun.net/v3/{self.domain}/messages"
        
        data = {
            "from": self.from_email,
            "to": to_email,
            "subject": subject,
            "html": html_content,
        }
        
        if text_content:
            data["text"] = text_content
        
        try:
            response = requests.post(
                url,
                auth=("api", self.api_key),
                data=data
            )
            
            if response.status_code == 200:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def send_contact_notification(self, contact_message):
        """
        Send notification email to admin about new contact message
        """
        admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@clickexpress.com')
        
        subject = f"New Contact Message: {contact_message.subject}"
        
        html_content = f"""
        <h2>New Contact Message</h2>
        <p><strong>Name:</strong> {contact_message.name}</p>
        <p><strong>Email:</strong> {contact_message.email}</p>
        <p><strong>Phone:</strong> {contact_message.phone or 'Not provided'}</p>
        <p><strong>Subject:</strong> {contact_message.subject}</p>
        <p><strong>Message:</strong></p>
        <p>{contact_message.message}</p>
        <hr>
        <p><em>Received at: {contact_message.created_at}</em></p>
        """
        
        return self.send_email(admin_email, subject, html_content)
    
    def send_contact_confirmation(self, contact_message):
        """
        Send confirmation email to user
        """
        subject = "Thank you for contacting ClickExpress"
        
        html_content = f"""
        <h2>Thank you for contacting us!</h2>
        <p>Dear {contact_message.name},</p>
        <p>We have received your message and will get back to you as soon as possible.</p>
        <p><strong>Your message:</strong></p>
        <p><em>{contact_message.message}</em></p>
        <hr>
        <p>Best regards,<br>ClickExpress Team</p>
        """
        
        return self.send_email(contact_message.email, subject, html_content)
    
    def send_newsletter_confirmation(self, email):
        """
        Send newsletter subscription confirmation
        """
        subject = "Welcome to ClickExpress Newsletter"
        
        html_content = f"""
        <h2>Welcome to ClickExpress!</h2>
        <p>Thank you for subscribing to our newsletter.</p>
        <p>You will receive updates about our latest services and news.</p>
        <hr>
        <p>Best regards,<br>ClickExpress Team</p>
        """
        
        return self.send_email(email, subject, html_content)


# Fallback email service using Django's built-in email
class DjangoEmailService:
    """
    Fallback email service using Django's built-in email
    """
    
    def send_contact_notification(self, contact_message):
        """
        Send notification email to admin using Django's email
        """
        admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@clickexpress.com')
        
        subject = f"New Contact Message: {contact_message.subject}"
        message = f"""
        New Contact Message:
        
        Name: {contact_message.name}
        Email: {contact_message.email}
        Phone: {contact_message.phone or 'Not provided'}
        Subject: {contact_message.subject}
        
        Message:
        {contact_message.message}
        
        Received at: {contact_message.created_at}
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [admin_email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def send_contact_confirmation(self, contact_message):
        """
        Send confirmation email to user using Django's email
        """
        subject = "Thank you for contacting ClickExpress"
        message = f"""
        Dear {contact_message.name},
        
        Thank you for contacting us! We have received your message and will get back to you as soon as possible.
        
        Your message:
        {contact_message.message}
        
        Best regards,
        ClickExpress Team
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [contact_message.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
