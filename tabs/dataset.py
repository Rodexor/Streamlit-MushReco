import streamlit as st
import random
from app_lib.widgets import select_gallery
from app_lib.utils import format_class_name,get_first_paragraph_wiki,get_page_wiki,change_number
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import toml
import os



# recuperartion des couleur de la page pour passer des coleurs coherentes
# au widgets personalisés
config_params=toml.load(".streamlit/config.toml")["theme"]
# exemple ci-dessous
# config_params["primaryColor"]
# config_params["backgroundColor"]
# config_params["secondaryBackgroundColor"]

title = "Le jeu de données en bref"
sidebar_name = "Données" 
def run(paths,df_filtered): 
    # initializing with a random number
    if "rn" not in st.session_state:
        st.session_state["rn"] = random.randint(1,100)
        
    random.seed(st.session_state.rn)
    
    #LAYOUT
    with st.columns(3)[1]:
        st.image(os.path.join(os.path.join(os.getcwd(),"static"),"logo_mushroom_observer.png"),use_column_width=True)
    st.markdown("""
            <h1 style='text-align: center;'>Jeu de données</h1>
            """,
            unsafe_allow_html=True
            )

    tab1, tab2, tab3,tab4 = st.tabs(["Gallerie", "Filtre Metadonnées", "Filtre Nombre d'Images","Dataframe"])
    
    with tab1:
        with st.columns((0.25,0.5,0.25))[1]:
            st.button("SHUFFLE", on_click=change_number,use_container_width=True)
        gallery_1=st.columns(1)
        wiki=st.expander("Extrait de Wikipedia")
        
    with tab2:
        st.subheader('Filtrez selon les metadonnées des images')    
        options1=st.columns(3)
        pies1=st.columns(3)
        options2=st.columns(3)
        pies2=st.columns(3)
    
    with tab3:
        st.subheader("Filtrez selon le taxon classifiant et le nombre d'images par classes")
        options3=st.columns(2)
        st.subheader("Nombre d'images par classe")
        distributions=st.columns(2)
 
    
    #CALCULATIONS
    with gallery_1[0]:         
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
        
        selected_class = entities["class"].to_list()[options.index(selected_class)]
    with wiki:
        st.write("Source: [{}]({})".format(get_page_wiki(selected_class),get_page_wiki(selected_class)))
        st.write("<p style='text-align: justify;'>"+get_first_paragraph_wiki(selected_class)+"</p>",
                    unsafe_allow_html=True)
    
    with options1[0]:
        selected_countries = st.multiselect('Pays',
                                            ['Tous']+list(df_filtered['country'].value_counts().index),
                                            default='Tous',
                                            )
        if 'Tous' in selected_countries:
            selected_countries = list(df_filtered['country'].unique())
    
    with options1[1]:    
        selected_phylum = st.multiselect('Phylum',
                                            ['Tous']+list(df_filtered['phylum'].value_counts().index),
                                            default='Tous'
                                            )
        if 'Tous' in selected_phylum:
            selected_phylum = list(df_filtered['phylum'].unique())
            
    with options1[2]:    
            ranks=[1,2,3,4,5,6,7,8,9,10,11,12,13]
            taxon_list=['1-form',
                        '2-variety',
                        '3-subspecies',
                        '4-species',
                        '5-stirps',
                        '6-subsection',
                        '7-section',
                        '8-subgenus',
                        '9-genus',
                        '10-family',
                        '11-order',
                        '12-class',
                        '13-phylum']
            selected_taxon = st.multiselect('Taxons', 
                                            ['Tous']+taxon_list, 
                                            default='Tous'
                                            )
            #selected_taxon = [selected_taxon] if isinstance(selected_taxon, str) else selected_taxon
            if 'Tous' in selected_taxon:
                filter_ranks=ranks
                selected_taxon = taxon_list
            else:
                filter_ranks=[]
                for taxon in selected_taxon:
                    filter_ranks.append(ranks[taxon_list.index(taxon)])
    
    with options2[0]:
        min_votes = st.slider('Minimum de votes',
                                min_value=0,
                                max_value=int(df_filtered['vote_cache'].max()),
                                step=1
                                )
        
    with options2[1]:
        selected_formats = st.multiselect('Formats d\'image',
                                            ['Tous']+list(df_filtered['content_type'].value_counts().index),
                                            default='Tous')
        if 'Tous' in selected_formats:
            selected_formats = list(df_filtered['content_type'].unique())
            
    with options2[2]:
            labels = ["VLD","LD",'SD', 'HD Ready', 'Full HD', '4k', '8k+']
            bins = [0,480*360, 720 * 480, 1280 * 720, 1920 * 1080, 3840 * 2160, 7680 * 4320,1e10]
            min_resol = st.selectbox('Minimum de résolution', labels, index=0)
            min_res=bins[labels.index(min_resol)]
            
    # Filtrer les données en fonction des options sélectionnées
    df_filtered = df_filtered[(df_filtered['country'].isin(selected_countries)) &
                                (df_filtered['phylum'].isin(selected_phylum)) &
                                (df_filtered['vote_cache'] >= min_votes) &
                                (df_filtered['content_type'].isin(selected_formats)) &
                                (df_filtered['resol'] >= min_res) &
                                (df_filtered['rank'].isin(filter_ranks))]
    
    #palette de couleur pour les camemberts lien avec les dipos:
    # https://plotly.com/python/discrete-color/
    #pour vote_cache et definition on pourrait utiliser une palette continue 
    #pour sous-ligner"l'augmentation d'une valeur entre chaque secteurs
    palette = px.colors.qualitative.Safe
    
    # Première rangée de camemberts
    titles=["Locations","Phylums","Classification<br>Ranks"]
    for i, col in enumerate(pies1):
        with col:
            # Calcul des données pour chaque camembert
            if i == 0:
                data = df_filtered['country'].value_counts()
                labels = data.index
            elif i == 1:
                data = df_filtered['phylum'].value_counts()
                labels = data.index
            elif i == 2:
                data = df_filtered['rank'].value_counts()
                labels = pd.Series(data.index)
                labels=labels.apply(lambda rank: [taxon_list[i] for i, value in enumerate(ranks) if value == rank][0])

            # Création du camembert
            fig = go.Figure(data=[go.Pie(labels=labels,
                                         values=data,
                                         showlegend=False,
                                         textinfo='label+percent',
                                         hole=0.4,
                                         marker=dict(colors=palette)
                                         )])
            fig.update_traces(textposition='inside')
            fig.update_layout(title_text=titles[i],
                              title_x=0.5,
                              title_y=0.5,
                              title_xanchor="center",
                              title_yanchor="middle",
                              margin=dict(l=0, r=0, t=0, b=0),
                              autosize=True,
                              )
            # Affichage du camembert
            st.plotly_chart(fig, use_container_width=True)
    
    # Deuxième rangée de camemberts
    titles=["User<br>Votes","Image<br>Formats","Image<br>Definition"]
    for i, col in enumerate(pies2):
        with col:
            # Calcul des données pour chaque camembert
            if i == 0:
                data = df_filtered['vote_cache'].value_counts(dropna=False)
                labels = data.index
            if i==1:
                data = df_filtered['content_type'].value_counts()
                labels = data.index
            if i==2:
                data = df_filtered['def'].value_counts()
                labels = data.index
                
            # Création du camembert
            fig = go.Figure(data=[go.Pie(labels=labels,
                                         values=data,
                                         showlegend=False,
                                         textinfo='label+percent',
                                         hole=0.4,
                                         marker=dict(colors=palette))])
            fig.update_traces(textposition='inside')
            fig.update_layout(title_text=titles[i],
                              title_x=0.5,
                              title_y=0.5,
                              title_xanchor="center",
                              title_yanchor="middle",
                              margin=dict(l=0, r=0, t=0, b=0),
                              autosize=True)
            # Affichage du camembert
            st.plotly_chart(fig, use_container_width=True)

    with options3[0]:
        selected_classification = st.selectbox('Type de classification', ['species', 'genus', 'family'], index=0)

    # Filtrer les données en fonction des options sélectionnées
    df_filtered = df_filtered.dropna(subset=[selected_classification])
    df_filtered = df_filtered.groupby(selected_classification)
    img_per_class = df_filtered.size()
    img_per_class=img_per_class.sort_values()
    
    with options3[1]:
        min_max_range = st.slider("Nombre d'images par classes", 
                                        min_value=0,
                                        max_value=1000, value=(10,300), step=10)
        min_img_per_class = min_max_range[0]
        max_img_per_class = min_max_range[1]
    
    with distributions[0]:
        # Curseur pour définir la plage de img_per_class
        custom_bins = [0, 1.1, 10.1, 100.1, 1000.1]
        custom_labels = ["1","]1-10]","]10-100]","]100-1000]"]
        
        # Créer l'histogramme des valeurs de img_per_class
        hist, bin_edges = np.histogram(img_per_class.values, bins=custom_bins)
        fig_hist = go.Figure(data=[go.Bar(x=custom_labels,
                                          y=hist,
                                          marker_color=config_params["primaryColor"]
                                          )])

        fig_hist.update_layout(title_text="Histogramme",
                               xaxis_title="Nombre d'images par classe",
                               yaxis_title='Nombre de classes'
                               )
        st.plotly_chart(fig_hist, use_container_width=True)

    with distributions[1]:
        # Calculer la distribution cumulée inverse
        cumsum_reverse = img_per_class[::-1].cumsum()[::-1]
        #Créer la courbe cumulée inversée
        fig_cumsum = go.Figure(data=[go.Scatter(x=img_per_class,
                                                y=cumsum_reverse,
                                                marker_color=config_params["primaryColor"]
                                                )])
        fig_cumsum.update_layout(title_text="Distribution cumulée décroissante",
                                 xaxis_title='Nombre d\'images par classe',
                                 yaxis_title='Nombre d\'images'
                                 )
        
        # Ajouter les barres verticales et les annotations pour min_img_per_class et max_img_per_class
        fig_cumsum.add_vline(x=min_img_per_class, line_dash="dash", line_color=palette[1], annotation_text=f"min img = {min_img_per_class}", annotation_position="top left")
        fig_cumsum.add_vline(x=max_img_per_class, line_dash="dash", line_color=palette[1], annotation_text=f"max img= {max_img_per_class}", annotation_position="top right")

        # Trouver la valeur de cumsum à l'endroit où les lignes verticales se croisent
        cross_min = cumsum_reverse[(img_per_class >= min_img_per_class)].values[0]
        
        df_filtered=df_filtered.agg(list).sort_index(axis=0)
        df_filtered=df_filtered[img_per_class.sort_index(axis=0)>=min_img_per_class]
        df_filtered["image_id"]=df_filtered["image_id"].apply(lambda x: x[:max_img_per_class] if len(x)>max_img_per_class else x)
        img_per_class=df_filtered["image_id"].apply(len)
        nb_image=img_per_class.sum()
        nb_class=df_filtered.shape[0]

        # Ajouter une annotation pour la valeur de cumsum à l'endroit où les lignes verticales se croisent
        fig_cumsum.add_annotation(dict(font=dict(color=palette[1],size=15),
                                    x=max_img_per_class+1,
                                    y=cross_min,
                                    showarrow=False,
                                    text="{} images <br> {} classes".format(nb_image,nb_class),
                                    xanchor='left'
                                    ))
        # Affiche
        st.plotly_chart(fig_cumsum, use_container_width=True)
    
    with tab4:
        dl_data=df_filtered.loc[:,["image_id"]]
        dl_data.rename(columns={ dl_data.columns[0]: "img_ids"},inplace=True)
        dl_data.index.name="class"
        st.download_button("Télécharger le dataframe",
                            dl_data.to_csv(sep="\t").encode('utf-8'),
                            "class_img_ids.csv",
                            "text/csv",
                            key='download-csv'
                            )
        st.dataframe(data=dl_data)
        with st.expander("Script Python pour télécharger les images depuis Mushroom Observer"):
            with open(os.path.join(os.path.join(os.getcwd(),"assets"),"script_dl.py"),'r') as script_file:
                script=script_file.read()
            st.download_button("Télécharger le script",
                                script,
                                "script_DL.py",
                                "text/plain",
                                key='download-script'
                                )
            st.code(script,language="python")
