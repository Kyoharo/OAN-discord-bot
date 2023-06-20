from TTS.api import TTS
#TTS
def tts_audio(response, path, lanuage):
    if "ja" in lanuage:
        model_name = 'tts_models/ja/kokoro/tacotron2-DDC'
        tts = TTS(model_name)
        tts.tts_to_file(text=response, file_path=path)
    else:
        model_name = TTS.list_models()[0]
        tts = TTS(model_name)
        tts.tts_to_file(text=response, speaker=tts.speakers[2], language=tts.languages[0], file_path=path)
