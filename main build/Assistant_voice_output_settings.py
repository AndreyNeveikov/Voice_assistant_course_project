# Functional
import sounddevice as sd
import torch
import time


SPEAKER_LIST = ['aidar', 'baya', 'kseniya', 'xenia', 'random']

class Speaker:

    def __init__(self):
        s

language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000
speaker = SPEAKER_LIST[3]
put_accent = True
put_yo = True
device = torch.device('cpu')

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)


def pronounce_assistant_answer(what: str):
    """
    Say the phrase aloud with speech synthesis

    :param what: written phrase
    :return: nothing
    """
    audio = model.apply_tts(text=what+"..",
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)

    sd.play(audio, sample_rate * 1.05)
    time.sleep((len(audio) / sample_rate) + 0.5)
    sd.stop()