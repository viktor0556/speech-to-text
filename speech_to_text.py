import openai
import pyttsx3 # convert text to speech
import speech_recognition as sr
import time
import sys

# Set your openai api key
openai.api_key = "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" # replace with your own own open AI key

# Initialize the text to speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping unknown error')

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["coices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        # Wait for user to say "genius"
        print("Say'Genius' to start recording your question")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "genius":
                    # record audio
                    filename = "input.wav"
                    print("Say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_treshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout = None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    # Transcribe audo to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said{text}")

                        # Generate response using GPT-3
                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")

                        # Read response using text to speech
                        speak_text(response)

            except Exception as e:
                print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()

            