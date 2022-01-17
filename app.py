from flask import Flask, render_template, request,redirect, url_for
from pytube import YouTube
from pathlib import Path

app = Flask(__name__)


def ytConv(url):
    downloadFolder = str(Path.home() / "Downloads")
    print(downloadFolder)
    print(url)
    # url="https://youtu.be/vV9gkIFxD54"
    obj=YouTube(url)
    stream = obj.streams.get_highest_resolution()
    stream.download(downloadFolder)
    print("downloaded")

@app.route('/form')
def form():
   return render_template("get_url.html")


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
    return "Hello, Flask!"

if __name__ == '__main__':
   app.run()
