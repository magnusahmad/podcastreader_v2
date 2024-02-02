from flask import render_template, request, flash, get_flashed_messages, session, redirect, url_for
from app import app, db
from download_youtube import * 
from models import Shop_Button
from datetime import datetime
import auth

@app.route("/")
def homepage():
    if session['user']:
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