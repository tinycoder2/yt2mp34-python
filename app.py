from flask import Flask, render_template, request,redirect, url_for
from pytube import YouTube
from pathlib import Path
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from dominate.tags import img
import os, waitress


logo = img(src="https://img.icons8.com/external-soft-fill-juicy-fish/30/000000/external-convert-user-interface-design-soft-fill-soft-fill-juicy-fish.png", height="50", width="50", style="margin-top:-15px")

topbar = Navbar(logo,
                View('Home', 'home'),
                View('About Me', 'aboutMe'),
                )

# registers the "top" menubar
nav = Nav()
nav.register_element('top', topbar)

app = Flask(__name__)
Bootstrap(app)

@app.route('/aboutMe')
def aboutMe():
    return render_template("about_me.html")

@app.route('/to_mp4', methods = ['GET','POST'])
def toMp4():
    if request.method == 'POST':
        url = request.form['url']
        try:
            obj=YouTube(url)
        except Exception as error:
            return_message = "Error : " + str(error) + " Try again!"
            return render_template("to_mp4.html",return_message=return_message)
        else:
            downloadFolder = str(Path.home() / "Downloads")
            stream = obj.streams.get_highest_resolution()
            stream.download(downloadFolder)
            return redirect(url_for('success'))
    else:
      return render_template("to_mp4.html")

@app.route('/to_mp3', methods = ['GET','POST'])
def toMp3():
    if request.method == 'POST':
        url = request.form['url']
        try:
            yt = YouTube(url)
        except Exception as error:
            return_message = "Error : " + str(error) + " Try again !"
            return render_template("to_mp3.html",return_message=return_message)
        else:
            video = yt.streams.filter(only_audio=True).first()
            downloadFolder = str(Path.home() / "Downloads")
            out_file = video.download(output_path=downloadFolder)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            return redirect(url_for('success'))
    else:
      return render_template("to_mp3.html")


@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/")
def home():
    return render_template("index.html")



nav.init_app(app)
if __name__ == '__main__':
    app.debug = False
    port=int(os.environ.get('PORT', 33507))
    waitress.serve(app, port=port)
#    app.run()
