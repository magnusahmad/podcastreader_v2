from flask import session, request, redirect
import pyrebase 
import app

config = {   'apiKey': "AIzaSyA5tPUV7Xfg3KdQDjTy9hsVhBLjZWgEiaM",
    'authDomain': "podcastreader-7e348.firebaseapp.com",
    'projectId': "podcastreader-7e348",
    'storageBucket': "podcastreader-7e348.appspot.com",
    'messagingSenderId': "482563787442",
    'appId': "1:482563787442:web:682fb4c900daa880bf97ab",
    'databaseURL': ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
app.secret_key = 'secret'
