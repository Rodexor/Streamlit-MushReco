import streamlit as st
import toml
from PIL import Image
from app_lib.widgets import display_gallery,select_gallery
from streamlit_extras.toggle_switch import st_toggle_switch
from app_lib.utils import format_class_name,get_max_value,make_gradcam_heatmap,save_and_display_gradcam,preproc,change_number,vspace,get_first_paragraph_wiki,get_page_wiki
from app_lib.data_loaders import loading_model,classe_list
import numpy as np
from rembg import remove

config_params=toml.load(".streamlit/config.toml")["theme"]

title ="Résultats"
sidebar_name="Résultats"

def run(paths):
    #-----------------------------------------
    #PREDICTIONS
    st.markdown(f"<h1 style='text-align: center;'>Testez notre modèle à 12 espèces!</h1>",unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center;'>Veuillez sélectionner une image prédéfinie ou télécharger une image de votre choix !</div>",unsafe_allow_html=True)

    vspace(3)

    model_simple=loading_model('assets/Model/model_opti.h5')
    model_crop=loading_model('assets/Model/model_crop.h5')
    model_noir=loading_model('assets/Model/model_fond_noir.h5')
    model_flou=loading_model('assets/Model/model_fond_flou.h5')
    model_noise=loading_model('assets/Model/model_noise.h5')
    model_noise_blur=loading_model('assets/Model/model_noise&blur.h5')


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

    #----------------------------------------------
    #A CODE THAT PRODUCES 3 class names and the probabilites

    cols=st.columns(2)
    with cols[0]:
        st.image(selected_image,caption="image originale",use_column_width=True)
        
    mod_list=["Simple",
                  "Crop",
                  "Black",
                  "Blurr",
                  "Noise",
                  "Noisy Blurr"
                  ]

    selected_model=st.selectbox("Choix du modèle et du type du traitement de l'image",mod_list)
    preproc_imgs=preproc(selected_image,remove(selected_image, only_mask=True),square_crop=True)
        
    if selected_model=="Simple":
        mod=model_simple
    elif selected_model=="Crop":
        selected_image=preproc_imgs[5]
        mod=model_crop
    elif selected_model=="Black":
        selected_image=preproc_imgs[1]
        mod=model_noir
    elif selected_model=="Blurr":
        selected_image=preproc_imgs[2]
        mod=model_flou
    elif selected_model=="Noise":
        selected_image=preproc_imgs[3]
        mod=model_noise
    elif selected_model=="Noisy Blurr":
        selected_image=preproc_imgs[4]
        mod=model_noise_blur
        
    with cols[1]:
        st.image(selected_image,caption="image d'entrée",use_column_width=True)
        
    classes_list,index=classe_list("assets/data_test/data_bb")

    if st.button("Predict",use_container_width=True):
        img_sec=np.array(selected_image)
        img_bis=selected_image.resize(size=(224,224))
        img_bis=np.array(img_bis)
        img_bis=np.expand_dims(img_bis, axis=0)
        img_bis=img_bis/255
        heatmap=make_gradcam_heatmap(img_bis,mod)
        grad_cam=save_and_display_gradcam(img_sec, heatmap, alpha=0.5)
        pred=mod.predict(img_bis)
        index_list,value=get_max_value(pred)
        proba_glob=[round(elem*100,2) for elem in value]
        proba = max(proba_glob)
        names=[]
        for i in index_list:
            names.append(classes_list[index.index(i)])
        if proba<=50:
            st.write("Probabilité maximal inférieur à 50 % , votre image n'est probablement pas un champignon")
        elif proba >50:
            st.header(format_class_name(names[0])+" - " +str(proba_glob[0])+'%')
            st.subheader(format_class_name(names[1])+" - " +str(proba_glob[1])+'%')
            st.subheader(format_class_name(names[2])+" - " +str(proba_glob[2])+'%')      
    
    #----------------------------------------------
            
        st.markdown('----')
        st.markdown("<h4 style='text-align: center;'>Images des 3 classes les plus probables </h4>",unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs([format_class_name(names[0]),
                                        format_class_name(names[1]),
                                        format_class_name(names[2])
                                        ])
        imgs_1=paths["simple"][paths["simple"]["class"]==names[0]]["path"].iloc[1:7]
        imgs_2=paths["simple"][paths["simple"]["class"]==names[1]]["path"].iloc[1:7]
        imgs_3=paths["simple"][paths["simple"]["class"]==names[2]]["path"].iloc[1:7]

        with tab1:
            display_gallery(imgs_1,
                            3,
                            border_width=5,
                            border_color=config_params["primaryColor"],
                            radius=25)
            with st.expander("Extrait de Wikipedia"):
                st.write("Source: [{}]({})".format(get_page_wiki(names[0]),get_page_wiki(names[0])))                
                st.write("<p style='text-align: justify;'>"+get_first_paragraph_wiki(names[0])+"</p>",
                         unsafe_allow_html=True)
        with tab2:
            display_gallery(imgs_2,
                            3,
                            border_width=5,
                            border_color=config_params["primaryColor"],
                            radius=25)
            with st.expander("Extrait de Wikipedia"):
                st.write("Source: [{}]({})".format(get_page_wiki(names[1]),get_page_wiki(names[1])))                
                st.write("<p style='text-align: justify;'>"+get_first_paragraph_wiki(names[1])+"</p>",
                         unsafe_allow_html=True)
        with tab3:
            display_gallery(imgs_3,
                            3,
                            border_width=5,
                            border_color=config_params["primaryColor"],
                            radius=25)
            with st.expander("Extrait de Wikipedia"):
                st.write("Source: [{}]({})".format(get_page_wiki(names[2]),get_page_wiki(names[2])))                
                st.write("<p style='text-align: justify;'>"+get_first_paragraph_wiki(names[2])+"</p>",
                         unsafe_allow_html=True)

        st.markdown('----')
        st.markdown("<h4 style='text-align: center;'>GradCam </h4>",unsafe_allow_html=True)
        st.write("La grad cam est un dispositif, permettant d'interpréter notre modèle en affichant les principales zones d'activation.")
        cols = st.columns((0.1,0.8,0.1))
        if grad_cam is not None:
                with cols[1]:
                    st.image(grad_cam,use_column_width=True)
