from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import google.generativeai as genai
from dotenv import load_dotenv
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

# Function to summarize the conversation using AI
def summarize_conversation(conversation):
    load_dotenv()
    api_key = os.getenv("google-api-key")
    
    if not api_key:
        print("API key for Generative AI is missing. Please check your environment variables.")
        return

    genai.configure(api_key=api_key)
    
    # Prepare the conversation as input for the model
    conversation_text = "\n".join(conversation)
    prompt = (
        "Summarize the following conversation between a doctor and a patient. "
        "Provide a summary of the patient's condition, doctor's recommendation and any other additional info:\n\n"
        f"{conversation_text}"
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        print("\nGenerated Summary and Recommendations:\n")
        print(response.text)

        # Save the summary and recommendations to a file
        with open("conversation_summary.txt", "w") as file:
            file.write(response.text)

        print("Summary saved to conversation_summary.txt.")
    except Exception as e:
        print(f"Error generating summary: {e}")

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

    # Generate summary and recommendations
    summarize_conversation(conversation)



# Run the program
if __name__ == "__main__":
    continuous_conversation()


    





