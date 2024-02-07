from flask import render_template, request, flash, get_flashed_messages, session, redirect, url_for
import firebase_admin
from firebase_admin import credentials, auth
from app import app, db
from download_youtube import * 
from models import Shop_Button
from datetime import datetime
import auth
import jsonify

class convert_to_dot_notation(dict):
    """
    Access dictionary attributes via dot notation
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

@app.route("/")
def homepage():
    if 'user' in session.keys():
        return render_template("index.html", user=session['user'])
    else:
        return render_template("index.html")

@app.route("/shop_button", methods=["POST"])
def shop_button():
    new_click = Shop_Button(date=datetime.utcnow(), click='1')
    db.session.add(new_click)
    db.session.commit()
    flash('Shop button was clicked')

@app.route("/submit", methods=["POST"])
def submit():
    url = request.form["url"]
    email = request.form["email"]
    try:
        download_youtube(url, email)
        response = f"""
        <p class="fade-in-text">Your submission has been received. You will receive your new ebook at {email} in some minutes...</p>
        """
    except Exception as e:
        print(f'Exception: {e}')
        response = f"""
        <p class="fade-in-text">That didn't work. Please refresh the page and try again.</p>
        """
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    if ('user' in session):
        return f'<p>Hi, {session["user"]}</p>'
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.auth.create_user_with_email_and_password(email, password)
            session['user'] = email
            return render_template('index.html', user=session['user'])
        except:
            try:
                user = auth.auth.sign_in_with_email_and_password(email,password)
                # auth.auth.sign_in_with_email_and_password(email, password)
                session['user'] = email
                return render_template('index.html', user=session['user'])
            
            except Exception as e:
                e = str(e)
                if 'INVALID_PASSWORD' in e:
                    flash('Inccorect password. Please try again.')
                    return render_template('login.html')
                else:
                    return f'Login failed due to unknown reason'
    return render_template('login.html')

cred = credentials.Certificate('podcastreader-firebase-key.json')
# firebase_admin.initialize_app(cred)

@app.route("/magic_link_login", methods=["POST"])
def magic_link_login():
    if ('user' in session):
        return f'<p>Hi, {session["user"]}</p>'
    if request.method == "POST":
        email = request.form.get('email')
        print(f'email: {email}, file=sys.stderr)')
        action_code_settings = {
            'url': 'http://localhost:8080/complete_sign_in'
            }
        action_code_settings = convert_to_dot_notation(action_code_settings)
        try:
            link = auth.auth.generate_sign_in_with_email_link(email, action_code_settings)
            print(f'email: {email}')
            # session['user'] = email
            response = f"""
            <p class="fade-in-text">Check your email for a sign in link! \n {link}</p>
            """
            return response
        except Exception as e:
            return f'Login failed: {e}'

@app.route('/complete_sign_in', methods=['GET'])
def complete_sign_in():
    email = request.args.get('email')
    link = request.args.get('link')
                            
    try:
        # Verify the link and sign in the user
        # This would typically be part of your client-side logic
        # Here, for simplicity, we're just verifying the link
        #result = auth.auth.sign_in_with_email_link(email, link)
        return f'Email: {email} \n Link: {link}'
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    