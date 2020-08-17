#! /usr/bin/env python3
"""Usage: translator text"""
import sys
from googletrans import Translator
from typing import Optional, Dict, NamedTuple, Tuple

from . import Professor

LANGS_PREFERENCE = {"vi", "fr", "en"} 
TRANSLATOR = Translator()


class LanguageProfessor(Professor):

    def answer_short(self, text: str):
        if self.is_mine(text):
            text = self.parse_text(text)
        return main(text) 

    def is_mine(self, text: str):
        text = text.strip().lower()
        return (
            text.startswith("ts ")
            or text.startswith("trans ")
            or text.startswith("tr ")
        )

    def parse_text(self, text):
        first_word, text = text.split(" ", 1)
        return text


def detect_lang(text: str) -> Optional[str]:
    try:
        res = TRANSLATOR.detect(text)
        return res.lang
    except Exception:
        return None


def translate(text, src, dest) -> Tuple[str, str]:
    """Return text_translated, possible_correction"""
    try:
        res = TRANSLATOR.translate(
                text, src=src, dest=dest)
        if res.extra_data["possible-mistakes"]:
            correction = res.extra_data["possible-mistakes"][1]
        else:
            correction = ""
        return res.text, correction
    except Exception:
        return "", ""


def translate_to_multi_langs(text, src: str) -> Dict[str, str]:
    language_dests = LANGS_PREFERENCE - {src}
    texts_translated = {}
    for dest in language_dests:
        text_translated, correction = translate(text, src, dest)
        if not text_translated:
            break
        texts_translated[dest] = text_translated
        texts_translated["correction"] = correction
    return texts_translated


def format_result(dict_translation: Dict[str, str]) -> str:
    """ Convert translation result to string """
    languages_translated = [
            lang for lang in dict_translation if lang != "correction"
    ]
    output_lines = []
    for language in languages_translated:
        text_translated = dict_translation[language]
        line = f"[{language}] {text_translated}"
        output_lines.append(line)
    correction = dict_translation.get("correction", "")
    if correction:
        line = f"Possible correction: {correction}"
        output_lines.append(line)
    return "\n".join(output_lines)


def main(text: str) -> Dict[str, str]:
    try:
        language_src = detect_lang(text)
        if language_src not in LANGS_PREFERENCE:
            language_srcs = LANGS_PREFERENCE
        else:
            language_srcs = [language_src]
        dict_translation = {}
        for language_src in language_srcs:
            dict_translation = translate_to_multi_langs(
                text, language_src        
            )
            if dict_translation:
                break

        return format_result(dict_translation)
    except Exception:
        import traceback; traceback.print_exc()
        return ""


if __name__=="__main__":
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        raise ValueError(
                "No string to translate\n"
                "Usage: translator text"
                )
    result_translated = main(text)
    print(result_translated)
