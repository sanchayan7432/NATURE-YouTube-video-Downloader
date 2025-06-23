# from flask import Flask, request, send_file, render_template_string
# from pathlib import Path
# import yt_dlp
# import time

# app = Flask(__name__)
# VIDEOS_DIR = Path("downloads")
# VIDEOS_DIR.mkdir(exist_ok=True)

# HTML_FORM = """
# <!doctype html>
# <html>
# <head>
#   <title>Nature - YouTube Downloader</title>
#   <style>
#     body, html {
#         margin: 0;
#         padding: 0;
#         height: 100%;
#         overflow: hidden;
#         font-family: Arial, sans-serif;
#     }

#     video.bg-video {
#         position: fixed;
#         top: 0;
#         left: 0;
#         min-width: 100%;
#         min-height: 100%;
#         object-fit: cover;
#         z-index: -1;
#     }

#     .container {
#         position: absolute;
#         top: 50%;
#         left: 50%;
#         transform: translate(-50%, -50%);
#         background: rgba(0, 0, 0, 0.6);
#         backdrop-filter: blur(10px);
#         padding: 30px;
#         border-radius: 20px;
#         color: white;
#         width: 400px;
#         text-align: center;
#         box-shadow: 0 0 20px rgba(0,0,0,0.8);
#     }

#     h2 {
#         font-size: 28px;
#         margin-bottom: 15px;
#     }

#     input, select {
#         width: 100%;
#         padding: 12px;
#         margin: 10px 0;
#         border-radius: 8px;
#         border: none;
#         font-size: 14px;
#     }

#     button {
#         padding: 12px;
#         width: 100%;
#         background: #28a745;
#         color: white;
#         border: none;
#         border-radius: 8px;
#         font-size: 16px;
#         cursor: pointer;
#     }

#     button:hover {
#         background: #218838;
#     }
#   </style>
# </head>
# <body>
#   <video class="bg-video" autoplay muted loop playsinline>
#     <source src="/static/vid1.mp4" type="video/mp4">
#     Your browser does not support the video tag.
#   </video>

#   <div class="container">
#     <h2>🌿 NATURE</h2>
#     <form method="post">
#         <input name="url" placeholder="Enter YouTube URL" required>
#         <select name="type">
#             <option>Video (Best Quality)</option>
#             <option>Video (Choose Resolution)</option>
#             <option>Audio Only</option>
#         </select>
#         <select name="resolution">
#             <option>144p</option>
#             <option>240p</option>
#             <option>360p</option>
#             <option>480p</option>
#             <option>720p</option>
#             <option>1080p</option>
#         </select>
#         <button type="submit">Download</button>
#     </form>
#   </div>
# </body>
# </html>
# """

# RESOLUTION_MAP = {
#     "144p": "160",
#     "240p": "133",
#     "360p": "134",
#     "480p": "135",
#     "720p": "136",
#     "1080p": "137"
# }

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         url = request.form.get("url", "").strip()
#         dl_type = request.form.get("type")
#         resolution = request.form.get("resolution")

#         if not url:
#             return "❌ Error: URL is required.", 400

#         output_template = str(VIDEOS_DIR / '%(title)s.%(ext)s')

#         ydl_opts = {
#             'outtmpl': output_template,
#             'noplaylist': True,
#             'quiet': True,
#             'no_warnings': True,
#             'ffmpeg_location': '/usr/bin/ffmpeg',
#             'socket_timeout': 30,
#             'retries': 10,
#             'fragment_retries': 20,
#             'continuedl': True,
#         }

#         if dl_type == "Audio Only":
#             ydl_opts.update({
#             'format': 'bestaudio[ext=m4a]/bestaudio/best',
#             'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#                 }]
#             })

#         elif dl_type == "Video (Choose Resolution)":
#             video_format = RESOLUTION_MAP.get(resolution, "bestvideo")
#             ydl_opts.update({
#                 'format': f"{video_format}+bestaudio[ext=m4a]/best",
#                 # No postprocessor needed — yt_dlp handles merge
#             })

#         else:  # Video (Best Quality)
#             ydl_opts.update({
#                 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
#                 # No postprocessor needed
#             })



#         try:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 ydl.download([url])
#             time.sleep(1)
#             latest_file = max(VIDEOS_DIR.glob("*"), key=lambda f: f.stat().st_mtime)

#             return send_file(
#                 latest_file,
#                 as_attachment=True,
#                 download_name=latest_file.name,
#                 mimetype='application/octet-stream'
#             )

#         except Exception as e:
#             return f"❌ Download failed: {e}", 500

#     return render_template_string(HTML_FORM)

# if __name__ == "__main__":
#     app.run(debug=True)













from flask import Flask, request, send_file, render_template_string, jsonify
from pathlib import Path
import threading
import yt_dlp
import time

app = Flask(__name__)
VIDEOS_DIR = Path("downloads")
VIDEOS_DIR.mkdir(exist_ok=True)

download_status = {"ready": False, "file": None, "error": None}

HTML_FORM = """<!doctype html>
<html><head><title>Nature - YouTube Downloader</title>
<style>
body, html { margin:0; padding:0; height:100%; overflow:hidden; font-family:Arial }
video.bg-video { position:fixed; top:0; left:0; min-width:100%; min-height:100%; object-fit:cover; z-index:-1 }
.container { position:absolute; top:50%; left:50%; transform:translate(-50%, -50%);
    background:rgba(0,0,0,0.6); backdrop-filter:blur(10px); padding:30px; border-radius:20px;
    color:white; width:400px; text-align:center; box-shadow:0 0 20px rgba(0,0,0,0.8); }
input, select, button { width:100%; padding:12px; margin:10px 0; border-radius:8px; border:none; font-size:14px }
button { background:#28a745; color:white; cursor:pointer; font-size:16px }
button:hover { background:#218838 }
</style>
</head><body>
<video class="bg-video" autoplay muted loop playsinline><source src="/static/vid1.mp4" type="video/mp4"></video>
<div class="container"><h2>🌿 NATURE</h2>
<form method="post">
  <input name="url" placeholder="Enter YouTube URL" required>
  <select name="type">
    <option>Video (Best Quality)</option>
    <option>Video (Choose Resolution)</option>
    <option>Audio Only</option>
  </select>
  <select name="resolution">
    <option>144p</option><option>240p</option><option>360p</option>
    <option>480p</option><option>720p</option><option>1080p</option>
  </select>
  <button type="submit">Download</button>
</form></div></body></html>
"""

PROGRESS_HTML = """
<!doctype html><html><head><title>Downloading...</title></head>
<body style="font-family:sans-serif;text-align:center;margin-top:100px;">
<h2>⏳ Downloading your video...</h2>
<div class="spinner"></div>
<script>
setInterval(() => {
    fetch('/status').then(r => r.json()).then(data => {
        if (data.ready) window.location.href = '/download';
        if (data.error) document.body.innerHTML = "<h2 style='color:red;'>❌ " + data.error + "</h2>";
    });
}, 2000);
</script>
<style>
.spinner { margin: 20px auto; border: 6px solid #f3f3f3; border-top: 6px solid #28a745;
    border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>
</body></html>
"""

RESOLUTION_MAP = {
    "144p": "160", "240p": "133", "360p": "134",
    "480p": "135", "720p": "136", "1080p": "137"
}


def download_video(url, dl_type, resolution):
    try:
        output_template = str(VIDEOS_DIR / '%(title).80s.%(ext)s')
        ydl_opts = {
            'outtmpl': output_template,
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4',
            'ffmpeg_location': '/usr/bin/ffmpeg',
            'socket_timeout': 30,
            'retries': 5,
            'fragment_retries': 10,
            'continuedl': True,
        }

        # Audio only (to mp3)
        if dl_type == "Audio Only":
            ydl_opts.update({
                'format': 'bestaudio[ext=m4a]/bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            })
        else:
            # Video (skip .webm / .opus)
            fmt_video = RESOLUTION_MAP.get(resolution, "bestvideo")
            ydl_opts['format'] = (
                f"{fmt_video}[ext=mp4]+bestaudio[ext=mp3]/best[ext=mp4]/best"
                if dl_type == "Video (Choose Resolution)"
                else "bestvideo[ext=mp4]+bestaudio[ext=mp3]/best[ext=mp4]/best"
            )
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])

        final_file = max(VIDEOS_DIR.glob("*"), key=lambda f: f.stat().st_mtime)
        if final_file.suffix == ".part":
            raise Exception("❌ Incomplete download detected")

        download_status.update({
            "ready": True,
            "file": str(final_file),
            "error": None
        })

    except Exception as e:
        download_status.update({
            "ready": False,
            "file": None,
            "error": str(e)
        })


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        dl_type = request.form.get("type")
        resolution = request.form.get("resolution")

        download_status.update({"ready": False, "file": None, "error": None})
        threading.Thread(target=download_video, args=(url, dl_type, resolution)).start()
        return PROGRESS_HTML
    return render_template_string(HTML_FORM)


@app.route("/status")
def status():
    return jsonify(download_status)


@app.route("/download")
def download():
    if not download_status["ready"] or not download_status["file"]:
        return "❌ File not ready", 400
    return send_file(download_status["file"], as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
