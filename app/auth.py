from flask import session, request, redirect
import pyrebase 
import app
import firebase_admin
from firebase_admin import credentials, auth

# config = {   'apiKey': "AIzaSyA5tPUV7Xfg3KdQDjTy9hsVhBLjZWgEiaM",
#     'authDomain': "podcastreader-7e348.firebaseapp.com",
#     'projectId': "podcastreader-7e348",
#     'storageBucket': "podcastreader-7e348.appspot.com",
#     'messagingSenderId': "482563787442",
#     'appId': "1:482563787442:web:682fb4c900daa880bf97ab",
#     'databaseURL': ""
# }

# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()
# app.secret_key = 'secret'

cred = credentials.Certificate('podcastreader-firebase-key.json')
firebase_admin.initialize_app(cred)