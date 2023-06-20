import whisper

#whisper
def transcribe_audio(audio_path):
    model = whisper.load_model("small")
    result = model.transcribe(audio_path)
    text = result["text"]
    language = result["language"]
    return text, language
