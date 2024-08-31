import spacy
from utils.sanitization import sanitize_input
from utils.encryption import encrypt_file_content
from utils.logging import log_info

class TextRedactor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def perform_ner(self, text):
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities

    def redact_text(self, text, entities, degree):
        for entity, label in entities:
            if degree == 1 and label in ["PERSON", "ORG"]:
                text = text.replace(entity, "[REDACTED]")
            elif degree == 2 and label in ["PERSON", "ORG", "DATE"]:
                text = text.replace(entity, "[REDACTED]")
            elif degree == 3:
                text = text.replace(entity, "[REDACTED]")
        return text

    def save_text_file(self, content, filename="redacted_text.txt"):
        sanitized_filename = sanitize_input(filename)
        with open(sanitized_filename, 'w') as file:
            file.write(content)
        log_info(f"Redacted text saved as {sanitized_filename}")

    def process(self):
        text = input("Please enter the text you would like to redact: ")
        print("Redaction levels:")
        print("1. Redact names of people and organizations.")
        print("2. Redact names of people, organizations, and dates.")
        print("3. Redact all detected entities.")
        degree = int(input("Choose the redaction level (1-3): "))
        entities = self.perform_ner(text)
        redacted_text = self.redact_text(text, entities, degree)
        encrypted_text = encrypt_file_content(redacted_text)
        self.save_text_file(encrypted_text.decode('utf-8'))
        print("Text has been redacted and saved.")
