import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from PIL import Image
import pytesseract
from dotenv import load_dotenv
from groq import Groq
import pdfkit  # Import pdfkit for PDF generation
# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Get the API key from environment variables
api_key = os.environ.get("GROQ_API_KEY")
print(f"API Key: {api_key}")  # Debugging to verify API key

# Initialize Groq client
client = Groq(api_key="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")

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Limit file size to 10MB

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Function to generate a meaningful heading
def generate_heading(text):
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"Condense the main takeaway from this paragraph into a short title.\n\n{text}"
            }
        ]
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192"  # Adjust model if necessary
        )
        heading = chat_completion.choices[0].message.content.strip()

        # Remove unwanted content from heading
        if ":" in heading:
            heading = heading.split(":", 1)[-1].strip()
        return heading
    except Exception as e:
        return f"Error generating heading: {str(e)}"

# Function to generate a summary
def generate_summary(text):
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"Summarize this text into a concise paragraph.\n\n{text}"
            }
        ]
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192"  # Adjust model if necessary
        )
        summary = chat_completion.choices[0].message.content.strip()

        # Remove unwanted content from summary if needed
        if ":" in summary:
            summary = summary.split(":", 1)[-1].strip()
        return summary
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Route for the homepage with upload form
@app.route('/')
def index():
    return render_template('upload.html')

# Route to handle image upload and text extraction
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        # Save the uploaded image to the upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Open the saved image and perform OCR
        try:
            image = Image.open(file_path)
            extracted_text = pytesseract.image_to_string(image)
            heading = generate_heading(extracted_text)
            summary = generate_summary(extracted_text)
            
            # Pass extracted text, heading, and summary to the result page
            return render_template('result.html', extracted_text=extracted_text, heading=heading, summary=summary)
        except Exception as e:
            flash(f'Error processing the image: {str(e)}')
            return redirect(request.url)
    
    flash('Invalid file type. Please upload an image.')
    return redirect(request.url)

# Route to generate and download the PDF
@app.route('/download_pdf', methods=['GET', 'POST'])
def download_pdf():
    # Get the extracted text, heading, and summary from the form
    extracted_text = request.form['extracted_text']
    heading = request.form['heading']
    summary = request.form['summary']

    # Create the content for the PDF
    pdf_content = f"<h1>{heading}</h1><h2>Summary:</h2><p>{summary}</p><h2>Extracted Text:</h2><p>{extracted_text}</p>"

    # Save the PDF to a temporary file
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], "output.pdf")
    pdfkit.from_string(pdf_content, pdf_path)

    # Send the generated PDF file to the user
    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)















