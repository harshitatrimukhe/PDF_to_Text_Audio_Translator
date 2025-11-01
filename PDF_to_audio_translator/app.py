# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from utils.ocr_utils import extract_text_from_pdf, ocr_image
from utils.translate_utils import translate_text, text_to_speech

# ====== Config ======
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Windows path examples (uncomment if needed):
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

POPPLE_WINDOWS_PATH = None

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get('FLASK_SECRET', 'devsecret')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ====== Routes ======
@app.route('/', methods=['GET'])
def index():
    # ✅ LANGUAGE MENU: Added Marathi
    languages = [
        ('English', 'en'),
        ('Hindi', 'hi'),
        ('Marathi', 'mr'),       # ✅ Added Marathi
        ('Spanish', 'es'),
        ('French', 'fr'),
        ('German', 'de'),
        ('Arabic', 'ar'),
        ('Chinese (Simplified)', 'zh-cn'),
        ('Japanese', 'ja')
    ]
    return render_template('index.html', languages=languages)

@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        ext = filename.rsplit('.', 1)[1].lower()

        # ✅ Determine OCR language (Marathi uses "mar")
        target_lang = request.form.get('target_lang', 'en')
        ocr_lang = "mar" if target_lang == "mr" else "eng"

        # ✅ Run OCR for PDF or image
        if ext == 'pdf':
            text = extract_text_from_pdf(save_path, lang=ocr_lang)
        else:
            text = ocr_image(save_path, lang=ocr_lang)

        if not text.strip():
            flash('No text found in the uploaded file.')
            return redirect(url_for('index'))

        # ✅ TTS language (Marathi = mr)
        tts_lang = request.form.get('tts_lang', target_lang) or target_lang

        translated = translate_text(text, dest=target_lang)
        
        try:
            audio_path = text_to_speech(translated, lang=tts_lang, output_dir=app.config['UPLOAD_FOLDER'])
        except:
            audio_path = None

        audio_url = audio_path.replace('\\', '/') if audio_path else None
        return render_template('result.html', original=text, translated=translated, audio_url=audio_url, filename=filename)

    else:
        flash('Unsupported file type. Allowed: pdf, png, jpg, jpeg, gif')
        return redirect(url_for('index'))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
