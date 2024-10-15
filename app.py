from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_bcrypt import Bcrypt
from email_validator import validate_email, EmailNotValidError
import sqlite3, smtplib, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # For session management
bcrypt = Bcrypt(app)

# Email Configuration (use your credentials)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'your-email@gmail.com'
EMAIL_PASSWORD = 'your-email-password'

# Database setup (Creates the table if it doesn't exist)
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            confirmed INTEGER DEFAULT 0
        )''')

# Email confirmation function
def send_confirmation_email(email):
    confirmation_link = f"http://127.0.0.1:5000/confirm_email?email={email}"
    message = f"Subject: Confirm your Email\n\nClick the link to confirm: {confirmation_link}"
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, message)

# Route: User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            validate_email(email)  # Validate email format
        except EmailNotValidError as e:
            flash(str(e), 'error')
            return render_template('register.html')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            with sqlite3.connect('database.db') as conn:
                conn.execute(
                    'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                    (username, email, hashed_password)
                )
            send_confirmation_email(email)  # Send email confirmation
            flash('Registration successful! Check your email to confirm.', 'info')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists.', 'error')

    return render_template('register.html')

# Route: Confirm Email
@app.route('/confirm_email')
def confirm_email():
    email = request.args.get('email')
    with sqlite3.connect('database.db') as conn:
        conn.execute('UPDATE users SET confirmed = 1 WHERE email = ?', (email,))
    flash('Email confirmed! You can now log in.', 'success')
    return redirect(url_for('login'))

# Route: User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('database.db') as conn:
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user and bcrypt.check_password_hash(user[3], password):
            if user[4] == 1:  # Check if email is confirmed
                session['user_id'] = user[0]
                flash('Login successful! OTP will be implemented in the next phase.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Please confirm your email before logging in.', 'error')
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')

# Route: Dashboard (Placeholder for future OTP implementation)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return 'Welcome to your dashboard! (OTP coming soon)'

# Route: Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
