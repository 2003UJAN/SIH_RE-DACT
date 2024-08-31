import cv2
import os
from utils.sanitization import sanitize_input
from utils.logging import log_info

class VideoRedactor:
    def redact_video_with_haar(self, video_path, degree=1):
        sanitized_video_path = sanitize_input(video_path)
        if not os.path.exists(sanitized_video_path):
            log_info(f"File not found: {sanitized_video_path}")
            return None

        cap = cv2.VideoCapture(sanitized_video_path)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(f'redacted_{os.path.basename(sanitized_video_path)}', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                if degree == 1:
                    face = frame[y:y+h, x:x+w]
                    blurred_face = cv2.GaussianBlur(face, (99, 99), 30)
                    frame[y:y+h, x:x+w] = blurred_face
                elif degree == 2:
                    face = frame[y:y+h, x:x+w]
                    small_face = cv2.resize(face, (w // 10, h // 10), interpolation=cv2.INTER_LINEAR)
                    resized_face = cv2.resize(small_face, (w, h), interpolation=cv2.INTER_NEAREST)
                    frame[y:y+h, x:x+w] = resized_face
                elif degree == 3:
                    frame[y:y+h, x:x+w] = 0

            out.write(frame)

        cap.release()
        out.release()
        log_info(f"Redacted video saved as redacted_{os.path.basename(sanitized_video_path)}")

    def process(self):
        video_path = input("Please enter the path of the video you would like to redact: ")
        print("Redaction levels:")
        print("1. Blur detected faces.")
        print("2. Pixelate detected faces.")
        print("3. Black out detected faces.")
        degree = int(input("Choose the redaction level (1-3): "))
        self.redact_video_with_haar(video_path, degree)
        print("Video has been redacted and saved.")
