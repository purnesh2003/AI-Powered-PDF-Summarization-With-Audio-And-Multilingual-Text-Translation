import PyPDF2
import pyttsx3
from gtts import gTTS

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to convert text to audio using pyttsx3 (offline)
def text_to_audio_pyttsx3(text, output_audio_file):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_audio_file)
    engine.runAndWait()

# Function to convert text to audio using gTTS (online)
def text_to_audio_gtts(text, output_audio_file):
    tts = gTTS(text)
    tts.save(output_audio_file)

# Example usage
pdf_file = "C:/Users/HP/Desktop/selenium/Summary_Output.pdf"  # Path to your PDF file
output_audio_file_pyttsx3 = "output_pyttsx3.mp3"
output_audio_file_gtts = "output_gtts.mp3"

# Extract text from PDF
text = extract_text_from_pdf(pdf_file)
print("Extracted Text:", text)

# Convert to audio (offline with pyttsx3)
text_to_audio_pyttsx3(text, output_audio_file_pyttsx3)
print(f"Audio saved as {output_audio_file_pyttsx3}")

# Convert to audio (online with gTTS)
text_to_audio_gtts(text, output_audio_file_gtts)
print(f"Audio saved as {output_audio_file_gtts}")
