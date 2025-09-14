import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid
from jinja2 import Environment, FileSystemLoader
from config import EMAIL_CONFIG, BASE_DIR

class EmailService:
    def __init__(self):
        self.smtp_server = EMAIL_CONFIG["SMTP_SERVER"]
        self.smtp_port = EMAIL_CONFIG["SMTP_PORT"]
        self.smtp_username = EMAIL_CONFIG["SMTP_USERNAME"]
        self.smtp_password = EMAIL_CONFIG["SMTP_PASSWORD"]
        self.from_email = EMAIL_CONFIG["FROM_EMAIL"]
        self.from_name = EMAIL_CONFIG["FROM_NAME"]
        
        # Set up Jinja2 environment for email templates
        template_dir = os.path.join(BASE_DIR, "templates")
        os.makedirs(template_dir, exist_ok=True)
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
        # Create default meeting invitation template if it doesn't exist
        self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default email templates if they don't exist"""
        template_dir = os.path.join(BASE_DIR, "templates")
        os.makedirs(template_dir, exist_ok=True)
        
        # Create meeting invitation template
        meeting_template = os.path.join(template_dir, "meeting_invitation.html")
        if not os.path.exists(meeting_template):
            with open(meeting_template, 'w') as f:
                f.write("""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Meeting Invitation: {{ meeting_title }}</title>
                </head>
                <body>
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <h2>You're Invited: {{ meeting_title }}</h2>
                        <p>Hello,</p>
                        <p>You have been invited to a meeting with the following details:</p>
                        
                        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p><strong>Title:</strong> {{ meeting_title }}</p>
                            <p><strong>Date & Time:</strong> {{ start_time }} - {{ end_time }}</p>
                            <p><strong>Description:</strong> {{ description or 'No description provided' }}</p>
                            <p><strong>Meeting Link:</strong> <a href="{{ meeting_link }}" target="_blank">Join Meeting</a></p>
                        </div>
                        
                        <p>Please join the meeting on time. If you have any questions, feel free to reply to this email.</p>
                        
                        <p>Best regards,<br>{{ organizer_name }}</p>
                        
                        <div style="margin-top: 30px; font-size: 12px; color: #777;">
                            <p>This is an automated message. Please do not reply directly to this email.</p>
                        </div>
                    </div>
                </body>
                </html>
                """)
    
    def _render_template(self, template_name, **context):
        """Render a template with the given context"""
        template = self.env.get_template(template_name)
        return template.render(**context)
    
    def send_email(self, to_emails, subject, html_content, text_content=None):
        """
        Send an email with HTML content
        
        Args:
            to_emails (list): List of recipient email addresses
            subject (str): Email subject
            html_content (str): HTML content of the email
            text_content (str, optional): Plain text version of the email
        """
        if isinstance(to_emails, str):
            to_emails = [to_emails]
        
        # Create message container
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{self.from_name} <{self.from_email}>"
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)
        msg['Message-ID'] = make_msgid()
        
        # Attach parts (plain text and HTML)
        if text_content:
            part1 = MIMEText(text_content, 'plain')
            msg.attach(part1)
        
        part2 = MIMEText(html_content, 'html')
        msg.attach(part2)
        
        # Send the email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
    
    def send_meeting_invitation(self, to_emails, meeting_details, organizer_name=None):
        """
        Send a meeting invitation email
        
        Args:
            to_emails (list): List of recipient email addresses
            meeting_details (dict): Dictionary containing meeting details
            organizer_name (str, optional): Name of the meeting organizer
        """
        if organizer_name is None:
            organizer_name = self.from_name
        
        # Render the email template
        html_content = self._render_template(
            "meeting_invitation.html",
            meeting_title=meeting_details.get('summary', 'Meeting Invitation'),
            start_time=meeting_details.get('start_time'),
            end_time=meeting_details.get('end_time'),
            description=meeting_details.get('description', ''),
            meeting_link=meeting_details.get('meet_link', '#'),
            organizer_name=organizer_name
        )
        
        # Create a plain text version of the email
        text_content = f"""
        Meeting Invitation: {meeting_details.get('summary', 'Meeting Invitation')}
        
        You have been invited to a meeting with the following details:
        
        Title: {meeting_details.get('summary', 'Meeting')}
        Date & Time: {meeting_details.get('start_time')} - {meeting_details.get('end_time')}
        Description: {meeting_details.get('description', 'No description provided')}
        Meeting Link: {meeting_details.get('meet_link', 'No link provided')}
        
        Best regards,
        {organizer_name}
        """
        
        # Send the email
        self.send_email(
            to_emails=to_emails,
            subject=f"Meeting Invitation: {meeting_details.get('summary', 'Meeting')}",
            html_content=html_content,
            text_content=text_content
        )
