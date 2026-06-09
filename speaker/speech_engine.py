from gtts import gTTS
import io


class SpeechEngine:
    def __init__(self, config):
        self.audio_buffer = io.BytesIO()
        self.accent = config["accent"]
        self.language = config["language"]

    def speak(self, text) -> io.BytesIO:
        audio_data = gTTS(text=text, lang=self.language, tld=self.accent)
        audio_data.write_to_fp(self.audio_buffer)
        self.audio_buffer.seek(0)
        return self.audio_buffer
