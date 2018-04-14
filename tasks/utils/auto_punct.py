import os, json
import requests
from requests.exceptions import RequestException

class AutoPunct:
    AUTO_PUNCT_URL = os.environ.get('AUTO_PUNCT_URL', '')

    @classmethod
    def get_punct_text(cls, text):
        payload = [{'src': text}]
        try:
            r = requests.post(cls.AUTO_PUNCT_URL, json=payload)
            response = r.json()
            return response[0][0]
        except RequestException:
            return None
        except ValueError:
            return None
    
    PUNCT_CHARACTERS = '：，。；、！“”‘’？\n'
    @classmethod
    def extract_punct(cls, punct_text):
        pos = 0
        punct_lst = []
        for ch in punct_text:
            if ch in cls.PUNCT_CHARACTERS:
                punct_lst.append( (pos, ch) )
            else:
                pos += 1
        return punct_lst

    @classmethod
    def get_puncts(cls, text):
        punct_text = cls.get_punct_text(text)
        return cls.extract_punct(punct_text)

    @classmethod
    def get_puncts_str(cls, text):
        puncts = cls.get_puncts(text)
        return json.dumps(puncts, separators=(',', ':'))
