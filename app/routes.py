from flask import render_template, request, flash, get_flashed_messages, session, redirect, url_for, abort, current_app
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from dotenv import load_dotenv
from urllib.parse import urlencode
from datetime import datetime
# from sqlalchemy import select

from app import app, db, User, Shop
from download_youtube import * 

import secrets
import requests

@app.route("/")
def homepage():
    #Might need to switch session for the same thing provided by flask_login
    if 'user' in session.keys():
        return render_template("index.html", user=session['user'])
    else:
        return render_template("index.html")

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

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template('login.html')

login = LoginManager(app)
login.login_view = 'index'

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

@app.route('/logout')
def logout():
    logout_user()
    session.pop('user')
    flash('You have been logged out.')
    return redirect(url_for('homepage'))


@app.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('homepage'))

    provider_data = current_app.config['OAUTH_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('oauth2_callback', provider=provider,
                                _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data['authorize_url'] + '?' + qs)


@app.route('/complete_sign_in/<provider>')
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('homepage'))

    provider_data = current_app.config['OAUTH_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # if there was an authentication error, flash the error messages and exit
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('homepage'))

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    # make sure that the authorization code is present
    if 'code' not in request.args:
        abort(401)

    # exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('oauth2_callback', provider=provider,
                                _external=True),
    }, headers={'Accept': 'application/json'})
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    # use the access token to get the user's email address
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    if response.status_code != 200:
        abort(401)
    email = provider_data['userinfo']['email'](response.json())
    print(email)
    # find or create the user in the database
    user = db.session.scalar(db.select(User).where(User.email == email))
    if user is None:
        user = User(email=email, username=email.split('@')[0])
        db.session.add(user)
        db.session.commit()

    # log the user in
    login_user(user)
    #pass the username to session
    record = User.query.filter_by(email=email).first()
    session['user'] = record.username
    return redirect(url_for('homepage'))

# @app.route("/shop_button", methods=["POST"])
# def shop_button():
#     new_click = Shop(datetime=datetime.utcnow(), click='1')
#     db.session.add(new_click)
#     db.session.commit()
#     flash('Shop button was clicked')
#     return render_template('storefront.html')

@app.route("/shop", methods=["GET", "POST"])
def shop():
    new_click = Shop(datetime=datetime.utcnow(), click='1')
    db.session.add(new_click)
    db.session.commit()
    return render_template('storefront.html')

@app.route("/display-page", methods=["GET", "POST"])
def display_page():
    return render_template('display-page.html')

# OLD

# class convert_to_dot_notation(dict):
# """
# Access dictionary attributes via dot notation
# """

# __getattr__ = dict.get
# __setattr__ = dict.__setitem__
# __delattr__ = dict.__delitem__


# @app.route("/magic_link_login", methods=["POST"])
# def magic_link_login():
#     if ('user' in session):
#         return f'<p>Hi, {session["user"]}</p>'
#     if request.method == "POST":
#         email = request.form.get('email')
#         print(f'email: {email}, file=sys.stderr)')
#         action_code_settings = {
#             'url': 'http://localhost:8080/complete_sign_in'
#             }
#         action_code_settings = convert_to_dot_notation(action_code_settings)
#         try:
#             link = auth.auth.generate_sign_in_with_email_link(email, action_code_settings)
#             print(f'email: {email}')
#             # session['user'] = email
#             response = f"""
#             <p class="fade-in-text">Check your email for a sign in link! \n {link}</p>
#             """
#             return response
#         except Exception as e:
#             return f'Login failed: {e}'

# @app.route('/complete_sign_in', methods=['GET'])
# def complete_sign_in():
#     email = request.args.get('email')
#     link = request.args.get('link')
                            
#     try:
#         # Verify the link and sign in the user
#         # This would typically be part of your client-side logic
#         # Here, for simplicity, we're just verifying the link
#         #result = auth.auth.sign_in_with_email_link(email, link)
#         return f'Successfully logged in. Redirecting you to the homepage.'
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

#@app.route("/login", methods=["GET", "POST"])
# def login():
#     if ('user' in session):
#         return f'<p>Hi, {session["user"]}</p>'
#     if request.method == "POST":
#         email = request.form.get('email')
#         password = request.form.get('password')
#         try:
#             user = auth.auth.create_user_with_email_and_password(email, password)
#             session['user'] = email
#             return render_template('index.html', user=session['user'])
#         except:
#             try:
#                 user = auth.auth.sign_in_with_email_and_password(email,password)
#                 # auth.auth.sign_in_with_email_and_password(email, password)
#                 session['user'] = email
#                 return render_template('index.html', user=session['user'])
            
#             except Exception as e:
#                 e = str(e)
#                 if 'INVALID_PASSWORD' in e:
#                     flash('Inccorect password. Please try again.')
#                     return render_template('login.html')
#                 else:
#                     return f'Login failed due to unknown reason'
#     return render_template('login.html')
