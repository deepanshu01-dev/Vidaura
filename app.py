from flask import Flask, render_template, redirect, request, flash
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = "toughestsecretkey2468098765"
download_folder = "downloads"

if not os.path.exists(download_folder):
  os.makedirs(download_folder)

def get_vid_info(url):
  ydl_opts = {
    "quiet": True,
    "skip_download": True,
  }
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url)
  
  formats = []
  for f in info["formats"]:
    formats.append({
      "format_id": f["format_id"],
      'ext': f['ext'],
      'resolution': f.get("resolution"),
      "height": f.get("height"),
      "filesize": round((f.get('filesize') or 0)/(1024*1024), 2),
      "url": f.get('url'),
    })

  return {
    "title": info['title'],
    "thumbnail": info["thumbnail"],
    "formats": formats
  }


@app.route("/", methods=['GET', 'POST'])
def index():
  if request.method == "POST":
    url = request.form.get("url")
    data = get_vid_info(url)
    return render_template("index.html", data=data)

  return render_template("index.html", data=None)

@app.route('/download', methods=["POST"])
def download():
  url = request.form['url']
  format_id = request.form['format_id']

  ydl_opts = {
    'format': f"{format_id}+bestaudio/best",
    'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
    'merge_output': 'mp4',
  }
  
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
  
  return "Download Started"


if __name__ == "__main__":
  app.run(debug=True)