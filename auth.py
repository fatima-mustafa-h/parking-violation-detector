from flask import Blueprint, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import auth, credentials
import json
import os

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')

firebase_app = None

def init_firebase():
    global firebase_app
    cred_path = os.path.join(os.path.dirname(__file__), 'firebase_config.json')
    cred = credentials.Certificate(cred_path)
    firebase_app = firebase_admin.initialize_app(cred)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = firebase_admin.auth.get_user_by_email(email)
            # Firebase does not verify password server-side; use Firebase client SDK or custom auth.
            # For demonstration, accept any existing user.
            session['user'] = user.uid
            return redirect(url_for('dashboard'))
        except Exception:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.create_user(email=email, password=password)
            return redirect(url_for('auth.login'))
        except Exception as e:
            return render_template('register.html', error=str(e))
    return render_template('register.html')

@auth_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

