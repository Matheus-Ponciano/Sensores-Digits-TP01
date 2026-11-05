import cv2
import numpy as np
import tensorflow as tf

BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)

# Load custom trained MNIST model
model = tf.keras.models.load_model("Modelo.keras")

# Static IP address assigned in AP Mode
STREAM_URL = "http://192.168.4.1/stream"

def main():
    print(f"Connecting to stream: {STREAM_URL}")
    cap = cv2.VideoCapture(STREAM_URL)

    if not cap.isOpened():
        print("Error: Could not open video stream. Ensure your PC is connected to 'Digits-Network'.")
        return

    frame_count = 0

    latest_detections = []
    latest_thresh = None
    thresh_method = False


    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from ESP32 feed.")
            break

        # Fix orientation
        frame = cv2.flip(frame, 1) 

        frame_count += 1

        # Process every 6th frame to significantly reduce flicker and lower CPU load
        if frame_count % 6 == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (7, 7), 0)

            thresh = None
            # Otsu's thresholding
            if(thresh_method):
                _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # Adaptative thresholding
            else:
                thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV,11,2)

            latest_thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Collect all valid digit bounding boxes first
            digit_boxes = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                area = w * h
                
                # Filter by size
                if area > 300 and 15 < w < 250 and 15 < h < 250:
                    digit_boxes.append((x, y, w, h))

            # Sort bounding boxes from Left to Right (x-coordinate) 
            digit_boxes = sorted(digit_boxes, key=lambda b: b[0])

            current_frame_detections = []

            for (x, y, w, h) in digit_boxes:
                pad = 8
                y1 = max(0, y - pad)
                y2 = min(frame.shape[0], y + h + pad)
                x1 = max(0, x - pad)
                x2 = min(frame.shape[1], x + w + pad)
                
                roi = thresh[y1:y2, x1:x2]

                try:
                    roi_resized = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
                    input_data = roi_resized.astype("float32") / 255.0
                    input_data = np.expand_dims(input_data, axis=(0, -1))

                    predictions = model.predict(input_data, verbose=0)
                    predicted_digit = np.argmax(predictions[0])
                    confidence = np.max(predictions[0])

                    if confidence > 0.50:
                        current_frame_detections.append((x, y, w, h, predicted_digit, confidence, GREEN))
                    else:
                        current_frame_detections.append((x, y, w, h, predicted_digit, confidence, RED))
                except Exception:
                    continue

            latest_detections = current_frame_detections

        # Draw boxes consistently every frame using the latest stable detection 
        full_number_string = ""
        for (x, y, w, h, digit, conf, color) in latest_detections:
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, str(digit)+':'+"{0:.2f}".format(conf), (x, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            full_number_string += str(digit)

        # If digits are found on screen, print the combined sequence at the top
        if len(full_number_string) > 0:
            cv2.putText(frame, f"Detected Number: {full_number_string}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, BLUE, 2)

        cv2.imshow("Multi-Digit ESP32 Recognition", frame)

        if latest_thresh is not None:
            if(thresh_method):
                cv2.putText(latest_thresh, f"Threshold Method: Otsu", (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, BLUE, 2)
            else:
                cv2.putText(latest_thresh, f"Threshold Method: Adaptative Gaussean", (20,40),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, BLUE, 2)
            cv2.imshow("Thresholded Inverted Image", latest_thresh)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.waitKey(1) & 0xFF == ord('t'):
            thresh_method = not thresh_method

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()