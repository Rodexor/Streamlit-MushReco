# Exemple de script pour télécharger les images contenu dans le fichier csv
#
# Le script crée 3 dossiers train, valid et test selon des proportions
#
# Une erreur sera renvoyé si une classe a très peu d'images et qu'aucune image n'a été attribué au test
# ou au valid lors de la randomisation. exemple : 2 images et les proportions [0.33,0.33,0.33]
#
# Il est possible d'interrompre le script lors du téléchargement, celui-ci
# ne téléchargera que les images restantes

import os
import numpy as np
import pandas as pd
import requests
from datetime import datetime
import warnings

def random_train_test_valid_list(size,proportions,generator):
    if size<3:
        raise ValueError("size cannot be less than 3")
    
    probs=generator.random(size)
    labels=probs.copy().astype("str")
    labels[probs<=proportions[0]]="train"
    labels[ (proportions[0]<probs) & ( probs<=(proportions[0]+proportions[1]) ) ]="valid"
    labels[(proportions[0]+proportions[1]) < probs ]="test"
    
    if  ( len(labels[labels=="valid"])==0 ) or ( len(labels[labels=="test"])==0 ) or ( len(labels[labels=="train"])==0 ):
        print(np.round(probs,decimals=2))
        raise ValueError("\n valid or test or train labels where not attributed because of the combination size: {} and proportions: {}. \nHere are the computed labels {}".format(size,proportions,list(labels))) 
    return list(labels)

#paramètres
csv_file="class_img_ids.csv" #filename of the csv file conaining the list image ids for each class 
data_directory=os.getcwd() #destination directory to create the train,valid and test sets 
proportions=[0.8,0.1,0.1] #proportion of the train, valid and test sets
size=320 #Taille des images à télécharger : 320,640,960,1280, "orig"
headers = {'User-Agent':"My agent"} #Dummy agent pour que le serveur accèpte les requêtes

#data loading
data=pd.read_csv(csv_file,sep="\t",converters={"img_ids": lambda x: x.strip("[]").split(", ")},index_col=0)

nb_image_per_classe=data["img_ids"].apply(len)
nb_image=nb_image_per_classe.sum()
nb_class=data.shape[0]

print("{} images pour {} classes will be downloaded".format(nb_image,nb_class))

rng = np.random.default_rng(1984)

#gives the label train,valid or test to each images in each class with the proportions given
data["subset"]=nb_image_per_classe.apply(lambda x:random_train_test_valid_list(x,proportions,rng))
count=0
for classe in data.index[1:4]:
    start_time = datetime.now()
    
    for ID,subset in zip(data.loc[classe,"img_ids"],data.loc[classe,"subset"]):
        subset_directory=os.path.join(data_directory,subset )
        if not os.path.exists(subset_directory):
            os.makedirs(subset_directory)
        
        class_directory=os.path.join(subset_directory,classe )
        if not os.path.exists(class_directory):
            os.makedirs(class_directory)
        
        filename="{}.jpg".format(ID)
        filepath=os.path.join(class_directory,filename )
        if not os.path.exists(filepath):
            url="https://mushroomobserver.org/images/{}/{}.jpg".format(size,ID)
            img_data = requests.get(url,headers=headers).content
            with open(filepath, 'wb') as handler:
                handler.write(img_data)    
    count+=1
    time_left=(nb_class-count)*(datetime.now() - start_time)
    count_str=str(count).zfill(len(str(nb_class)))
    print("\rClass {}/{} ETA : {}".format(count_str,nb_class,time_left),end="")
