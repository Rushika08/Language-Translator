import streamlit as st
import speech_recognition as sr
import io
import os
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder
from googletrans import Translator
from gtts import gTTS
import google.generativeai as genai

def recognize_speech(language, audio_bytes):
    """Recognizes speech from audio bytes using Google Speech Recognition."""
    if not audio_bytes:
        return None
    
    recognizer = sr.Recognizer()
    
    # Convert audio bytes to WAV file in memory
    audio_file = io.BytesIO(audio_bytes)
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file

    try:
        query = recognizer.recognize_google(audio_data, language=language)
        st.success(f"Recognized Speech: {query}")
        return query.lower()
    except sr.UnknownValueError:
        st.error("Could not understand the audio. Please try again.")
    except sr.RequestError:
        st.error("Speech recognition service unavailable. Check your internet connection.")
    
    return None

def translate_and_speak(text, dest_lang, src_lang):
    if not text:
        return None, None  # Return early if text is None

    translator = Translator()
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text
    st.write(f"**Translated ({src_lang} → {dest_lang}):** {translated_text}")

    # Convert translated text to speech
    tts = gTTS(text=translated_text, lang=dest_lang, slow=False)
    
    # Store audio in memory instead of saving to a file
    audio_io = io.BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)  # Move cursor to start for playback

    return translated_text, audio_io

def summarize_conversation(conversation):
    load_dotenv()
    api_key = os.getenv("google-api-key")
    
    if not api_key:
        st.error("API key for Generative AI is missing. Please check your environment variables.")
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
        
        st.subheader("Generated Summary and Recommendations:")
        st.write(response.text)
    except Exception as e:
        st.error(f"Error generating summary: {e}")

def main():
    st.title("Doctor-Patient Conversation Assistant")

    # Language selection
    st.subheader("Select Language Preferences")
    doctor_lang = st.selectbox("Doctor's Language", ["en", "si", "ta", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh-CN"])
    patient_lang = st.selectbox("Patient's Language", ["si", "en", "ta", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh-CN"])

    # Role selection
    role = st.radio("Select Your Role", ["Doctor", "Patient"])
    st.write(f"**{role} Role Selected**")

    # Audio Recording
    st.subheader("Record Your Speech")
    audio_bytes = audio_recorder()

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if audio_bytes:
        # Recognize speech based on selected role
        language = doctor_lang if role == "Doctor" else patient_lang
        recognized_text = recognize_speech(language, audio_bytes)

        # If speech was recognized, translate and generate speech
        if recognized_text:
            dest_lang = patient_lang if role == "Doctor" else doctor_lang
            src_lang = doctor_lang if role == "Doctor" else patient_lang

            translated_text, translated_audio = translate_and_speak(recognized_text, dest_lang, src_lang)
            
            # Play translated speech
            if translated_audio:
                st.audio(translated_audio, format="audio/mp3")

            if translated_text:
                st.write(f"**Recognized Text ({language}):** {recognized_text}")
                st.write(f"**Translated Text ({dest_lang}):** {translated_text}")
                
                if st.button("Append to Conversation"):
                    if role == "Doctor":
                        st.session_state.conversation.append(f"Doctor: {recognized_text}")
                    else:
                        st.session_state.conversation.append(f"Patient: {translated_text}")

    # Display conversation history
    if st.session_state.conversation:
        st.subheader("Conversation History")
        for entry in st.session_state.conversation:
            st.write(entry)

    # Button to summarize conversation
    if st.button("Summarize Conversation") and st.session_state.conversation:
        summarize_conversation(st.session_state.conversation)

if __name__ == "__main__":
    main()
