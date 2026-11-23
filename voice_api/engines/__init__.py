from .pidgin_mms import PidginMmsEngine

_SPEECH_ENGINES = {}


def _register(engine):
    for language in engine.languages:
        _SPEECH_ENGINES[language] = engine


_register(PidginMmsEngine())


def get_speech_engine(language):
    return _SPEECH_ENGINES.get(language)


def speech_languages():
    return sorted(_SPEECH_ENGINES)
