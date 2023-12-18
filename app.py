import subprocess
from vosk import Model, KaldiRecognizer
import os
import wave

# Path to your video file
video_file_path = "C:\\users\\troyd\\Videos\\2023-12-17 22-59-35.mkv"
# Path to the output audio file
audio_file_path = "output.wav"
# Path to your Vosk model
model_path = "./models/vosk-model-small-en-us-0.15"  # Replace with your Vosk model path

# Function to extract audio from video using FFmpeg
def extract_audio(video_path, audio_path):
    try:
        command = f"ffmpeg -i \"{video_path}\" -ac 1 -ar 16000 -vn \"{audio_path}\""
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error in extracting audio: {e}")
        return False
    return True

# Function to transcribe the audio file
def transcribe_audio(file_path):
    # Load the Vosk model
    model = Model(model_path)
    # Open the audio file
    wf = wave.open(file_path, "rb")

    recognizer = KaldiRecognizer(model, wf.getframerate())
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            print(recognizer.Result())
        else:
            print(recognizer.PartialResult())

    print(recognizer.FinalResult())

# Extract audio and transcribe
if extract_audio(video_file_path, audio_file_path):
    transcribe_audio(audio_file_path)
