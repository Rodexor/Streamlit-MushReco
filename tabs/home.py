import streamlit as st
from app_lib.utils import vspace 
import os

title = "RECONNAISSANCE DE CHAMPIGNONS"
sidebar_name = "Présentation" 

def run():
    #st.markdown("""
                #<h1 style='text-align: center;'>RECONNAISSANCE DE CHAMPIGNONS</h1>
                #""",
                #unsafe_allow_html=True
                #)
    #cols = st.columns(3)
    #with cols[1]:
        #st.image(os.path.join(os.path.join(os.getcwd(),"assets"),"logo.png"),use_column_width=True)
    
    #TODO ajouter une version anglaise, les noms de créateurs et leur coordonnées, ainis que des infos
    #sur datascientest
    #TODO utiliser un logo plus atrayant et peut-etre des animations cools

    with st.columns(3)[1]:
        st.image(os.path.join(os.path.join(os.getcwd(),"static"),"logo_hexa_shadow_512.png"),use_column_width=True)
        
    st.markdown("""
                <h1 style='text-align: center;'>RECONNAISSANCE DE CHAMPIGNONS</h1>
                """,
                unsafe_allow_html=True
                )
    st.markdown("")
    st.markdown("")
    st.markdown("")


    st.markdown("<h2 style='text-align: center; color: black;'>Enguerran Gay - Rodrigo Jolly - Louis Pailler</h2>", unsafe_allow_html=True)

    st.subheader("Résumé du projet ")
    st.markdown("- **CONTEXTE**: Outils de computer vision de plus en plus utilisés dans de nombreux domaines d'activité")
    
    st.markdown("- **OBJECTIF**: Créer une application qui puisse identifier l'espèce d'un champignon grâce à une photo")
    lien="https://mushroomobserver.org"
    texte_lien="Mushroom Observer"
    
    st.markdown("- **METHODE**: Apprentissage d'un réseau de neuronne à partir des données de [{}]({})".format(texte_lien, lien))
    
    st.markdown("- **RESULTATS**: Le modèle obtenu réussi à prédire l'espèce d'un champignon avec une précision d'environ 92% pour le meilleur modèle avec 12 espèces retenus")

    st.markdown("")
    st.markdown("")
    st.markdown("")



    st.subheader("Détails du projet ")
    ctxt=st.expander("**CONTEXTE**")
    with ctxt:
        st.markdown("""<h6 style='text-align: justify; color: black;'>La classification des espèces est primordiale dans tous les domaines d’étude du vivant. 
                    De nombreuses activités, telles que l'étude de la richesse spécifique d'une région, la surveillance des populations menacées ou encore les
                    actions de lutte contre des espèces invasives, dépendent de la précision des compétences en matière d'identification</h6>""", unsafe_allow_html=True)
        st.markdown("""<h6 style='text-align: justify; color: black;'>L’identification précise des espèces de champignons, au niveau de l’espèce, est primordiale 
                    dans différents domaines d’application fondamentale (écologie, évolution du vivant, taxonomie) et appliquée (bio inspiration, métabolomique) 
                    de la recherche scientifique. C’est aussi le cas dans l’industrie, 
                    puisqu’ils produisent de nombreux composés naturels comme certains métabolites secondaires utilisés dans l’industrie pharmaceutique, 
                    médicale ou encore des cosmétiques. Cependant, au vu de la grande diversité d’espèces dans le règne des champignons et de leurs 
                    caractéristiques phénotypiques parfois très proches, leur identification reste fastidieuse et complexe.</h6>""", unsafe_allow_html=True)
        st.markdown("""<h6 style='text-align: justify; color: black;'> Le développement d’algorithmes d'analyse d'images automatisée (“computer vision”), 
                    l'intelligence artificielle s'est révélée être une solution efficace pour réaliser des tâches nécessitant des analyses d'images spécialisées 
                    que constitue l’identification d’espèces. Les réseaux de neurones convolutifs (CNN), se sont montrés très efficaces pour le traitement d’images.</h6>""", unsafe_allow_html=True)
        st.image("static/Figure_contexte.png")

    obj=st.expander("**OBJECTIFS**")
    with obj:
        st.markdown("""<h6 style='text-align: justify; color: black;'> Cette étude avait pour but d'entraîner un CNN capable d’analyser des images de champignons, 
        de les classifier et d'identifier l’espèce correspondante. Ce dernier à été entrainé sur plusieurs milliers d’images de champignons, généralement des photographies 
        prises par des mycologues, scientifiques ou des amateurs de champignons. Nous avons construit un CNN pour identifier les espèces présentes sur des photographies, puis évaluer les 
        performances du modèle développé. </h6>""", unsafe_allow_html=True)
    
    meth=st.expander("**METHODE**")
    with meth:
        st.markdown("""<h6 style='text-align: justify; color: black;'> Les images disponibles sur la base de données en ligne de Mushroom Observer ont été utilisées pour entrainer les modèles.
                Après exploration des données et séléction des images selon certaines caractéristiques (images prises aux Etats-Unis, plus de 100 images par espèces, format jpeg, résolution suffisante), différents modèles ont été entrainés pour obtenir les meilleurs résultats possibles.
                Des modèles à architectures simples (AlexNet, VGG16 et VGG19) ont tout d'abord été testé. Puis, d'autres modèles plus complexes ont été utilisés 
                (ResNet50V2, ResNet152V2 et EfficientNet), en faisant varier les hyperparamètres. </h6>""", unsafe_allow_html=True)

    res=st.expander("**RESULTATS**")
    with res:
        st.markdown("""<h6 style='text-align: justify; color: black;'> Ici nous avons développé un modèle capable de reconnaitre un certain nombre d’espèces, avec un taux d’identification correcte d’environ 92%. Les images utilisées sont disponibles sur le <a href='https://github.com/MenguGay/AVR2023_BootcampDS_Repo_Champ'>Github</a>. Après exploration des données et sélection des images selon certaines caractéristiques (pays, résolution, type de classification, note, etc.), plusieurs modèles ont été testés selon le preprocessing appliqué aux images qui ont montré des taux variables de classification correcte, avec les meilleurs résultats pour un modèle REsNet151V2. Des photos peuvent être déposées directement à la page pour une identification en temps réel.</h6>""", unsafe_allow_html=True)
