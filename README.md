# Jovian Job Offerings CRUD Application

## Overview
This is a Flask-based CRUD (Create, Read, Update, Delete) application for managing job offerings at a company called Jovian. The application connects to a MySQL database hosted on [Aiven](https://aiven.io/) and provides functionalities to view job listings, apply for jobs, and manage applications. Additionally, it integrates hCaptcha for form validation and sends email notifications upon successful job applications.

## Features
- **Job Listings**: View all available job positions at Jovian.
- **Job Application**: Apply for a specific job position.
- **Admin Features**: View and manage job applications.
- **Email Notifications**: Sends a confirmation email to the applicant upon successful application submission.
- **hCaptcha Integration**: Adds an extra layer of security by validating user interactions.

## Prerequisites
- Python 3.7+
- MySQL database
- Flask
- hCaptcha account
<!-- - MailerSend account for sending emails -->

## Installation

1. **Clone the repository**
    ```sh
    git clone -b master https://github.com/senaditya/jovian-v2
    cd jovian-v2
    ```

2. **Create a virtual environment and activate it**
    ```sh
    python3 -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**
    Create a `.env` file in the project root directory and add the following environment variables:
    ```
    DB_SECRET=your_database_connection_string
    SMTP_USER=your_smtp_username
    SMTP_PASS=your_smtp_password
    MAIL_FROM=your_email_address
    CAPTCHA_SITEKEY=your_hcaptcha_site_key
    CAPTCHA_SECRET=your_hcaptcha_secret_key
    ```

5. **Run the application**
    ```sh
    flask --app index run
    ```

## Application Structure
- `index.py`: The main Flask application file.
- `templates/`: Directory containing HTML templates.
- `static/`: Directory containing static files like CSS, JavaScript, and images.
- `requirements.txt`: Python dependencies.
- `.env`: File containing environment variables.

## Key Functions and Routes

### Email Function
Responsible for sending email notifications.
```python
def send_email(receiver_email, subject, message):
    # Email sending logic
```

### Database Functions
Functions to load and manage jobs and applications from the database.
```python
def load_jobs():
    # Fetch all job listings

def load_job(id):
    # Fetch a specific job by ID

def application(jobId, data):
    # Process a job application

def load_applications():
    # Load all applications

def load_application(jobId):
    # Load application for a specific job ID
```

### Routes
- `/`: Home page displaying job listings.
- `/api/jobs`: API endpoint to list all jobs.
- `/api/jobs/<id>`: API endpoint to fetch a specific job by ID.
- `/api/applications`: API endpoint to list all applications.
- `/api/applications/<jobId>`: API endpoint to fetch applications for a specific job ID.
- `/job/<id>`: Web page to view a specific job.
- `/job/<id>/apply`: Web page to apply for a specific job (POST request).

### Error Handlers
Custom error handlers for different HTTP status codes.
```python
@app.errorhandler(404)
def not_found_error(error):
    # Handle 404 errors

@app.errorhandler(500)
def internal_server_error(error):
    # Handle 500 errors

@app.errorhandler(400)
def bad_request_error(error):
    # Handle 400 errors

@app.errorhandler(405)
def method_not_allowed(error):
    # Handle 405 errors
```

## Usage
- **Viewing Jobs**: Navigate to the home page to see all job listings.
- **Applying for a Job**: Click on a job to view details and apply.
- **Managing Applications**: Admins can view all applications through the provided API endpoints.

## Security
- **hCaptcha**: Used to prevent spam and abuse on the application form.
- **Email Verification**: Sends a confirmation email to verify the application submission.

## Troubleshooting
- Ensure all environment variables are correctly set in the `.env` file.
- Check database connectivity and credentials.
- Verify SMTP settings for email notifications.
- Use `flask run` with `debug=True` during development to see detailed error messages.

## Contributing
Feel free to open issues or submit pull requests for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

By following this README, you should be able to set up and run the Jovian Job Offerings CRUD application locally. For any issues, refer to the troubleshooting section or open an issue on the project's GitHub repository.
