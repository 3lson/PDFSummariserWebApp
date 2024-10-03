from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import PyPDF2
import os
import json
import logging

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files (for serving the HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the PEGASUS model and tokenizer
# Tokenizer - converts the sentences to set of tokens, by assigning unique ID to word to pass to the model 
# ConditionalGeneration - allows us to use the model
tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

# Helper function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to summarize text in segments with max_length parameter
def summarize_segments(text, max_length=120):
    sentences = text.split('. ')
    segments = []
    current_segment = ""

    for sentence in sentences:
        tokenized_length = len(tokenizer(current_segment + sentence, return_tensors="pt").input_ids[0])
        if tokenized_length <= 512:  # Keep segments within the model's max token limit
            current_segment += sentence + '. '
        else:
            if current_segment:
                segments.append(current_segment.strip())
            current_segment = sentence + '. '

    if current_segment:
        segments.append(current_segment.strip())

    summaries = []
    for segment in segments:
        # truncation: shortens the text to make sure it is an appropriate length to pass through our model
        # return_tensors = 'pt' - returns the tensors as PyTorch
        tokens = tokenizer(segment, truncation=True, padding="longest", return_tensors="pt")
        summary_ids = model.generate(
            # "**" unpacks the input_id (actual tokens) and attention_masks (specifies where the specific attention is going to be directed when we are going to generate this text)
            **tokens,
            max_length=max_length,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)

    final_summary = " ".join(summaries)
    return final_summary

# Serve the HTML file from a static directory
@app.get("/", response_class=HTMLResponse)
def get_html():
    with open(os.path.join("static", "index.html")) as f:
        return f.read()

# Summarization route for PDF uploads
@app.post("/summarize/pdf")
async def summarize_pdf(file: UploadFile = File(...), length: str = "medium"):
    pdf_text = extract_text_from_pdf(file.file)
    
    if not pdf_text or pdf_text.strip() == "":
        return {"error": "Failed to extract text from the PDF. Please check the PDF content."}

    # Adjust max_length based on the input text length
    input_length = len(tokenizer(pdf_text).input_ids)

    # Set max_length based on user selection and input length
    if length == "short":
        max_length = 30  # Fixed short length
    elif length == "medium":
        max_length = 90  # Fixed medium length
    elif length == "long":
        max_length = 150  # Fixed long length
    else:
        max_length = 90  # Default to medium if length is unrecognized

    # Optional: You can still adjust max_length based on input length if desired
    # But ensure that it doesn't override user settings
    if input_length < 100:  # Short input
        max_length = min(max_length, 30)
    elif input_length < 300:  # Medium input
        max_length = min(max_length, 90)
    else:  # Long input
        max_length = min(max_length, 150)

    summary = summarize_segments(pdf_text, max_length=max_length)
    return {"summary": summary, "input_length": input_length}

# Summarization route for text input
@app.post("/summarize/text")
async def summarize_text(input_data: dict):
    text = input_data.get("text")
    length = input_data.get("length", "medium")

    # Log the input data
    logging.info(f"Received text for summarization: {text[:30]}...")  # Log first 30 chars for brevity
    logging.info(f"Summary length selected: {length}")
    
    if not text or text.strip() == "":
        return {"error": "No text provided for summarization."}

    # Adjust max_length based on the input text length
    input_length = len(tokenizer(text).input_ids)

    # Set max_length based on user selection
    if length == "short":
        max_length = 30  # Fixed short length
    elif length == "medium":
        max_length = 90  # Fixed medium length
    elif length == "long":
        max_length = 150  # Fixed long length
    else:
        max_length = 90  # Default to medium if length is unrecognized

    # Optional: You can still adjust max_length based on input length if desired
    # But ensure that it doesn't override user settings
    if input_length < 100:  # Short input
        max_length = min(max_length, 30)
    elif input_length < 300:  # Medium input
        max_length = min(max_length, 90)
    else:  # Long input
        max_length = min(max_length, 150)

    summary = summarize_segments(text, max_length=max_length)
    return {"summary": summary, "input_length": input_length}