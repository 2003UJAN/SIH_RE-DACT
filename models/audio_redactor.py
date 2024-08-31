import speech_recognition as sr
from gtts import gTTS
from utils.sanitization import sanitize_input
from utils.logging import log_info
from models.text_redactor import TextRedactor

class AudioRedactor:
    def redact_audio(self, audio_path, degree=1):
        sanitized_audio_path = sanitize_input(audio_path)

        recognizer = sr.Recognizer()
        with sr.AudioFile(sanitized_audio_path) as source:
            audio = recognizer.record(source)
        
        try:
            text = recognizer.recognize_google(audio)
            text_redactor = TextRedactor()
            redacted_text = text_redactor.redact_text(text, text_redactor.perform_ner(text), degree)
            return redacted_text
        except sr.UnknownValueError:
            log_info("Could not understand audio")
        except sr.RequestError as e:
            log_info(f"Error with Google API: {e}")

        return None

    def save_audio_file(self, text, filename="redacted_audio.mp3"):
        sanitized_filename = sanitize_input(filename)
        tts = gTTS(text=text, lang='en')
        tts.save(sanitized_filename)
        log_info(f"Redacted audio saved as {sanitized_filename}")

    def process(self):
        audio_path = input("Please enter the path of the audio file you would like to redact: ")
        print("Redaction levels:")
        print("1. Redact names of people and organizations.")
        print("2. Redact names of people, organizations, and dates.")
        print("3. Redact all detected entities.")
        degree = int(input("Choose the redaction level (1-3): "))
        redacted_text = self.redact_audio(audio_path, degree)
        if redacted_text:
            self.save_audio_file(redacted_text)
            print("Audio has been redacted and saved.")
