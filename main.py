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
    fact = soup.find_all("div", id="content")

    formatted_fact = fact[0].getText()

    return formatted_fact


def get_pig_latin(formatted_fact):
    """
        Translates random fact from unkno.com into pig latin and get new url
        :param: fact string
        :return: url for pig latin translation
    """
    url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"
    payload = {"input_text": formatted_fact}

    translate_url = requests.post(url, data=payload, allow_redirects=False)
    translate_new_page = translate_url.headers["Location"]

    return translate_new_page


def get_translation(translate_new_page):
    """
        Return pig latin translation
        :param: url translation from get_pid_latin function
        :return: string of pig latin translated
    """
    response = requests.get(translate_new_page)
    soup = BeautifulSoup(response.content, "html.parser")

    translated_fact = soup.find("body").getText().replace("Pig Latin", " ").replace("Esultray", " ")

    return translated_fact


@app.route('/')
def home():
    """
        Pig Latin Web app home page
        :return: random fact url
    """
    fact = get_fact().strip()

    get_new_page_url = get_pig_latin(fact)

    translation = get_translation(get_new_page_url)

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
