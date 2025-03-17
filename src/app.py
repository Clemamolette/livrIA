import streamlit as st
import base64

st.set_page_config(page_title="LivrIA", page_icon="📚")
with open("src/style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)



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
    