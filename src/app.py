import streamlit as st
from PIL import Image
from src.get_masks import get_masks
import os

st.set_page_config(page_title="LivrIA", page_icon="📚")
with open("src/style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


output_folder = "uploaded_images/"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

primary_color = 'rgb(89, 24, 178)'

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("src/logo livria.png",width=300)


left, right = st.columns(2, border=True)
with left:
    st.markdown("Sélectionner une photo de votre bibliothèque")
    photo = st.file_uploader(label='')
with right:
    st.markdown("Image")
    if photo is not None:
        st.image(photo)

_, cent, _ = st.columns(3)
with cent:
    if photo is not None:
        st.markdown("La machine travaile ...")
        st.image('src/cat-cute.gif')

        # on convertit l'image uploadée par l'utilisateur dans le format compris par notre modèle
        img = Image.open(photo)
        img_path = os.path.join(output_folder, photo.name)
        img.save(img_path)

        # récupération de tous les masques de livre de l'image
        masks = get_masks(img_path)
        for mask in masks:
            st.image(mask)

