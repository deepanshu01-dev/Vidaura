from flask import Flask, render_template, redirect
import yt_dlp
import os

app = Flask(__name__)
download_folder = "downloads"

if not os.path.exists(download_folder):
  os.makedirs(download_folder)

@app.route("/", methods=['GET', 'POST'])
def index():
  return render_template("index.html")



if __name__ == "__main__":
  app.run(debug=True)