from models.text_redactor import TextRedactor
from models.image_redactor import ImageRedactor
from models.video_redactor import VideoRedactor
from models.audio_redactor import AudioRedactor

def chatbot():
    print("Welcome to the Redaction Tool Chatbot! How can I help you today?")
    while True:
        print("\nOptions:")
        print("1. Redact Text")
        print("2. Redact Image")
        print("3. Redact Video")
        print("4. Redact Audio")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            redactor = TextRedactor()
            redactor.process()

        elif choice == '2':
            redactor = ImageRedactor()
            redactor.process()

        elif choice == '3':
            redactor = VideoRedactor()
            redactor.process()

        elif choice == '4':
            redactor = AudioRedactor()
            redactor.process()

        elif choice == '5':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    chatbot()
