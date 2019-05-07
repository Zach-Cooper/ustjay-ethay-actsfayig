"""
    Mashup that returns random fact in pig latin
"""

import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    """
        Retrieves random fact from unkno.com
        :return: random fact in string format
    """

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    formatted_facts = facts[0].getText()

    return formatted_facts


def get_pig_latin(fact):
    """
        Translates random fact from unkno.com into pig latin and get new url
        :param: fact string
        :return: url for pig latin translation 
    """
    url = "https://hidden-journey-62459/herokuapp.com/piglatinize/"
    payload = {"input_text": fact}

    translate_url = requests.post(url, data=payload, allow_redirects=False)
    new_page = translate_url.headers["Location"]

    return new_page


def get_translation(get_pig_latin):
    """
        Return pig latin translation
        :param: url translation from get_pid_latin function
        :return: string of pig latin translated
    """
    response = requests.get(get_pig_latin)
    soup = BeautifulSoup(response.content, "html.parser")

    fact_translated = soup.find("body").getText()
    fact_translated_stripped = fact_translated.resplace("Pig Latin\nEsultry", "")

    return fact_translated_stripped


@app.route('/')
def home():
    """
        Pig Latin Web app home page
        :return: random fact url
    """
    fact = get_fact().strip()

    get_new_page = get_pig_latin(fact)

    translation = get_translation(get_new_page)

    return translation


# def home_page():
#     """
#         Format for home page
#         :return: HTML template
#     """

#     html_page = """<html>
#     <head>
#     <title>Random Fact in Pig Latin</title>
#     </head>
#     <body>

#         <h1>Random Fact in Pig Latin Generator</h1>
#         <p>{}</p>
#         <p>Thanks for visiting!!!</p>

#     </body>
#     </html>"""

#     return html_page


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
