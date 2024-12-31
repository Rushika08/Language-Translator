from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

# Function to capture voice input
def take_command(language, retries=3):
    recognizer = sr.Recognizer()
    for attempt in range(retries):
        with sr.Microphone() as source:
            print(f"Listening ({language})... Attempt {attempt + 1} of {retries}")
            recognizer.pause_threshold = 1
            try:
                audio = recognizer.listen(source)
                print("Recognizing...")
                query = recognizer.recognize_google(audio, language=language)
                print(f"You said: {query}\n")
                return query.lower()
            except sr.UnknownValueError:
                print("Could not understand. Please say that again...")
            except sr.RequestError:
                print("Service is unavailable. Please check your internet connection.")
                return None
    print("Failed to recognize input after multiple attempts.")
    return None


# Function to translate text and speak it
def translate_and_speak(text, dest_lang, src_lang):
    translator = Translator()
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text
    print(f"Translated to ({dest_lang}): {translated_text}")

    tts = gTTS(text=translated_text, lang=dest_lang, slow=False)
    tts.save("temp_audio.mp3")
    playsound("temp_audio.mp3")
    os.remove("temp_audio.mp3")

    return translated_text

# Function to save the conversation to a text file
def save_conversation_to_file(conversation):
    with open("conversation.txt", "w") as file:  # Write all at once after the loop
        file.writelines([line + "\n" for line in conversation])

# Main conversation loop
def continuous_conversation():
    print("Starting conversation. Say 'stop' to end.")
    doctor_lang = 'en'
    patient_lang = 'si'

    conversation = []  # List to store the conversation in text

    while True:
        # Doctor's turn
        print("Doctor's turn:")
        doctor_query = take_command(doctor_lang)
        if doctor_query is None or "stop" in doctor_query:
            print("Conversation ended.")
            break
        translated_doctor_query = translate_and_speak(doctor_query, dest_lang=patient_lang, src_lang=doctor_lang)
        conversation.append(f"Doctor: {doctor_query}")
        # conversation.append(f"Patient (translated): {translated_doctor_query}")

        # Patient's turn
        print("Patient's turn:")
        patient_query = take_command(patient_lang)
        if patient_query is None or "stop" in patient_query:
            print("Conversation ended.")
            break
        translated_patient_query = translate_and_speak(patient_query, dest_lang=doctor_lang, src_lang=patient_lang)
        # conversation.append(f"Patient: {patient_query}")
        conversation.append(f"Patient: {translated_patient_query}")

    # Save the conversation to a file
    save_conversation_to_file(conversation)
    print("Conversation saved to conversation.txt.")

# Run the program
if __name__ == "__main__":
    continuous_conversation()
