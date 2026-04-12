from flask import Flask, render_template, request, redirect, url_for, flash
from resume_parser import extract_text
from analyzer import analyze_resume
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('resume')
    job_desc_text = request.form.get('job_description_text', '').strip()

    if not file or file.filename == '':
        flash('Please upload a resume file in PDF or DOCX format.')
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Unsupported file type. Please upload a PDF or DOCX file.')
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    resume_text = extract_text(filepath)
    if not resume_text:
        flash('Could not extract text from the uploaded resume. Please upload a valid PDF or DOCX file.')
        return redirect(url_for('index'))

    analysis = analyze_resume(resume_text, job_desc_text if job_desc_text else None)
    return render_template('dashboard.html', analysis=analysis)

if __name__ == '__main__':
    app.run(debug=True)