#%% Imports
from dspy.signatures import OutputField
import ollama
import dspy
from typing import Literal 

#%% Test ollama
Input_Folder = "./book_masks/"
IMAGES_TEST = [
        "./book_masks/book_4.jpg",
        "./book_masks/book_7.jpg",
        "./book_masks/book_5.jpg",
        "./book_masks/book_6.jpg",
        "./book_masks/book_9.jpg",
        "./book_masks/book_8.jpg"
        ]

number_Of_Books = len(IMAGES_TEST)

# response = ollama.chat(
#         model='llava-phi3',
#         # model='gemma3:4b',
#         messages=[
#             {
#                 'role': 'user',
#                 'content': f'Give me the title and author of each book (those image are the side of the books). Return the result as a json. There is only one book by image, for a total of {number_Of_Books} books.',
#                 'images': IMAGES_TEST
#                 }]
#             )
# print(response)



for image in IMAGES_TEST:
    print(f"Image: {image}")
    response = ollama.chat(
            # model='llama3.2-vision',
            # model='granite3.2-vision',
            # model='minicpm-v',
            model='llava-phi3',
            # model='gemma3:4b',
            # model='deepseek-r1:8b',
            messages=[
                # message de contexte

                # {
                #     'role': 'system',
                #     'content': "Your task is to extract the title and author of each book picture I'll show you. Each image is a side of a book. If you can't find the title or author, just say 'Unkown'. I want an output as a json with only those two fields: 'title(s)' and 'author'.",
                #
                #     },
                {
                'role': 'user',
                # 'content': 'Give me the title and author of each book (those images are the side of books). Return the result as a json. Hint: you may be unable to find the title or author of some books. In that case, just say "Unknown".',
                'content': 'Give me the title and author of this book (this is the side of the book). Return the result as a json. Hint: you may be unable to find the title or author of some books. In that case, just say "Unknown". There is only one book by this image.',
                'images': [image]
                }]
            )


    print(response)


# Vérifiez que les images sont accessibles
#%% Test dspy
Model_Name = 'ollama/llama3.2-vision'
Model_Name  = 'ollama/minicpm-v'
Model_Name  = 'ollama/llava-phi3'

lm = dspy.LM(Model_Name, api_base="http://localhost:11434", api_key="")
dspy.configure(lm=lm)


# create a signature for finding book titles and authors of the image of side of a book
class BookTitleAuthor(dspy.Signature):
    """
    book_slice : input image(s)
    book_title: title of the book
    book_author: author of the book
    confidence: confidence
    """
    book_slice = dspy.InputField(type="image")
    book_Title: str = dspy.OutputField(desc="the title of the book")
    book_author: str = dspy.OutputField(desc="the name of the author of the book")
    confidence: float = OutputField()

from PIL import Image
image = Image.open(IMAGES_TEST[0])

# classify = dspy.Predict(BookTitleAuthor)
# print(classify(book_slice=image))

