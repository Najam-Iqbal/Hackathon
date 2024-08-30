from flask import Flask, render_template, request, jsonify
import fitz  # PyMuPDF for PDF text extraction
import requests
from transformers import pipeline
from flashcards import generate_flashcards

app = Flask(__name__)

# Load a pre-trained NLP model for NER and text generation (e.g., HuggingFace pipeline)
ner_model = pipeline("ner")
qa_model = pipeline("question-answering")

# Extract text from the uploaded PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Fetch word meaning using a dictionary API
def fetch_word_meaning(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()[0]['meanings'][0]['definitions'][0]['definition']
    return "Meaning not found."

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to upload and process the PDF
@app.route('/upload', methods=['POST'])
def upload_pdf():
    pdf_file = request.files['file']
    pdf_path = f"uploaded/{pdf_file.filename}"
    pdf_file.save(pdf_path)

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(pdf_path)

    # Generate hyperlinks using NER
    entities = ner_model(extracted_text)
    for entity in entities:
        entity_text = entity['word']
        entity_url = f"https://en.wikipedia.org/wiki/{entity_text.replace(' ', '_')}"
        extracted_text = extracted_text.replace(entity_text, f'<a href="{entity_url}" target="_blank">{entity_text}</a>')

    # Generate flashcards
    flashcards = generate_flashcards(extracted_text)

    return jsonify({'text': extracted_text, 'flashcards': flashcards})

# Route to fetch word meaning
@app.route('/word-meaning', methods=['POST'])
def word_meaning():
    word = request.form['word']
    meaning = fetch_word_meaning(word)
    return jsonify({'meaning': meaning})

if __name__ == "__main__":
    app.run(debug=True)
