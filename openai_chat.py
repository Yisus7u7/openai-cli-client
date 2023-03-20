#!/usr/bin/env python

import openai
import readline
import configparser
from time import sleep
from xdg.BaseDirectory import xdg_config_home
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

# Creador: Jesús Chapman (Yisus7u7)

user_config = xdg_config_home

config = configparser.ConfigParser()

try:
    config.read(f"{user_config}/openai_client.conf")
    api_token = config.get('openai', 'token')

except configparser.NoSectionError:
    print("Error: File does not exist ~/.config/openai_client.conf")
    print("Creating a new configuration file...\n")
    sleep(3)

    user_token = input("Enter your token ==> ")

    config["openai"] = {
            "token": user_token
        }
    with open(f"{user_config}/openai_client.conf", "w") as archivo_config:
        config.write(archivo_config)

    print("Finished, you can edit your token by editing ~/.config/openai_client.conf")
    exit(1)

openai.api_key = api_token

class ChatSession:
    def __init__(self):
        self.history = []

    def remember(self, message):
        self.history.append(message)

    def respond(self, message):
        self.remember(message)
        model_engine = "text-davinci-002"
        prompt = " ".join(self.history)
        completions = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = completions.choices[0].text
        self.remember(message)
        return message

session = ChatSession()

print("""
      Welcome to OpenAI Chat CLI !\n

Source code => github.com/Yisus7u7/openai-cli-client
Creator => Yisus7u7 
Version => 1.0-stable

write \"exit()\" to exit chat
      """)

while True:
    message = input("You: ")

    if message == "exit()":
        print("Leaving...")
        exit(0)

    response = session.respond(message)
    
    # Resaltar la sintaxis de la respuesta usando Pygments
    highlighted_response = highlight(response, PythonLexer(), TerminalFormatter())

    # Imprimir la respuesta del modelo resaltada
    print("OpenAI: \n" + highlighted_response)
