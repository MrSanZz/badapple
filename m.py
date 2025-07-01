import cv2
from PIL import Image
import numpy as np
import os
import time
import sys

# Karakter ASCII berdasarkan kecerahan
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", " ", "'", "|", "!", "&", "-", "="]

def frame_to_ascii(frame, new_width=100):
    # Resize frame dengan ukuran tetap
    height, width, _ = frame.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    # Konversi ke ASCII
    ascii_art = ""
    for pixel_row in gray_frame:
        for pixel in pixel_row:
            ascii_art += ASCII_CHARS[pixel // 25]
        ascii_art += "\n"
    return ascii_art


def display_ascii_video(video_path):
    cap = cv2.VideoCapture(video_path)
    target_fps = 60  # Set target FPS
    frame_duration = 1 / target_fps  # Durasi ideal per frame

    # Tetapkan ukuran ASCII tetap
    fixed_size = None

    while cap.isOpened():
        start_time = time.time()  # Catat waktu mulai frame
        ret, frame = cap.read()
        if not ret:
            break
        
        # Tetapkan ukuran ASCII hanya sekali
        if fixed_size is None:
            height, width, _ = frame.shape
            aspect_ratio = height / width
            new_width = 100  # Lebar ASCII art (bisa disesuaikan)
            new_height = int(aspect_ratio * new_width * 0.55)
            fixed_size = (new_width, new_height)

        # Ubah frame menjadi ASCII art
        ascii_frame = frame_to_ascii(frame, new_width=fixed_size[0])

        # Bersihkan layar dan tampilkan ASCII art
        #os.system("cls" if os.name == "nt" else "clear")
        sys.stdout.write(ascii_frame)
        sys.stdout.flush()

        # Hitung waktu yang digunakan dan sesuaikan jeda
        elapsed_time = time.time() - start_time
        sleep_time = max(0.0078, frame_duration - elapsed_time)
        time.sleep(sleep_time)

    cap.release()


# Main Program
if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=FtutLA63Cp8&ab_channel=kasidid2"  # Ganti dengan URL video
    output_dir = "./videos/output.mp4"

    print("Downloading video...")
    print("Video downloaded.")

    print("Displaying video as ASCII art...")
    display_ascii_video(output_dir)
