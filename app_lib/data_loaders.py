import pandas as pd
import numpy as np
import os
import streamlit as st
from keras.models import load_model
import numpy as np

#TODO make the functiuns read the actual csv and images files in the github isntead of a personalised
# one
@st.cache_data
def load_metadata(dirpath):
    
        #%% Ouverture des donnés
    #========================Ouverture des donnés========================================

    images_observation=pd.read_csv(os.path.join(dirpath,"images_observations.csv"),sep='\t')
    locatation_ctry=pd.read_csv(os.path.join(dirpath,"locations_ctry.csv"),sep='\t')
    name_classification=pd.read_csv(os.path.join(dirpath,"name_classifications.csv"),sep="\t")
    observations=pd.read_csv(os.path.join(dirpath,"observations.csv"),sep="\t")
    image_parsed=pd.read_csv(os.path.join(dirpath,"images_parsed.csv"),sep='\t')
    name_parsed=pd.read_csv(os.path.join(dirpath,"names_reparsed.csv"),engine="python",sep=r"\t")
    #%% 
    #========================================Merging==============================================
    #On ne prend ici que les donnés intéressante dans le cadre du pre-processing de donnés
    #Renomage des id par le nom des clef primaire et clef étrangère présent dans les tables dans la database pour faciliter les merges
    image_parsed=image_parsed.rename(columns={"id":"image_id"})
    observations=observations.rename(columns={"id":"observation_id"})
    observations=observations.drop("vote_cache",axis=1) #Doublons avec image_parsed
    name_parsed=name_parsed.rename(columns={"id":"name_id"})
    #Création d'un dataframe et merge des donnés 
    df=image_parsed[["vote_cache","height","width","content_type","image_id","diagnostic","ok_for_export"]]
    df=df.merge(right=images_observation,on="image_id",how="inner")
    df=df.merge(right=observations[["observation_id","location_id","name_id","thumb_image_id"]],on="observation_id",how="inner")
    df=df.merge(right=name_parsed[["name_id","classification","rank","text_name"]],on='name_id',how="inner")
    df=df.merge(right=name_classification,on="name_id",how="inner")
    df=df.merge(right=locatation_ctry[["location_id","country","country_iso"]],on="location_id",how="inner")
    #Gestion légère des donnés, supressions d'information superflus et génération des colonnes espéces et génus 
    df["content_type"]=df["content_type"].str.replace("image/","")
    # =============================================================================
    # df=df.rename(columns={"text_name":"species"})
    # for place in ("group","sect."):
    #    df["species"]=df["species"].str.replace(place,"")
    # df["genus"]=df['species'].apply(lambda x:x.split(sep=' ')[0].strip('"'))
    # df["species"]=df["species"].str.replace(" ","_")#Nécessaire pour générer des directory
    # =============================================================================
    df["genus"]=np.nan    
    df["species"]=np.nan
    sub_species=df["rank"]<=4
    sub_genus=df["rank"]<=9
    df["species"].mask(sub_species,df[sub_species]["text_name"].apply(lambda x:x.split(sep=' ')[0].strip('"') + "_" + x.split(sep=' ')[1].strip('"')),inplace=True)
    df["genus"].mask(sub_genus,df[sub_genus]["text_name"].apply(lambda x: x.split(sep=' ')[0].strip('"')),inplace=True)
    # =============================================================================
    df["resol"]=df['height']*df["width"]#Définition de la résolution d'une image 
        
    df=df[['image_id','vote_cache','content_type', 'diagnostic', 'ok_for_export', 'kingdom', 'phylum', 'family','country', 'genus', 'species', 'resol','rank']]
    df = df[(df['kingdom'] == 'Fungi') & (df['diagnostic'] == 1) & (df['ok_for_export'] == 1) & (df['resol'] != 0) & ~(df['resol'].isna())]

    bins = [0, 720 * 480, 1280 * 720, 1920 * 1080, 3840 * 2160, 7680 * 4320,1e10]
    labels = ["LD",'SD', 'HD Ready', 'Full HD', '4k', '8k+']
    df["def"] = pd.cut(df["resol"], bins=bins, labels=labels)
    df=df.drop(columns=['kingdom','diagnostic','ok_for_export'])
    
    #REBIN DE VOTE_CACHE
    df['vote_cache']=df['vote_cache'].round(decimals=0)
    return df 
@st.cache_data
def load_img_paths(repertoire_racine):
    chemins = []
    classes = []
    noms_fichiers = []
    # Parcourir les sous-répertoires
    for classe in os.listdir(repertoire_racine):
        sous_repertoire = os.path.join(repertoire_racine, classe)
        
        # Vérifier si l'élément est un répertoire
        if os.path.isdir(sous_repertoire):
            # Parcourir les fichiers dans le sous-répertoire
            for fichier in os.listdir(sous_repertoire):
                chemin_fichier = os.path.join(sous_repertoire, fichier)
                
                # Ajouter les données aux listes
                chemins.append(chemin_fichier)
                classes.append(classe)
                noms_fichiers.append(os.path.basename(fichier))

    # Créer le DataFrame
    data = {'path': chemins, 'class': classes,'filename': noms_fichiers}
    return pd.DataFrame(data)

@st.cache_resource
def loading_model(model_path):
    model=load_model(model_path)
    return model

@st.cache_data
def classe_list(path):
    classes=sorted(os.listdir(os.path.join(os.getcwd(),path)))
    index=[i for i in range(12)]
    return classes,index    
