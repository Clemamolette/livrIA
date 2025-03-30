import ollama
from typing import Literal


def get_data_from_sprin(image_path: str, model: Literal['llama3.2-vision', 'llava-phi3', 'vision']) -> str:

    response = ollama.chat(
        model=model,
        messages=[
            {
                'role': 'system',
                'content': "Your task is to extract the title and author of a book spine. If you can't find the title or author, just say 'Unkown'. Your answer ***MUST*** be in the format 'title: ... \n\nauthor: ...'.",
            },
            {
                'role': 'user',
                'images': [image_path]
            }
        ]
    )

    output = response['message']['content'].strip()

    # remove all '\n' and replace them with a space
    output = output.replace('\n', ' ')

    return output
