import streamlit as st

# this because it crash otherwise
import torch
import os
torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)]


from PIL import Image, ImageDraw
from src.get_masks import get_boxes_and_masks
from src.ocr import get_data_from_sprin
import os
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
@st.cache_data(show_spinner=False)
def extract_text_from_mask(mask_path):
    model = ""
    if model_selected.startswith("Minicpm"):
        model = "minicpm-v"
    elif model_selected.startswith("Llava-phi3"):
        model = "llava-phi3"
    elif model_selected.startswith("Llama3.2-vision"):
        model = "llama3.2-vision"
    else:
        raise ValueError("Modèle non reconnu")

    return get_data_from_sprin(mask_path, model)


def highlight_book(image, boxes, selected_index=None):
    draw = ImageDraw.Draw(image)
    for i, box in enumerate(boxes):
        color = "red" if i == selected_index else "white"
        draw.polygon(box.flatten().tolist(), outline=color, width=4)
    return image


# LOGO CENTRAL
left_co, cent_co, last_co = st.columns(3)
with cent_co:
    st.image("src/logo livria.png", width=300)

# APP PRINCIPALE
_, center, select = st.columns(3, gap='large')
with center:
    photo = st.file_uploader(
        label="Sélectionner une photo de bibliothèque", label_visibility="visible")
with select:
    model_selected = st.selectbox(
        "Choisissez le modèle d'OCR à utiliser :",
        ("Minicpm - rapide mais peu précis", "Llava-phi3 - assez lent mais plus précis", "Llama3.2-vision - très lent mais très précis"),
        placeholder="Modèle d'OCR à sélectionner",
        index=None
    )


left, right = st.columns([0.3, 0.7], vertical_alignment='center', gap='medium')
if photo is not None and model_selected is not None:
    # on convertit l'image uploadée par l'utilisateur dans le format compris par notre modèle
    img = Image.open(photo)
    img_path = os.path.join(output_folder, photo.name)
    img.save(img_path)

    # récupération de tous les masques de livre de l'image
    boxes, masks = get_boxes_and_masks(img_path)

with left:
    if photo is not None and model_selected is not None:
        highlighted_image = highlight_book(img, boxes, selected_index=st.session_state.selected_index)
        st.image(highlighted_image)

with right:
    if photo is not None and model_selected is not None:
        st.subheader("Livres détectés :")
        cols = st.columns(6)
        for i, mask in enumerate(masks):
            with cols[i % 6]:
                # sauvegarde du mask
                mask_path = os.path.join(output_folder, f"mask_{i}.jpg")
                cv2.imwrite(mask_path, mask)

                with st.spinner("Lecture du texte..."):
                    text = extract_text_from_mask(mask_path)
                if st.button(text, key=f"button_{i}"):
                    st.session_state.selected_index = i
                    st.rerun()
