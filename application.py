from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os
from datetime import datetime
import logging
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(subject, body, to_email):
    """Simple email function without Flask-Mail"""
    try:
        smtp_server = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('MAIL_PORT', 587))
        username = os.environ.get('MAIL_USERNAME')
        password = os.environ.get('MAIL_PASSWORD')
        
        if not all([username, password]):
            logger.warning("Email credentials not configured")
            return False
            
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return False

@app.route('/')
def home():
    """Home page with hero section and overview"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page with therapist information"""
    return render_template('about.html')

@app.route('/services')
def services():
    """Services page with detailed offerings"""
    return render_template('services.html')

@app.route('/contact')
def contact():
    """Contact page with form"""
    return render_template('contact.html')

@app.route('/book-appointment')
def book_appointment():
    """Booking page optimized for Google Ads conversions"""
    return render_template('book_appointment.html')

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    """Handle contact form submission"""
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service = request.form.get('service')
        message = request.form.get('message')
        
        # Validate required fields
        if not all([name, email, message]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('contact'))
        
        # Send email notification
        email_body = f"""
        New contact form submission:
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        Service Interest: {service}
        Message: {message}
        
        Submitted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        recipient = os.environ.get('MAIL_USERNAME')
        email_sent = send_email(f'New Contact Form Submission from {name}', email_body, recipient)
        
        if email_sent:
            logger.info(f'Contact form submitted by {name} ({email})')
        
        flash('Thank you for your message! We\'ll get back to you soon.', 'success')
        
        # Track conversion for Google Ads
        return render_template('contact_success.html', name=name)
        
    except Exception as e:
        logger.error(f'Error processing contact form: {str(e)}')
        flash('Sorry, there was an error sending your message. Please try again.', 'error')
        return redirect(url_for('contact'))

@app.route('/api/track-conversion', methods=['POST'])
def track_conversion():
    """API endpoint for tracking Google Ads conversions"""
    try:
        conversion_data = request.get_json()
        # Log conversion for analytics
        logger.info(f'Conversion tracked: {conversion_data}')
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f'Error tracking conversion: {str(e)}')
        return jsonify({'status': 'error'}), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Production server
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=False, host='0.0.0.0', port=port)