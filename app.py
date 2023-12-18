import subprocess
from vosk import Model, KaldiRecognizer
import os
import wave
import json
import time

# Path to your video file
video_file_path = "C:\\users\\troyd\\Videos\\2023-12-17 22-59-35.mkv"
# Path to the output audio file
audio_file_path = "output.wav"
# Path to your Vosk model
model_path = "./models/vosk-model-small-en-us-0.15"  # Replace with your Vosk model path
transcription_file_path = "transcription.txt"  # File to store transcriptions
some_delay = 10  # Delay in seconds, adjust as needed


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

def transcribe_incrementally(audio_path, model_path, transcription_path):
    model = Model(model_path)
    file_pos = 0

    try:
        with open(transcription_path, 'a') as trans_file:  # Open transcription file in append mode
            while True:  # Continuous loop
                with wave.open(audio_path, "rb") as wf:
                    wf.setpos(file_pos)  # Seek to the last read position
                    recognizer = KaldiRecognizer(model, wf.getframerate())

                    while True:  # Transcribe new audio
                        data = wf.readframes(4000)
                        if len(data) == 0:
                            break
                        if recognizer.AcceptWaveform(data):
                            result = json.loads(recognizer.Result())
                            trans_file.write(result.get('text', '') + '\n')
                            trans_file.flush()  # Flush the output buffer

                    
                    file_pos = wf.tell()  # Remember the position for the next iteration

                # Sleep or wait for a while before next iteration
                # to allow new audio to be recorded
                time.sleep(some_delay)

    except Exception as e:
        print(f"Error during transcription: {e}")

# Extract audio and transcribe
#if extract_audio(video_file_path, audio_file_path):
    #transcribe_audio(audio_file_path)
transcribe_incrementally(audio_file_path, model_path, transcription_file_path)

