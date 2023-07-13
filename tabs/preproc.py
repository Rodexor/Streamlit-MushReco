import streamlit as st
from app_lib.widgets import select_gallery
from app_lib.utils import format_class_name,preproc,change_number,vspace
import toml
import os
from app_lib.widgets import select_buttons
from PIL import Image
from rembg import remove
import io
from streamlit_toggle import st_toggle_switch

title = "Preprocessing"
sidebar_name = "Preprocessing" 

config_params=toml.load(".streamlit/config.toml")["theme"]

def run(paths):

    
    st.image(os.path.join(os.path.join(os.getcwd(),"static"),"rembg_screen.png"),use_column_width=True)
    st.markdown(f"<h1 style='text-align: center;'>Preprocessing avec Rembg</h1>",unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center;'>Veuillez sélectionner une image prédéfinie ou télécharger une image de votre choix !</div>",unsafe_allow_html=True)

    vspace(3)
    
    with st.expander("Séléctionner une image"):     
        with st.columns((0.25,0.5,0.25))[1]:
            st.button("SHUFFLE", on_click=change_number,use_container_width=True)
        entities=paths["crop"].groupby('class').nth(0)
        options=[format_class_name(x) for x in entities["class"]]
        selected_class=select_gallery(options=options,
                                       main_key="galery_datset",
                                       paths=entities["path"],
                                       n_cols=4,
                                       border_width=10,
                                       border_colors=[config_params["backgroundColor"],config_params["primaryColor"]],
                                       radius=50,
                                       overlay=config_params["primaryColor"]+"44",
                                       unselect=False,
                                       default=0
                                       )    
                
        classe = entities["class"].to_list()[options.index(selected_class)]   
        selected_image=Image.open(paths["simple"][paths["simple"]["class"]==classe]["path"].iloc[0])
        
    # Render the dropzone component
    fil = st.file_uploader(label="Télécharger votre image", type=['png', 'jpg', 'jpeg'])
        # Check if a file was uploaded
    if fil is not None:
            # Display the uploaded image
        img = Image.open(fil)
            
        switch=st_toggle_switch(label="use uploaded image",default_value=True,
                                    inactive_color="#838383",
                                    active_color="#DF7F5F",
                                    track_color="#FF9F7F"
                                    )
        if switch:
            selected_image=img
    
    st.divider()
    
    preview_columns=st.columns(2)
    with preview_columns[0]:
        st.image(selected_image,caption='Image séléctionné',use_column_width=True)
    
    button_cols=st.columns(2)
    with button_cols[0]:
        switch_crop=st_toggle_switch(label="Square Crop",
                        key="switch_crop",
                        default_value=False,
                        label_after=False,
                        inactive_color=config_params["secondaryBackgroundColor"],
                        active_color=config_params["primaryColor"],
                        track_color="#29B5E8",  # optional
                    )
    with button_cols[1]:
        rembg_button=st.button("Rembg !",key="rembg_button",use_container_width=True)


    if rembg_button:
        img_mask = remove(selected_image, only_mask=True)
        with preview_columns[1]:
            st.image(img_mask,caption="Sortie de Rembg",use_column_width=True)
    
        
        subtabs=st.tabs(["Détouré","Noir","Flouté","Bruité","Flouté et bruité"])
        preproc_imgs=preproc(selected_image,img_mask,st.session_state.switch_crop)
        
        filenames=["detoure.png","black.png","blurr.png","noisy.png","blurr_noise.png"]
        for i,tab in enumerate(subtabs):
            with tab:
                # Créer un flux d'image PNG
                png_data = io.BytesIO()
                preproc_imgs[i].save(png_data, format='PNG')
                png_data.seek(0)
                with st.columns([0.25,0.5,0.25])[1]:
                    # Ajouter un bouton de téléchargement
                    st.download_button(
                        label='Télécharger',
                        data=png_data,
                        file_name=filenames[i],
                        mime='image/png',
                        use_container_width=True
                    )
                    st.image(preproc_imgs[i],use_column_width=True)
