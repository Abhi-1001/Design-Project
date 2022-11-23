import speech_recognition as sr
import pathlib
import tempfile
from pydub import AudioSegment
import pyaudio
import wave
import io

import numpy as np
import scipy.io.wavfile
import soundfile as sf
from scipy.io.wavfile import write
from audiorecorder import audiorecorder
import os

def convert_mp3_to_wav(wav_file):
    temp_mp3_file = tempfile.NamedTemporaryFile()
    
    input_file = wav_file
    # convert mp3 file to wav file
    try:
        sound = AudioSegment.from_file(input_file.name, format = "mp3")
    except:
        sound = AudioSegment.from_file(input_file.name, format = "mp4")
    sound.export(temp_mp3_file, format="wav")

    return temp_mp3_file


def get_text_from_audio(file_uploaded):
    # if file_uploaded
    print("this:",file_uploaded.name)
    input_file = file_uploaded
    if pathlib.Path(file_uploaded.name).suffix == ".mp3":
        input_file = convert_mp3_to_wav(file_uploaded)

    r = sr.Recognizer()
    with sr.AudioFile(input_file) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text_value = r.recognize_google(audio_data)
    
    return text_value

def convert_bytearray_to_wav_ndarray(input_bytearray: bytes, sampling_rate=16000):
    bytes_wav = bytes()
    byte_io = io.BytesIO(bytes_wav)
    write(byte_io, sampling_rate, np.frombuffer(input_bytearray, dtype=np.int16))
    output_wav = byte_io.read()
    output, samplerate = sf.read(io.BytesIO(output_wav))
    return output


def record_audio():
    audio = audiorecorder("Click to record", "Click to stop recording")

    if len(audio) > 0:       
        # To save audio to a file:
        tmp_audio_file = tempfile.NamedTemporaryFile(delete = False, mode = "w+b", suffix = ".mp3")
        # tmp_audio_file = open("tmp_file_trial.wav", "w+b")
        # if os.path.exists(tmp_audio_file.name):
        #     print("hello")
        #     tmp_audio_file.close()
        #     os.unlink(tmp_audio_file.name)
        #     tmp_audio_file = tempfile.NamedTemporaryFile(delete = False, suffix = ".mp3")
        #     tmp_audio_file.close()
        tmp_audio_file.write(audio.tobytes())

        user_text = get_text_from_audio(tmp_audio_file)

        tmp_audio_file.close()
        os.remove(tmp_audio_file.name)
        return user_text
    
    return None