import ollama
from typing import Literal


def get_data_from_sprin(image_path: str, model: Literal['llama3.2-vision', 'llava-phi3', 'vision']) -> str:

    response = ollama.chat(
        model=model,
        messages=[
            {
                'role': 'system',
                'content': "Ton objectif est d'extraitre le titre et l'auteur d'un livre à partir d'une photo de sa côte. Répond de manière concise et efficace. Lorsque c'est impossible de lire les informations, renvoie 'Inconnu.'.",
            },
            {
                'role': 'user',
                'images': [image_path]
            }
        ]
    )

    output = response['message']['content'].strip()

    # remove all '\n' and replace them with a space
    output = output.replace('\n','').replace(';','\n').replace("Titre: ","").replace("Auteur: ","\n - \n").replace("Titre : ","").replace("Auteur : ","\n - \n").replace("Title: ","").replace("Author: ","\n - \n").replace("Title : ","").replace("Author : ","\n - \n")

    return output
