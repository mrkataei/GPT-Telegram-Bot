import json
from pathlib import Path

_lang = 'fa'
DEFINITION_PATH = f'{Path(__file__).parent.resolve()}/definitions.json'


def activate(lang):
    global _lang
    _lang = lang


def get_lang():
    return _lang


with open(DEFINITION_PATH) as defi:
    TRANSLATIONS = json.load(defi)


def trans(string: str) -> str:
    return TRANSLATIONS[string][_lang]
