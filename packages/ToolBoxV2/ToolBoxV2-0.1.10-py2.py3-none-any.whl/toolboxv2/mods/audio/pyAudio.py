import os
from pathlib import Path
from typing import Optional

import speech_recognition as sr

from toolboxv2 import get_app, App, MainTool, FileHandler
from toolboxv2.mods.audio.TBV2STT.transcription.liveTranscriptHfOpenai import init_live_transcript, s30sek_mean
from toolboxv2.mods.audio.TBV2TTS.audioProvider.ElevenLapsProviderPy import ElevenLapsProvider
from toolboxv2.mods.audio.TBV2TTS.audioProvider.PiperProviderPy import PiperInterface
from toolboxv2.mods.audio.utils import split_text_x_symbol

try:
    import pyttsx3

    pyttsx3_init = True
except ImportError:
    pyttsx3_init = False

try:
    import whisper

    whisper_init = True
except Exception:
    whisper_init = False

try:
    import winsound

    winsound_init = True
except ImportError:
    winsound_init = False

voices = ["ErXwobaYiN019PkySvjV", "EXAVITQu4vr4xnSDxMaL", "9Mi9dBkaxn2pCIdAAGOB"]
_most_recent_text_spoken_to_user_via_speech_stream_isaa_audio_ = ""

Name = 'audio'
version = "0.0.1"
export = get_app(f"{Name}.EXPORT").tb
no_test = export(mod_name=Name, test=False, version=version)
test_only = export(mod_name=Name, test_only=True, version=version, state=True)
to_api = export(mod_name=Name, api=True, version=version)


class Tools(MainTool, FileHandler):
    version = version

    def __init__(self, app=None):
        self.name = Name
        self.color = "BLUE"

        self.keys = {"mode": "db~mode~~:"}
        self.encoding = 'utf-8'

        self._most_recent_text_spoken_to_user_via_speech_stream_isaa_audio_ = ""
        self._simpel_speech_recognizer = None
        self._simpel_speech_recognizer_mice = None
        self._eleven_laps_provider: Optional[ElevenLapsProvider] = None
        self._piper_provider: Optional[PiperInterface] = None

        MainTool.__init__(self,
                          load=self.on_start,
                          v=self.version,
                          name=self.name,
                          color=self.color,
                          on_exit=self.on_exit)

    @export(
        mod_name=Name,
        name="Version",
        version=version,
    )
    def get_version(self):
        return self.version

    @export(mod_name=Name, initial=True)
    def on_start(self):
        self._simpel_speech_recognizer_mice = sr.Microphone()
        self._simpel_speech_recognizer = sr.Recognizer()
        self._eleven_laps_provider = ElevenLapsProvider()
        models = {
            'karlsson': r'C:\Users\Markin\Workspace\piper_w\models\de_DE-karlsson-low.onnx',
            'pavoque': r'C:\Users\Markin\Workspace\piper_w\models\de_DE-pavoque-low.onnx',
            'hfc_female': r'C:\Users\Markin\Workspace\piper_w\models\en_US-hfc_female-medium.onnx',
            'kathleen': r'C:\Users\Markin\Workspace\piper_w\models\en_US-kathleen-low.onnx',
            'lessac': r'C:\Users\Markin\Workspace\piper_w\models\en_US-lessac-high.onnx',
            'ryan': r'C:\Users\Markin\Workspace\piper_w\models\en_US-ryan-high.onnx',
        }
        piper_path = os.getenv('PIPER_PATH', r'C:\Users\Markin\Workspace\piper_w\piper.exe')
        _piper_provider = PiperInterface(models=models, piper_path=piper_path, default_model_path=models['ryan'],
                                         verbose=False)
        self.app.print("simpel speech online")

        if not os.path.exists(f"{get_app(from_=f'{Name}.isaa.audio.get_data_dir').data_dir}/Audio/"):
            Path(f"{get_app(from_=f'{Name}.isaa.audio.get_data_dir').data_dir}/Audio/").mkdir(parents=True,
                                                                                              exist_ok=True)

    @export(mod_name=Name, initial=False)
    def init_speech(self, app: App = None):
        if app is None:
            app = get_app(from_=f"{Name}.init_speech")
        isaa = app.get_mod("isaa")
        isaa.speak = self.speech_stream
        print("speech initialized")

    @export(mod_name=Name, exit_f=True)
    def on_exit(self):
        if self._simpel_speech_recognizer is not None:
            self._simpel_speech_recognizer = None
        if self._simpel_speech_recognizer_mice is not None:
            self._simpel_speech_recognizer_mice = None
        if self._eleven_laps_provider is not None:
            self._eleven_laps_provider = None
        if self._piper_provider is not None:
            self._piper_provider = None

    @no_test
    def speech(self, text, voice_index=0, use_cache=True, provider='piper', config=None):
        if provider == 'eleven_labs' and self._eleven_laps_provider is not None:
            chucks = []
            if len(text) > 800:
                chucks = split_text_x_symbol(text)
            i = 0
            for chuck in chucks:
                print(f"Dobbing-{len(chuck)} chunk {i}/{len(chucks)}")
                i += 1
                if chuck:
                    if use_cache:
                        self._eleven_laps_provider.eleven_labs_speech_cache(chuck, voice_index)
                    else:
                        self._eleven_laps_provider.eleven_labs_speech(chuck, voice_index)
        if provider == 'piper' and self._piper_provider is not None:
            return self._piper_provider.text_to_speech(text, cache=use_cache, config=config)

    @no_test
    def speech_stream(self, text: str, voice_index=0, use_cache=True, provider='piper', config=None):
        chucks = []
        if not text:
            return False
        if text == self._most_recent_text_spoken_to_user_via_speech_stream_isaa_audio_:
            return False
        self._most_recent_text_spoken_to_user_via_speech_stream_isaa_audio_ = text

        if provider == 'eleven_labs':
            if len(text) > 800:
                chucks = split_text_x_symbol(text)
            i = 0
            for chuck in chucks:
                print(f"Dobbing-{len(chuck)} chunk {i}/{len(chucks)}")
                i += 1
                if chuck:
                    if use_cache:
                        self._eleven_laps_provider.eleven_labs_speech_cache(chuck, voice_index, cache=True)
                    else:
                        self._eleven_laps_provider.eleven_labs_speech_stream(chuck, voice_index)
        if provider == 'piper' and self._piper_provider is not None:
            return self._piper_provider.text_to_speech_stram(text, cache=use_cache, config=config)


@no_test
def transcript(model="jonatasgrosman/wav2vec2-large-xlsr-53-german",
               rate=16000, chunk_duration=10, amplitude_min=84, microphone_index=0):
    return init_live_transcript(model=model,
                                rate=rate, chunk_duration=chunk_duration,
                                amplitude_min=amplitude_min,
                                microphone_index=microphone_index)


@no_test
def wake_word(word="hey", variants=None,
              microphone_index=-1,
              amplitude_min=-1.,
              model="openai/whisper-medium",
              do_exit=True,
              do_stop=True, ques=None):
    if amplitude_min == -1:
        amplitude_min = s30sek_mean(seconds=10, microphone_index=3)
        print(amplitude_min)
    if ques is None:
        put, res_que = init_live_transcript(microphone_index=microphone_index,
                                            chunk_duration=5,
                                            amplitude_min=amplitude_min,
                                            model=model, rate=44100)  # openai/whisper-large-v3
    else:
        put, res_que = ques
    if variants is None:
        variants = []
    put("start")
    exit_variants = ["end", "exit"]
    stop_variants = ["pause", "secret", "pose", "geheim", "stop"]
    called = False
    text_ = ""
    while not called:
        data = res_que.get().lower()
        print(f"Wake detection : wat for {word} got {data}" + ' ' * 30, end='\r')
        do_brake = False
        for ev in exit_variants:
            if ev in data:
                do_brake = True
                break
        if do_brake:
            break
        for ev in stop_variants:
            if ev in data:
                put("stop")
                if 'y' in input('type y to continue'):
                    put("start")
                    continue
                break
        if word in data:
            called = True
            text_ = data.replace(word, '')
            break
        for ev in variants:
            if ev in data:
                called = True
                text_ = data.replace(ev, '')
                break
    if do_stop:
        put("stop")
    if do_exit:
        put("exit")
    return called, text_


@no_test
def transcript_stream():
    pass


if __name__ == "__main__":
    pass
    # on_start(get_app())
    # speech_stream("Hallo test 123")
    # print(wake_word(word="computer", variants=["isaa", "isa", "rechner", "pc"], microphone_index=3, amplitude_min=1.3))
