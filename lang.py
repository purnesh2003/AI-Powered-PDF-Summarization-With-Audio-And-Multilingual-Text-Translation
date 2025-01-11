import json
import PyPDF2
from googletrans import Translator

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to translate text using Google Translator
def translate_text(text, target_language="kn"):
    translator = Translator()
    return translator.translate(text, dest=target_language).text

# Example usage
pdf_file = "C:/Users/HP/Desktop/selenium/Summary_Output.pdf"  # Path to your PDF file
output_file = "C:/Users/HP/Desktop/selenium/output.json"  # Output JSON file

# Extract text from PDF
pdf_text = extract_text_from_pdf(pdf_file)
print("Extracted Text:", pdf_text)

# Translate the extracted text
translated_text = translate_text(pdf_text, target_language="kn")

# Save the translated text in JSON format
translated_data = {"translated_text": translated_text}

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(translated_data, file, ensure_ascii=False, indent=4)

print(f"Translated text saved to {output_file}")
