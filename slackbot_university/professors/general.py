#! /usr/bin/env python3
import sys
import wikipedia
from typing import List
from . import Professor

TEXT_LENGTH_LIMIT = 1000


class GeneralProfessor(Professor):

    def answer_short(self, text: str):
        return main(text) 

    def is_mine(self, text: str):
        text = text.strip().lower()
        return (
            text.startswith("ts ")
            or text.startswith("trans ")
            or text.startswith("tr ")
        )

    def is_default(self):
        return True

def summary(text: str):
    try:
        summary = wikipedia.summary(text)
        first_line = summary.splitlines()[0]
        first_line_limited = first_line[:TEXT_LENGTH_LIMIT]
        return first_line_limited
    except Exception:
        return ""


def search(text: str) -> List[str]:
    try:
        page_names = wikipedia.search(text)
        return page_names
    except Exception:
        return []


def main(text):
    text_summaried = summary(text)
    if text_summaried:
        return text_summaried
    list_names_found = search(text)
    if list_names_found:
        text_output = (
            f"No found for {text}\n"
            f"Do you mean: \n\t"
        )
        text_output += "\n\t".join(list_names_found)
        return text_output
    return ""


if __name__=="__main__":
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        raise ValueError(
                "No input string\n"
                "Usage: wiki text"
                )
    result_wiki = main(text)
    print(result_wiki)
