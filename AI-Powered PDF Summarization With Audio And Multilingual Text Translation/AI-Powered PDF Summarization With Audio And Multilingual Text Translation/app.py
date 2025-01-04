from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from transformers import pipeline
from pdfminer.high_level import extract_text
import PyPDF2
from gtts import gTTS
import pyttsx3
import json
import os

app = Flask(__name__)

# Path to the directory where audio files will be saved
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to extract text from PDF
def extract_pdf_text(pdf_path):
    return extract_text(pdf_path)

# Function to summarize the text using Hugging Face
def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=200, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Function to convert text to audio using pyttsx3 (offline)
def text_to_audio_pyttsx3(text, output_audio_file):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_audio_file)
    engine.runAndWait()

# Function to convert text to audio using gTTS (online)
def text_to_audio_gtts(text, output_audio_file):
    tts = gTTS(text)
    tts.save(output_audio_file)

# Function to extract text from PDF using PyPDF2
def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to translate text using Google Translator
def translate_text(text, target_language="kn"):
    from googletrans import Translator
    translator = Translator()
    return translator.translate(text, dest=target_language).text

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        pdf_file = request.files["pdf_file"]
        if pdf_file:
            # Save uploaded PDF temporarily
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(pdf_path)

            # Extract text from PDF
            pdf_text = extract_pdf_text(pdf_path)

            # Summarize the extracted text
            summary_text = summarize_text(pdf_text)

            # Save summary text to a file
            summary_file = os.path.join(app.config['UPLOAD_FOLDER'], "summary.txt")
            with open(summary_file, "w") as f:
                f.write(summary_text)

            return render_template("index.html", summary_text=summary_text, summary_file=summary_file)

    return render_template("index.html")

@app.route("/audio", methods=["GET", "POST"])
def audio():
    if request.method == "POST":
        action = request.form["action"]
        summary_file = request.form["summary_file"]
        with open(summary_file, "r") as f:
            summary_text = f.read()

        audio_file = None
        if action == "pyttsx3":
            # Convert summary to audio (offline)
            audio_file = os.path.join(app.config['UPLOAD_FOLDER'], "summary_pyttsx3.mp3")
            text_to_audio_pyttsx3(summary_text, audio_file)
        elif action == "gtts":
            # Convert summary to audio (online)
            audio_file = os.path.join(app.config['UPLOAD_FOLDER'], "summary_gtts.mp3")
            text_to_audio_gtts(summary_text, audio_file)

        # Ensure the audio file was generated
        if audio_file:
            return redirect(url_for('download_audio', filename=os.path.basename(audio_file)))

    return render_template("audio.html")

@app.route("/translate", methods=["GET", "POST"])
def translate():
    if request.method == "POST":
        target_language = request.form["language"]
        summary_file = request.form["summary_file"]
        with open(summary_file, "r") as f:
            summary_text = f.read()

        # Translate the text
        translated_text = translate_text(summary_text, target_language)

        # Save translated text to a file
        translated_file = os.path.join(app.config['UPLOAD_FOLDER'], f"translated_{target_language}.json")
        with open(translated_file, "w", encoding="utf-8") as f:
            json.dump({"translated_text": translated_text}, f, ensure_ascii=False, indent=4)

        return render_template("translate.html", translated_text=translated_text, translated_file=translated_file)

    return render_template("translate.html")

@app.route('/uploads/<filename>')
def download_audio(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
