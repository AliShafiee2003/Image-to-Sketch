import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

# Function to create a sketch from an RGB image
def create_sketch(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    inverted_image = cv2.bitwise_not(gray_image)
    blur_image = cv2.GaussianBlur(inverted_image, (21, 21), 0)
    inverted_blur = cv2.bitwise_not(blur_image)
    sketch = cv2.divide(gray_image, inverted_blur, scale=256.0)
    return sketch

# Section 1: Static Image Processing
if __name__ == "__main__":
    image_path = os.path.join("images", "car.jpg")
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    sketched_image = create_sketch(image_rgb)

    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    output_image_path = os.path.join(output_folder, "sketched_car.jpg")
    cv2.imwrite(output_image_path, sketched_image)

    plt.figure(figsize=(10, 6))
    plt.imshow(sketched_image, cmap="gray")
    plt.title("Sketched Image")
    plt.axis("off")
    plt.show()

# Section 2: Webcam Processing
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        sketched_frame = create_sketch(frame_rgb)
        sketched_frame_bgr = cv2.cvtColor(sketched_frame, cv2.COLOR_RGB2BGR)

        cv2.imshow("Sketched Webcam Frame", sketched_frame_bgr)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# Section 3: Video Processing
    video_path = os.path.join("images", "cars.mp4")
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open the video.")
        exit()

    output_video_path = os.path.join(output_folder, "sketched_cars.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        sketched_frame = create_sketch(frame_rgb)
        sketched_frame_bgr = cv2.cvtColor(sketched_frame, cv2.COLOR_RGB2BGR)

        out.write(sketched_frame_bgr)
        cv2.imshow("Sketched Video Frame", sketched_frame_bgr)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Sketched video saved at: {output_video_path}")
