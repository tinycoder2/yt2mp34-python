from flask import Flask, render_template, request,redirect, url_for
from pytube import YouTube
from pathlib import Path
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from dominate.tags import img



logo = img(src='./static/img/forg.png', height="50", width="50", style="margin-top:-15px")

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
    return redirect("https://tinycoder2.github.io/pimbuOS/")

def ytConv(url):
    downloadFolder = str(Path.home() / "Downloads")
    print(downloadFolder)
    print(url)
    # url="https://youtu.be/vV9gkIFxD54"
    obj=YouTube(url)
    stream = obj.streams.get_highest_resolution()
    stream.download(downloadFolder)
    print("downloaded")

# @app.route('/form')
# def form():
#    return render_template("get_url.html")


@app.route('/get_Input', methods = ['GET','POST'])
def getInput():
    if request.method == 'POST':
        url = request.form['url']
        try:
            ytConv(url)
            return redirect(url_for('home'))
        except Exception as error:
            return_message = str(error)
            return(return_message)
    else:
      return render_template("get_url.html")


@app.route("/")
def home():
    return render_template("index.html")


nav.init_app(app)
if __name__ == '__main__':
   app.run()
