# 🤖 AI-Powered Real-Time Computer Vision & Voice Assistant Platform

A full-stack, multimodal AI application that combines real-time object detection with adaptive text-to-speech interaction. Built with **YOLOv8**, **OpenCV**, and **Flask**, this project seamlessly bridges real-time computer vision streams with dynamic audio feedback.

---

## ✨ Features

* **Real-Time Object Detection:** Streams video feeds and detects objects instantly using **YOLOv8** and **OpenCV**.
* **Multimodal Voice Assistant:** Provides continuous audio feedback based on detected objects or voice interactions.
* **Dual Text-to-Speech (TTS) Engine:** Supports both cloud-based speech synthesis (**gTTS**) and offline/edge speech generation (**pyttsx3**).
* **Asynchronous Multithreading:** Utilizes Python's `threading` and `Queue` modules for smooth, non-blocking audio playback alongside real-time frame processing.
* **Responsive Web Interface:** Built-in web UI powered by HTML5, CSS3, JavaScript, and Flask templates.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Computer Vision:** YOLOv8 (Ultralytics), OpenCV
* **Audio & Speech Processing:** gTTS, pyttsx3, playsound
* **Concurrency:** Python `threading`, `queue`
* **Frontend:** HTML5, CSS3, JavaScript

---

## 📂 Project Structure

```text
DataHub_Project/
├── static/
│   ├── index.css
│   └── index.js
├── templates/
│   └── index.html
├── app.py              # Main Flask application & routes
├── assistant.py        # Voice assistant logic
├── trans.py            # Translation & speech utilities
├── test_voice.py       # Speech engine test scripts
└── yolov8n.pt          # Pre-trained YOLOv8 model weights
