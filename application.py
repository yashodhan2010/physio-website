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
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Gmail SMTP configuration
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        server.login(username, password)
        text = msg.as_string()
        server.sendmail(username, to_email, text)
        server.quit()
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

@app.route('/')
def home():
    """Home page with hero section and key services"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page with practice information"""
    return render_template('about.html')

@app.route('/services')
def services():
    """Services page with treatment options"""
    return render_template('services.html')

@app.route('/contact')
def contact():
    """Contact page with form and information"""
    return render_template('contact.html')

@app.route('/book-appointment')
def book_appointment():
    """Booking page optimized for Google Ads conversions"""
    from datetime import datetime
    today_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('book_appointment.html', today_date=today_date)

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    """Handle contact form and appointment booking submission"""
    try:
        # Debug: Log all form data
        logger.info(f"Form data received: {dict(request.form)}")
        
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service = request.form.get('service')
        message = request.form.get('message')
        
        # Check if this is an appointment booking
        is_appointment = service == 'appointment-booking'
        
        # Validate required fields
        if not all([name, email]):
            flash('Please fill in all required fields.', 'error')
            if is_appointment:
                return redirect(url_for('book_appointment'))
            return redirect(url_for('contact'))
        
        if is_appointment:
            # Validate appointment-specific required fields
            if not message:
                flash('Please describe your condition or symptoms.', 'error')
                return redirect(url_for('book_appointment'))
            
            # Handle appointment booking
            service_type = request.form.get('service-type')
            consultation_type = request.form.get('consultation-type')
            
            # Validate required appointment fields
            if not service_type:
                flash('Please select a service type.', 'error')
                return redirect(url_for('book_appointment'))
            
            if not consultation_type:
                flash('Please select a consultation type (In-Person or Video).', 'error')
                return redirect(url_for('book_appointment'))
            
            preferred_date = request.form.get('preferred-date')
            preferred_time = request.form.get('preferred-time')
            urgency = request.form.get('urgency')
            age = request.form.get('age')
            pain_level = request.form.get('pain-level')
            duration = request.form.get('duration')
            first_time = 'Yes' if request.form.get('first-time') else 'No'
            
            # Create appointment email body
            email_body = f"""
        NEW APPOINTMENT BOOKING:
        
        PERSONAL INFORMATION:
        Name: {name}
        Email: {email}
        Phone: {phone}
        Age: {age or 'Not specified'}
        
        APPOINTMENT DETAILS:
        Service Type: {service_type}
        Consultation Type: {consultation_type}
        Preferred Date: {preferred_date or 'Flexible'}
        Preferred Time: {preferred_time or 'Flexible'}
        Urgency: {urgency or 'Routine'}
        
        MEDICAL INFORMATION:
        Primary Condition: {message}
        Pain Level (1-10): {pain_level or 'Not specified'}
        Duration: {duration or 'Not specified'}
        First time seeking physiotherapy: {first_time}
        
        Submitted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        ==========================================
        Please contact the patient within 24 hours to confirm the appointment.
        """
            
            subject = f'🏥 NEW APPOINTMENT BOOKING - {name} ({consultation_type})'
            
        else:
            # Handle regular contact form
            if not message:
                flash('Please fill in all required fields.', 'error')
                return redirect(url_for('contact'))
            
            email_body = f"""
        New contact form submission:
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        Service Interest: {service}
        Message: {message}
        
        Submitted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
            
            subject = f'New Contact Form Submission from {name}'
        
        # Send email notification
        recipient = os.environ.get('MAIL_USERNAME')
        email_sent = send_email(subject, email_body, recipient)
        
        if email_sent:
            if is_appointment:
                logger.info(f'Appointment booking submitted by {name} ({email}) - {consultation_type}')
            else:
                logger.info(f'Contact form submitted by {name} ({email})')
        
        if is_appointment:
            flash('Your appointment request has been submitted! We\'ll contact you within 24 hours to confirm.', 'success')
        else:
            flash('Thank you for your message! We\'ll get back to you soon.', 'success')
        
        # Track conversion for Google Ads
        return render_template('contact_success.html', name=name, is_appointment=is_appointment)
        
    except Exception as e:
        logger.error(f'Error processing form submission: {str(e)}')
        flash('Sorry, there was an error processing your request. Please try again.', 'error')
        if request.form.get('service') == 'appointment-booking':
            return redirect(url_for('book_appointment'))
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