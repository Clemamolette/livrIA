import streamlit as st
from PIL import Image
from src.get_masks import get_masks
import os

# CONFIG
st.set_page_config(page_title="LivrIA", page_icon="📚")
with open("src/style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

output_folder = "uploaded_images/"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# LOGO CENTRAL
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("src/logo livria.png",width=300)



# APP PRINCIPALE
_, center, _ = st.columns(3)
with center:
    photo = st.file_uploader(label="Sélectionner une photo de bibliothèque", label_visibility="visible")

left, right = st.columns([0.3,0.7], vertical_alignment='center',gap='medium')
with left:
    if photo is not None:
        st.image(photo)
with right:
    if photo is not None:
        # on convertit l'image uploadée par l'utilisateur dans le format compris par notre modèle
        img = Image.open(photo)
        img_path = os.path.join(output_folder, photo.name)
        img.save(img_path)

        # récupération de tous les masques de livre de l'image
        masks = get_masks(img_path)

        st.subheader("Livres détectés :")
        cols = st.columns(6)
        for i, mask in enumerate(masks):
            with cols[i % 6]:
                st.image(mask)
                st.markdown(
                    f"""
                    <div class="livre">
                        <strong>Titre - Auteur</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
