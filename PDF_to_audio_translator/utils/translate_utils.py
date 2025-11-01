# utils/translate_utils.py

from googletrans import Translator
from gtts import gTTS
import os
import uuid

translator = Translator()

def translate_text(text, dest='en'):
    """
    Translate text to selected language (Supports Marathi, Hindi, etc.)
    """
    try:
        result = translator.translate(text, dest=dest)
        return result.text
    except Exception as e:
        print(f"Translation Error: {e}")
        return text  # fallback to original text


def text_to_speech(text, lang="en", output_dir="static/uploads"):
    """
    Convert text to speech (gTTS supports Marathi as lang='mr')
    """
    try:
        os.makedirs(output_dir, exist_ok=True)

        # Convert text to audio
        tts = gTTS(text=text, lang=lang)

        # Unique audio filename
        file_name = f"audio_{uuid.uuid4().hex}.mp3"
        save_path = os.path.join(output_dir, file_name)

        tts.save(save_path)
        return save_path
    except Exception as e:
        print(f"TTS Error: {e}")
        return None
