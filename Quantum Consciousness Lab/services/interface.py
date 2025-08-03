import speech_recognition as sr

def voice_command():
    """
    Processes voice commands for QCL.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    return recognizer.recognize_google(audio)
