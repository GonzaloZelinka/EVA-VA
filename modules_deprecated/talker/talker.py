import io
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play


class Talker:

    def __init__(self, client: OpenAI):
        self._client = client
        pass

    def say(self, text):
        response = self._client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text,
            speed=1.1,
        )

        audio_data = io.BytesIO(response.content)
        audio_segment = AudioSegment.from_file(audio_data, format="mp3")
        play(audio_segment)
