from transformers import pipeline
from pdfminer.high_level import extract_text
from fpdf import FPDF

# Function to extract text from PDF
def extract_pdf_text(pdf_path):
    return extract_text(pdf_path)

# Function to create PDF and write summary
def write_summary_to_pdf(summary_text, output_pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary_text)  # Allows multi-line text in the PDF
    pdf.output(output_pdf_path)

# Initialize Hugging Face summarizer pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Extract text from PDF
pdf_path = "C:/Users/HP/Desktop/Crisis Compass1.pdf"  # Path to your PDF file
pdf_text = extract_pdf_text(pdf_path)

# Summarize the extracted text
summary = summarizer(pdf_text, max_length=200, min_length=50, do_sample=False)

# Get the summarized text
summary_text = summary[0]['summary_text']

# Output PDF path
output_pdf_path = "C:/Users/HP/Desktop/selenium/Summary_Output.pdf"  # Path to the output PDF file

# Write the summary to the output PDF
write_summary_to_pdf(summary_text, output_pdf_path)

# Print confirmation message
print(f"Summary has been written to {output_pdf_path}")
