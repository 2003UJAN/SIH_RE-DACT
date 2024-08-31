import cv2
import os
from utils.sanitization import sanitize_input
from utils.logging import log_info

class ImageRedactor:
    def redact_image_with_haar(self, image_path, degree=1):
        sanitized_image_path = sanitize_input(image_path)
        if not os.path.exists(sanitized_image_path):
            log_info(f"File not found: {sanitized_image_path}")
            return None

        image = cv2.imread(sanitized_image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            if degree == 1:
                face = image[y:y+h, x:x+w]
                blurred_face = cv2.GaussianBlur(face, (99, 99), 30)
                image[y:y+h, x:x+w] = blurred_face
            elif degree == 2:
                face = image[y:y+h, x:x+w]
                small_face = cv2.resize(face, (w // 10, h // 10), interpolation=cv2.INTER_LINEAR)
                resized_face = cv2.resize(small_face, (w, h), interpolation=cv2.INTER_NEAREST)
                image[y:y+h, x:x+w] = resized_face
            elif degree == 3:
                image[y:y+h, x:x+w] = 0

        return image

    def save_image_file(self, image, filename="redacted_image.jpg"):
        sanitized_filename = sanitize_input(filename)
        cv2.imwrite(sanitized_filename, image)
        log_info(f"Redacted image saved as {sanitized_filename}")

    def process(self):
        image_path = input("Please enter the path of the image you would like to redact: ")
        print("Redaction levels:")
        print("1. Blur detected faces.")
        print("2. Pixelate detected faces.")
        print("3. Black out detected faces.")
        degree = int(input("Choose the redaction level (1-3): "))
        redacted_image = self.redact_image_with_haar(image_path, degree)
        if redacted_image is not None:
            self.save_image_file(redacted_image)
            print("Image has been redacted and saved.")
