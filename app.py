from flask import Flask, render_template, redirect, request, flash, url_for
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
  if "youtu.be" or "youtube.com" in url:
    for f in info["formats"]:
      if f.get("acodec") != "none":
        formats.append({
          "format_id": f["format_id"],
          'ext': f['ext'],
          'resolution': f.get("resolution"),
          "height": f.get("height"),
          "filesize": round((f.get('filesize') or 0)/(1024*1024), 2),
          "url": f.get('url'),
        })
  elif "facebook.com" or "instagram.com" in url:
    for f in info['formats']:
        if f.get('ext') == 'mp4' and f.get('url'):
            formats.append({
                'format_id': f['format_id'],
                'resolution': f.get('resolution'),
                'url': f.get('url'),
                'ext': f['ext'],
                "filesize": round((f.get('filesize') or 0)/(1024*1024), 2),
            })

  return {
    "title": info['title'] or None,
    "thumbnail": info["thumbnail"] or None,
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
    'format': "best",
    'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
    'cookiefile': 'cookies.txt',
  }
  
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
  flash("Download started successfully!")

  return redirect(url_for('downloading'))

@app.route('/downloading', methods=['GET', 'POST'])
def downloading():
  return render_template('downloading.html')


@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact')
def contact():
  return render_template('contact.html')

@app.route('/privacy')
def privacy():
  return render_template('privacy.html')

@app.route('/terms')
def terms():
  return render_template('terms.html')


if __name__ == "__main__":
  app.run(debug=True)