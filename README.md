# Secure Authentication System Development

## Overview  

This project aims to develop a secure login system with two-factor authentication (2FA) using email and OTP (One-Time Password). It enhances user security by requiring both a password and a time-sensitive OTP sent to the user's email for login.


## Technologies Used  

- **Programming Language:** Python 3.8+  
- **Web Framework:** Flask  
- **Database:** SQLite  
- **Email Service:** smtplib for sending emails  
- **Frontend:** HTML/CSS (Bootstrap optional for styling)  


## Setup Instructions  

### 1. Prerequisites  
- Python 3.8+ installed on your system.  
- SMTP server credentials (e.g., Gmail) for sending emails.  
- Virtual environment (recommended for dependencies).

### 2. Installation  
1. Clone the repository to your local machine:
   ```bash
   git clone <your-repo-link>
   cd <your-repo-directory>
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
3. Install the required packages:
   ```bash
   pip install Flask bcrypt
4. Configure the SMTP settings in app.py:
   ```pyhton
   SMTP_SERVER = 'smtp.gmail.com'
   SMTP_PORT = 587
   EMAIL_ADDRESS = 'your-email@gmail.com'
   EMAIL_PASSWORD = 'your-app-password'


## How to Run the Application

1. Initialize the SQLite database:
   ```bash
   python init_db.py
2. Start the Flask server:
   ```bash
   flask run
3. Open your browser and go to http://127.0.0.1:5000/.


## Current Functionalities (Phase 1)

### 1. User Registration:  
- Collects username, password, and email address.
- Passwords are securely hashed using bcrypt.  
-Sends an email confirmation link for verification.

### 2. User Login:
  
- Authenticates users with a username and password.
- Checks if the user has verified their email.


## Known Issues or Limitations
- **OTP-based authentication** is not yet implemented and will be added in the next phase.
- Error handling needs further refinement to enhance the user experience.


## Next Steps
- Implement OTP generation and email delivery for 2FA.
- Introduce rate limiting to prevent brute-force attacks.
- Add Bootstrap styling for improved UI.
