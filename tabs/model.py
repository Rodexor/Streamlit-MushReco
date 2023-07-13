import streamlit as st

title = "Modèle"
sidebar_name = "Modèle"  

def run(paths):
    #MODEL
    st.markdown("<h1 style='text-align: center; color: darkgoldenrod;'>Modélisation</h1>", unsafe_allow_html=True)
    st.markdown("")
    st.subheader("Les réseaux de neurones convolutifs (CNN)")
    st.image("static/Figure_model.png")
    st.markdown("<h6 style='text-align: center; color: black;'> Schéma général d'un CNN</h6>", unsafe_allow_html=True)
    st.markdown("""<h6 style='text-align: justify; color: black;'> Les réseaux de neurones convolutifs (CNN), se sont montrés efficaces pour 
                le traitement d’images et la détection d’objets. En effet, ils sont considérés comme 
                les modèles de reconnaissance visuelle les plus puissants dans le domaine de la computer vision. Les CNN visent à transformer 
                une image d'entrée de haute dimension en une sortie sémantique de basse dimension mais hautement abstraite. Ils permettent une hiérarchisation 
                des caractéristiques par le biais d’une segmentation précise, ce qui les rend hautement précis. L’architecture des différents types de CNN est 
                sensiblement similaire, et comprend notamment différentes couches présentées ci dessus. </h6>""", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    # CNN Simples
    st.subheader("Essais de différents modèles")
    simp=st.expander("**CNN A ARCHITECTURES SIMPLES**")
    with simp:
        st.markdown("""<h6 style='text-align: justify; color: black;'>Plusieurs tests ont été réalisés pour des modèles à artchitectures simples (voir image ci dessous) comme le VGG16, Alexnet
            ou encore le VGG19.</h6>""", unsafe_allow_html=True)
        st.image("static/Figure_architecture_VGG16.png")
        st.markdown("<h6 style='text-align: center; color: black;'> Schéma de l'architecture du modèle VGG16</h6>", unsafe_allow_html=True)
        st.markdown("")
        st.markdown("""<h6 style='text-align: justify; color: black;'> Les meilleures résultats sont obtenus avec un modèle de base VGG19 (learning rate = 0.0001; dropout = 0.4). La perte finale est de 
            1.9 sur les données de test et 2.5 pour les données d'entrainement. La précision est proche de 0.55 pour le test et 0.35 pour celui d’entrainement. 
            Cette valeur étant relativement faible, la matrice de confusion n’apporte aucune précision sur les espèces (i.e. photographies) mal classifiées.
              D’autres tests ont été réalisés sur davantage d'époques, en faisant varier notamment la valeur du dropout ou du learning rate mais n’ont pas obtenu de meilleurs résultats. </h6>""", unsafe_allow_html=True)
        st.image("static/Figure_loss_accuracy_VGG19.png")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    # CNN a arhitectures plus complexes
    comp=st.expander("**CNN A ARCHITECTURES COMPLEXES**")
    with comp:
        st.markdown("""<h6 style='text-align: justify; color: black;'> Là aussi, plusieurs modèles à artchitectures complexes comme le ResNet50V2, ResNet152V2 
                ou encore EfficientNet. Ils sont composés de plus de blocks de convolution, et par conséquent, peuvent afficher de meilleurs résultats. Le modèle 
                ResNet152V2 affiche les meilleurs résultats. Le dernier bloc de convolution a été dégelé dans l’objectif d’améliorer les résultats 
                 en ré-entraînant le modèles sur ces couches.</h6>""", unsafe_allow_html=True)
        st.subheader("52 classes")
        st.markdown("""<h6 style='text-align: justify; color: black;'> En faisant varier les paramètres des modèles, les résultats ci dessous sont obtenus.</h6>""", unsafe_allow_html=True)
        st.image("static/Figure_resnet152V2_52c.png")
        st.markdown("")
        st.markdown("""<h6 style='text-align: justify; color: black;'> Une fois le dégel des couches réalisé, on observe que le modèle entraîné sur 52 classes atteint cette fois-ci 
                65% de precision sur les données de test. La matrice de confusion ci dessus montre de bons résultats, mais le score F1 de beaucoup de classes reste relativement faible.</h6>""", unsafe_allow_html=True)
        st.markdown("")
        st.image("static/Figure_matrice_confusion_52c.png")
        st.markdown("""<h6 style='text-align: justify; color: black;'> Au vue des résultats variables des scores F1 obtenus sur le cas d’étude précédent, 
                avec certains relativement faibles, ce modèle a été de nouveau entrainé sur un jeu de données à 12 classes.</h6>""", unsafe_allow_html=True)
        st.markdown("")
        st.subheader("12 classes")
        st.image("static/Figure_resnet152V2_12c.png")
        st.markdown("")
        st.markdown("""<h6 style='text-align: justify; color: black;'> Finalement, l’accuracy final sur le jeu de données d'entraînement est de 0.85, 
                pour une accuracy maximal sur le jeu de test de 0.92. On obtient une classification de très haute qualité (voir matrice de confusion ci-dessous)
                avec des scores F1 étant au plus bas à 0.7. Ces résultats confirment l’efficacité de cette approche avec un nombre de classes réduite.</h6>""", unsafe_allow_html=True)
        st.markdown("")
        st.image("static/Figure_matrice_confusion_12c.png")
    
