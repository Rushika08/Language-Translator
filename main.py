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
    print("Starting conversation. Press 's' to end.")
    doctor_lang = 'en'
    patient_lang = 'si'

    conversation = []  # List to store the conversation in text
    continue_options = ["c", "r", "s"]

    while True:
        while True:
            # Doctor's turn
            print("Doctor's turn:")
            doctor_query = take_command(doctor_lang)
            if doctor_query is None:
                print("Could not recognize input. Try again.")
                continue
            translated_doctor_query = translate_and_speak(doctor_query, dest_lang=patient_lang, src_lang=doctor_lang)
            print("Doctor's query recorded.")

            # Prompt options for the doctor
            print("Press 'c' to continue, 'r' to repeat, or 's' to stop the conversation.")
            doctor_choice = input("Your choice: ").lower()
            while doctor_choice not in continue_options:
                print("Invalid choice. Please press 'c', 'r', or 's.")
                doctor_choice = input("Your choice: ").lower()
            
            if doctor_choice == "s":
                conversation.append(f"Doctor: {doctor_query}")
                print("Conversation ended.")
                save_conversation_to_file(conversation)
                print("Conversation saved to conversation.txt.")
                summarize_conversation(conversation)
                return
            elif doctor_choice == "r":
                print("Repeat the query...")
                continue
            elif doctor_choice == "c":
                conversation.append(f"Doctor: {doctor_query}")
                break

        while True:
            # Patient's turn
            print("Patient's turn:")
            patient_query = take_command(patient_lang)
            if patient_query is None:
                print("Could not recognize input. Try again.")
                continue

            translated_patient_query = translate_and_speak(patient_query, dest_lang=doctor_lang, src_lang=patient_lang)
            print("Patient's query recorded.")

            # Prompt options for the patient
            print("Press 'c' to continue, 'r' to repeat, or 's' to stop the conversation.")
            patient_choice = input("Your choice: ").lower()
            while patient_choice not in continue_options:
                print("Invalid choice. Please press 'c', 'r', or 's.")
                patient_choice = input("Your choice: ").lower()
            
            if patient_choice == "s":
                conversation.append(f"Patient: {translated_patient_query}")
                print("Conversation ended.")
                save_conversation_to_file(conversation)
                print("Conversation saved to conversation.txt.")
                summarize_conversation(conversation)
                return
            elif patient_choice == "r":
                print("Repeat the query...")
                continue
            elif patient_choice == "c":
                conversation.append(f"Patient: {translated_patient_query}")
                break

# Run the program
if __name__ == "__main__":
    continuous_conversation()


    





# import streamlit as st
# from playsound import playsound
# import speech_recognition as sr
# from googletrans import Translator
# from gtts import gTTS
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os

# # Function to capture voice input
# def take_command(language):
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info(f"Listening ({language})...")
#         recognizer.pause_threshold = 1
#         try:
#             audio = recognizer.listen(source)
#             st.info("Recognizing...")
#             query = recognizer.recognize_google(audio, language=language)
#             return query.lower()
#         except sr.UnknownValueError:
#             st.error("Could not understand. Please try again.")
#             return None
#         except sr.RequestError:
#             st.error("Service unavailable. Check your internet connection.")
#             return None

# # Function to translate text and speak it
# def translate_and_speak(text, dest_lang, src_lang):
#     translator = Translator()
#     translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text
#     st.write(f"Translated ({dest_lang}): {translated_text}")

#     tts = gTTS(text=translated_text, lang=dest_lang, slow=False)
#     tts.save("temp_audio.mp3")
#     playsound("temp_audio.mp3")
#     os.remove("temp_audio.mp3")

#     return translated_text

# # Function to save the conversation to a text file
# def save_conversation_to_file(conversation):
#     with open("conversation.txt", "w") as file:
#         file.writelines([line + "\n" for line in conversation])

# # Function to summarize the conversation using AI
# def summarize_conversation(conversation):
#     load_dotenv()
#     api_key = os.getenv("google-api-key")

#     if not api_key:
#         st.error("API key for Generative AI is missing. Please check your environment variables.")
#         return

#     genai.configure(api_key=api_key)

#     conversation_text = "\n".join(conversation)
#     prompt = (
#         "Summarize the following conversation between a doctor and a patient. "
#         "Provide a summary of the patient's condition, doctor's recommendation, and any other additional info:\n\n"
#         f"{conversation_text}"
#     )

#     try:
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         response = model.generate_content(prompt)
#         st.subheader("Summary and Recommendations")
#         st.write(response.text)

#         # Save the summary and recommendations to a file
#         with open("conversation_summary.txt", "w") as file:
#             file.write(response.text)
#         st.success("Summary saved to conversation_summary.txt.")
#     except Exception as e:
#         st.error(f"Error generating summary: {e}")

# # Streamlit Application
# def main():
#     st.title("Doctor-Patient Conversation Assistant")
#     st.sidebar.header("Controls")

#     doctor_lang = st.sidebar.text_input("Doctor's Language Code (e.g., 'en')", "en")
#     patient_lang = st.sidebar.text_input("Patient's Language Code (e.g., 'si')", "si")

#     conversation = st.session_state.get("conversation", [])
#     st.session_state["conversation"] = conversation

#     if st.button("Doctor's Turn"):
#         doctor_query = take_command(doctor_lang)
#         if doctor_query:
#             translated_doctor_query = translate_and_speak(doctor_query, dest_lang=patient_lang, src_lang=doctor_lang)
#             st.session_state.conversation.append(f"Doctor: {doctor_query}")
#             st.session_state.conversation.append(f"Translated: {translated_doctor_query}")

#     if st.button("Patient's Turn"):
#         patient_query = take_command(patient_lang)
#         if patient_query:
#             translated_patient_query = translate_and_speak(patient_query, dest_lang=doctor_lang, src_lang=patient_lang)
#             st.session_state.conversation.append(f"Patient: {patient_query}")
#             st.session_state.conversation.append(f"Translated: {translated_patient_query}")

#     if st.button("End Conversation"):
#         save_conversation_to_file(st.session_state.conversation)
#         st.success("Conversation saved to conversation.txt.")
#         summarize_conversation(st.session_state.conversation)

#     st.subheader("Conversation History")
#     st.text("\n".join(st.session_state.conversation))

# if __name__ == "__main__":
#     main()



# import streamlit as st
# from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
# import numpy as np
# import wave

# class AudioProcessor(AudioProcessorBase):
#     def __init__(self):
#         self.frames = []

#     def recv_audio(self, frames):
#         audio_data = np.frombuffer(frames[0].to_ndarray(), dtype=np.int16)
#         self.frames.append(audio_data)
#         return frames

#     def save_audio(self, filename):
#         if self.frames:
#             audio = np.concatenate(self.frames, axis=0)
#             with wave.open(filename, "wb") as wf:
#                 wf.setnchannels(1)  # Mono
#                 wf.setsampwidth(2)  # 16-bit audio
#                 wf.setframerate(16000)  # 16kHz
#                 wf.writeframes(audio.tobytes())
#             st.success(f"Audio saved to {filename}")

# st.title("Audio Recorder with Streamlit")

# audio_processor = AudioProcessor()

# webrtc_ctx = webrtc_streamer(
#     key="audio_recorder",
#     mode=WebRtcMode.SENDONLY,
#     audio_receiver_size=1024,
#     media_stream_constraints={"audio": True, "video": False},
#     audio_processor_factory=lambda: audio_processor,
# )

# if webrtc_ctx.state.playing:
#     st.info("Recording audio. Press Stop when done.")

# if st.button("Save Audio"):
#     audio_processor.save_audio("output.wav")
