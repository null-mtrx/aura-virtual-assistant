from gtts import gTTS
import soundfile
import sounddevice
import io

from PySide6.QtCore import QObject, Signal


class SpeechEngine(QObject):
    duration = Signal(float)
    finished = Signal(int)

    def __init__(self, config):
        super().__init__()
        self.accent = config["accent"]
        self.language = config["language"]

    def speak(self, text) -> io.BytesIO:
        audio_buffer = io.BytesIO()
        audio_data = gTTS(text=text, lang=self.language, tld=self.accent)
        audio_data.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        audio, sample_rate = soundfile.read(audio_buffer)
        audio_buffer.seek(0)
        speech_info = soundfile.info(audio_buffer)
        self.duration.emit(speech_info.duration)
        sounddevice.play(audio, sample_rate)
        self.finished.emit(1)
