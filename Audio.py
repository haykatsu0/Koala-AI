import keyboard, pyttsx3, whisper, string
import sounddevice as sd
import numpy as np
from Chat import GeminiAssistant
from Config import API_KEY, Gemini_Model, vc_key, lang

model = whisper.load_model("base")

# ---------------------------
# Speech to Text
# ---------------------------

def record_while_key_held(fs=16000):
    audio_frames = []

    def callback(indata, frames, time, status):
        audio_frames.append(indata.copy())

    with sd.InputStream(samplerate=fs, channels=1, dtype='float32', callback=callback):
        while keyboard.is_pressed(vc_key):
            sd.sleep(50)

    audio = np.concatenate(audio_frames, axis=0)
    return audio.flatten()

def stt_from_audio(audio):
    result = model.transcribe(audio, language=lang, fp16=False)
    text = result["text"].strip().lower()
    return text

# ---------------------------
# Text to Speech
# ---------------------------

def tts(text):
    engine = pyttsx3.init()
    
    voices = engine.getProperty('voices')
    selected_voice = None

    for voice in voices:
        if lang.lower() in voice.name.lower() or lang.lower() in voice.id.lower():
            selected_voice = voice.id
            break
    
    if selected_voice:
        engine.setProperty('voice', selected_voice)
    else:
        print(f"\033[31m No matching TTS voice found for '{lang}'. Using default voice. \033[0m\n")

    engine.say(text)
    engine.runAndWait()

# ---------------------------
# Voice Chat: STT + TTS
# ---------------------------

def voice_chat():
    ai = GeminiAssistant(api_key=API_KEY, model_name=Gemini_Model)

    print(f"\n\033[35mWelcome to Koala.\033[0m\n"
          f"Hold '{vc_key}' to talk.\n"
          "Say 'close' for mode selection.\n"
          "Say 'exit' to leave.\n")

    while True:
        print("\033[96mYou:\033[0m ", end='\r')

        if keyboard.is_pressed(vc_key):
            print("\033[96mYou:\033[0m ...", end='\r')
            audio = record_while_key_held()
            print("\r\033[K", end='')
            print("\033[96mYou:\033[0m ", end='\r')
            text = stt_from_audio(audio)

            if not text:
                continue

            print(f"\033[96mYou:\033[0m {text}\n")

            clean_text = text.lower().strip().translate(str.maketrans('', '', string.punctuation))
            if clean_text == "close":
                break

            if clean_text == "exit":
                exit()

            reply = ai.generate_reply(text)
            print(f"\033[35mKoala:\033[0m {reply}\n")
            tts(reply)