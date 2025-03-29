import streamlit as st
from PIL import Image, ImageDraw
from src.get_masks import get_boxes_and_masks
import os
import numpy as np
from mistralai import Mistral
import cv2

# CONFIG
if "selected_index" not in st.session_state:
    st.session_state.selected_index = None
st.set_page_config(page_title="LivrIA", page_icon="📚")
with open("src/style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

output_folder = "tmp/"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# FONCTIONS
def convert_image_to_pdf(image_file, pdf_file):
    image = Image.open(image_file)
    if image.mode != "RGB":
        image = image.convert("RGB")
    image.save(pdf_file)

def extract_text_from_mask(mask_path):
    api_key = "CYbXnj1pSLnTvGNVYE8rv3JXpkT43yLj"
    client = Mistral(api_key=api_key)

    pdf_file = mask_path.replace(".jpg", ".pdf")
    convert_image_to_pdf(mask_path, pdf_file)

    uploaded_pdf = client.files.upload(
        file={
            "file_name": pdf_file,
            "content": open(pdf_file, "rb"),
        },
        purpose="ocr"
    )

    signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": signed_url.url,
        }
    )

    if ocr_response.pages:
        return ocr_response.pages[0].markdown
    return "Texte non détecté"


def highlight_book(image, boxes, selected_index=None):
    draw = ImageDraw.Draw(image)
    for i, box in enumerate(boxes):
        color = "red" if i == selected_index else "white"
        draw.polygon(box.flatten().tolist(), outline=color, width=4)
    return image

# LOGO CENTRAL
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("src/logo livria.png",width=300)



# APP PRINCIPALE
_, center, _ = st.columns(3)
with center:
    photo = st.file_uploader(label="Sélectionner une photo de bibliothèque", label_visibility="visible")



left, right = st.columns([0.3,0.7], vertical_alignment='center',gap='medium')
if photo is not None:
        # on convertit l'image uploadée par l'utilisateur dans le format compris par notre modèle
        img = Image.open(photo)
        img_path = os.path.join(output_folder, photo.name)
        img.save(img_path)

        # récupération de tous les masques de livre de l'image
        boxes, masks = get_boxes_and_masks(img_path)

with left:
    if photo is not None:
        highlighted_image = highlight_book(img, boxes,selected_index=st.session_state.selected_index)
        st.image(highlighted_image)
with right:
    if photo is not None:
        st.subheader("Livres détectés :")
        cols = st.columns(6)
        for i, mask in enumerate(masks):
            with cols[i % 6]:
                # sauvegarde du mask
                mask_path = os.path.join(output_folder, f"mask_{i}.jpg")
                cv2.imwrite(mask_path, mask)

                #with st.spinner("Lecture du texte..."):
                    #text = extract_text_from_mask(mask_path)    # RECHECK LE FORMAT DE SORTIE ET LIMITE DE L'API
                text = "livre"
                if st.button(text, key=f"button_{i}"):
                    st.session_state.selected_index = i
                    st.rerun()



