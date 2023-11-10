import os
import time
import cv2
import openai
import base64
import pygame
import sounddevice as sd
import wavio

# Ensure the OpenAI API key is set
openai.api_key = os.getenv('OPENAI_API_KEY')
if openai.api_key is None:
    raise ValueError('The OPENAI_API_KEY environment variable is not set.')

# Function Definitions

def capture_image(image_path):
    """
    Captures an image from the webcam and saves it to the specified path.
    """
    with cv2.VideoCapture(0) as cap:
        if not cap.isOpened():
            raise ValueError("Could not open webcam")
        ret, frame = cap.read()
        if not ret:
            raise ValueError("Could not read frame")
        cv2.imwrite(image_path, frame)

def encode_image_to_base64(image_path):
    """
    Encodes the given image to base64 format for API requests.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_art_advice(encoded_image):
    """
    Sends the encoded image to OpenAI's API and returns art advice.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "user", "content": [{"type": "text", "text": "What improvements can be made to this drawing?"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}]},
        ],
        max_tokens=1000,
    )
    return response.choices[0].message["content"]

def text_to_speech_and_play(text):
    """
    Converts the given text to speech, saves, and plays the audio using pygame.
    """
    speech_path = "speech_output.mp3"
    spoken_response = openai.Audio.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    spoken_response.stream_to_file(speech_path)

    # Initialize pygame mixer
    pygame.mixer.init()
    # Load and play the sound
    sound = pygame.mixer.Sound(speech_path)
    sound.play()

    # Wait for the sound to finish playing
    while pygame.mixer.get_busy():
        pygame.time.delay(100)

    return speech_path

def transcribe_audio(audio_file_path):
    """
    Transcribes the audio from the given file path.
    """
    with open(audio_file_path, "rb") as audio_file:
        transcript_response = openai.AudioTranscription.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    return transcript_response.text

def record_audio(duration=5, filename="user_query.wav", sample_rate=44100):
    """
    Records audio from the microphone for the specified duration.
    """
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()
    wavio.write(filename, recording, sample_rate, sampwidth=2)
    return filename

# Main Functions

def interactive_art_advisor():
    """
    Main loop that listens to user queries, transcribes them, and gives art advice.
    """
    try:
        while True:
            print("Please speak now...")
            audio_file = record_audio()
            user_query = transcribe_audio(audio_file)
            print(f"Transcribed text: {user_query}")
            # Process user query as needed
            time.sleep(2)
    except KeyboardInterrupt:
        print("Stopping the interactive art advisor.")

def periodic_art_advice():
    """
    Periodically captures an image and gets art advice.
    """
    image_path = "/mnt/data/captured_image.jpg"
    try:
        while True:
            capture_image(image_path)
            encoded_image = encode_image_to_base64(image_path)
            advice = get_art_advice(encoded_image)
            text_to_speech_and_play(advice)
            time.sleep(120)
    except KeyboardInterrupt:
        print("Art advice process stopped manually.")

# Program Execution

if __name__ == "__main__":
    # Choose either interactive art advisor or periodic art advice based on your need
    interactive_art_advisor()
    # periodic_art_advice()
