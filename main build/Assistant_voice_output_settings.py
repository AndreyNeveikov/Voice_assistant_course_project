# Functional
import sounddevice as sd
import torch
import time


class Speaker:
    """
    Contain the voice acting settings and voice acting method
    """

    def __init__(self, speaker_voice):
        """
        Initializing Voice Assistant Attributes

        :param speaker_voice: selected voice
        """
        self.speaker = speaker_voice
        self.language = 'ru'
        self.model_id = 'ru_v3'
        self.sample_rate = 48000
        self.put_accent = True
        self.put_yo = True
        self.device = torch.device('cpu')

        self.model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                       model='silero_tts',
                                       language=self.language,
                                       speaker=self.model_id)

        self.model.to(self.device)

    def pronounce_assistant_answer(self, what: str):
        """
        Say the phrase aloud with speech synthesis

        :param what: written phrase
        :return: nothing
        """
        audio = self.model.apply_tts(text=what+"..",
                                     speaker=self.speaker,
                                     sample_rate=self.sample_rate,
                                     put_accent=self.put_accent,
                                     put_yo=self.put_yo)

        sd.play(audio, self.sample_rate * 1.05)
        # Waiting for assistant to say a phrase
        time.sleep((len(audio) / self.sample_rate) + 0.5)
        sd.stop()
