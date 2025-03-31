import ollama
from typing import Literal
import re

def get_data_from_sprin(image_path: str, model: Literal['llama3.2-vision', 'llava-phi3', 'vision']) -> str:

    response = ollama.chat(
        model=model,
        messages=[
            {
                'role': 'system',
                'content': "Ton objectif est d'extraitre le titre, sous-titre et l'auteur d'un livre STRICTEMENT à partir d'une photo de sa côte, juste en y lisant les caractères inscrits. Répond de manière concise et efficace. Lorsque c'est impossible de lire les informations, renvoie 'Inconnu.'.",
            },
            {
                'role': 'user',
                'images': [image_path]
            }
        ]
    )

    output = response['message']['content'].strip()

    # remove all '\n' and replace them with a space
    output = output.replace('\n',' - ').replace(';',' - ').replace("Titre: ","").replace("Auteur: "," - ").replace("Titre : ","").replace("Auteur : "," - ").replace("Title: ","").replace("Author: "," - ").replace("Title : ","").replace("Author : "," - ").replace(" by "," - ").replace(" par "," - ")
    output = re.sub(r'Note:.*', '', output)
    output = re.sub(r'Note :.*', '', output)
    output = output.replace('- -','-')
    return output
