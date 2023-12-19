from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from download_youtube_notranscribe import * 
### !!changed to download_youtube_notranscribe to test deployment without whisper!! ###

app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

@app.route("/")
def homepage():
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

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))