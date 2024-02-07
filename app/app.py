from flask import Flask, session, request, redirect, render_template
from flask_assets import Bundle, Environment
from flask_sqlalchemy import SQLAlchemy
import pyrebase 
import os
from dotenv import load_dotenv
### !!changed to download_youtube_notranscribe to test deployment without whisper!! ###

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('CSRF_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

# import json
# cur_path = os.getcwd()
# csrf_path = os.path.relpath('./credentials/csrf_key.json', cur_path)
# sql_path = os.path.relpath('./credentials/sqlalchemy_uri.json', cur_path)

# with open(csrf_path) as csrf:
#     data = json.load(csrf)
#     app.config['SECRET_KEY'] = data['CSRF_SECRET_KEY']

# with open(sql_path) as sql:
#     data = json.load(sql)
#     app.config['SQLALCHEMY_DATABASE_URI'] = data['SQLALCHEMY_DATABASE_URI']

db = SQLAlchemy(app)

# app.config['SECRET_KEY'] = os.getenv('csrf_key')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('sqlalchemy_uri')
# db = SQLAlchemy(app)

# db = SQLAlchemy(app)

app.app_context().push()

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

from routes import *

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    # import json
    # cur_path = os.getcwd()
    # new_path = os.path.relpath('./credentials/openai_key.json', cur_path)

    # with open(new_path) as f:
    #     credentials = json.load(f)
    # file = input('Enter filename: ')
    # whisper_transcribe(file)