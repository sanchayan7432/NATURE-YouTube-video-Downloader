# NATURE-YouTube-video-Downloader
This project is a YouTube Video Downloader built with Flask and yt_dlp (a fork of youtube-dl).


Here is the `README.md` content for your **Flask-based YouTube Downloader** project:

---

# 🌿 Nature - YouTube Video & Audio Downloader

A Flask web application that allows users to download YouTube videos or audio in high quality. It supports different resolutions, progress tracking, and ensures compatibility by avoiding unsupported formats like `.opus`.

![Preview](static/vid1.mp4) *(Background video with glassmorphism form UI)*

---

## 🚀 Features

* 📥 Download YouTube Videos (Best Quality or Custom Resolution)
* 🎵 Download Audio in `.mp3` format (avoids unsupported `.opus`)
* 🔄 Shows Real-Time Download Progress
* 🎞️ Stylish UI with video background and glass blur
* ❌ Prevents duplicate downloads of the same URL
* ✅ Merges video and audio using `ffmpeg` to produce compatible `.mp4`

---

## 🧰 Tech Stack

* **Backend:** Flask (Python)
* **Downloader:** `yt_dlp`
* **Frontend:** HTML, CSS (Glassmorphism)
* **Media Processor:** `ffmpeg`

---

## 🧪 Requirements

Install via:

```bash
pip install flask yt-dlp
```

Ensure `ffmpeg` is installed and accessible:

```bash
sudo apt install ffmpeg   # On Linux

# or for Windows: Download from https://ffmpeg.org/download.html and add to PATH
```

---

## 📂 Directory Structure

```
project-root/
│
├── main.py               # Flask backend
├── downloads/            # Folder where videos are saved
├── static/vid1.mp4       # Background video
├── requirements.txt      # Dependencies
└── README.md
```

---

## ⚙️ Running the App

```bash
python main.py
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📌 Important Notes

* `.opus` audio is **not compatible** with many players (like Windows Media Player). The app forces `.mp3` audio extraction to ensure broad support.
* All merged videos are output as `.mp4` using `ffmpeg`.

---

## 📦 Download Behavior

* Videos are downloaded only once for the same URL to prevent redundancy.
* Background download thread with a progress spinner ensures a smooth experience.
* Supports multiple resolutions like 144p, 240p, 360p, etc.

---

## 🛠️ Troubleshooting

* **Port already in use:** Run `lsof -i :5000` or change the port in `app.run(port=XXXX)`
* **.part file issues:** Ensured `.mp4` is finalized before serving. Use `merge_output_format` in yt\_dlp.
* **FFmpeg errors:** Ensure `ffmpeg` is installed correctly and available in system PATH.

---

## 🧾 License

MIT License © 2025 — Sanchayan Ghosh

---

Let me know if you’d like a `requirements.txt` or Dockerfile as well.
