import streamlit as st
import random
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import wikipediaapi
import rembg
import numpy as np
import tensorflow as tf
from keras.utils import img_to_array,array_to_img
import matplotlib.cm as cm

def vspace(n):
    for i in range(n):
        st.write("")
        
def round_corners(image, radius, border_width=0, border_color=(0,0,0), overlay=None):
    # Ajouter l'overlay avec la bonne couleur et opacité à l'image d'origine
    if overlay is not None:
        overlay = Image.new("RGBA", image.size, overlay)
        image = Image.alpha_composite(image.convert("RGBA"), overlay)

    # masquer l'image avec un rectangle de coins arrondis de même dimension
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), image.size], radius, fill=255)
    
    image = image.convert("RGBA")
    image.putalpha(mask)
    
    # Créer une nouvelle image RGBA totalement transparente de taille augmentée pour la bordure
    width, height = image.size
    enlarged_size = (width + 2 * border_width, height + 2 * border_width)
    new_image = Image.new("RGBA", enlarged_size, (0, 0, 0, 0))

    # Dessiner un rectangle de coins arrondis rempli de la couleur de bordure
    draw = ImageDraw.Draw(new_image)
    draw.rounded_rectangle([(0,0), enlarged_size], radius,
                           fill=border_color)

    # Coller l'image croppée sur la nouvelle image
    new_image.paste(image, (border_width, border_width), mask=image)

    return new_image

def change_number():
    st.session_state["rn"] = random.randint(1,100)
    return 
@st.cache_data
def sample(x,n,rn):
    #dummy function to cache the result
    return x.sample(n)

def set_states(key,value):
    """
    Wrapper functun to use with callbacks

    Parameters
    ----------
    key : any
        clé unique , identifiant streamlit.
    value : any
        valeur à affecté à la clé.

    Returns
    -------
    None.

    """
    st.session_state[key]=value
 
def format_class_name(name):
    s_name=name.split("_")
    c_name=""
    for w in s_name:
        c_name+=" "+w.capitalize()
        
    return c_name

def get_first_paragraph_wiki(term):
    wiki_wiki = wikipediaapi.Wikipedia('mush-reco (https://mush-reco.streamlit.app/)','fr')
    page = wiki_wiki.page(term)
    if page.exists():
        # paragraphs = page.text.split('\n')
        # if len(paragraphs) > 0:
        #     return paragraphs[0]
        return page.summary
    else:
        wiki_wiki = wikipediaapi.Wikipedia('mush-reco (https://mush-reco.streamlit.app/)','en')
        page = wiki_wiki.page(term)
        if page.exists():
            # paragraphs = page.text.split('\n')
            # if len(paragraphs) > 0:
            #     return paragraphs[0]
            return page.summary
        else:
            return None

def get_page_wiki(term):
    wiki_wiki = wikipediaapi.Wikipedia('mush-reco (https://mush-reco.streamlit.app/)','fr')
    page = wiki_wiki.page(term)
    if page.exists():
        return page.canonicalurl
    else:
        wiki_wiki = wikipediaapi.Wikipedia('mush-reco (https://mush-reco.streamlit.app/)','en')
        page = wiki_wiki.page(term)
        if page.exists():
            return page.canonicalurl
        else:
            return None  
def preproc(img,mask,square_crop=True):
    #smart crop
    mask_np=np.array(mask)
    
    if square_crop:
        rows, cols = np.nonzero(mask_np)
        top, bottom = np.min(rows), np.max(rows)
        left, right = np.min(cols), np.max(cols)
        width = right - left
        height = bottom - top
        diff = abs(width - height)
        
        # Ajustement des variables pour obtenir un carré
        if width < height:
            left -= diff // 2
            right += diff - (diff // 2)
        else:
            top -= diff // 2
            bottom += diff - (diff // 2)
        # Ajustement pour s'assurer que les valeurs restent dans les limites de l'image
        if (left < 0) and (right >= mask.width):
            left=0
            right = mask.width
        else:
            if left < 0:
                right -= left
                left = 0
            if right >= mask.width:
                left -= (right - mask.width + 1)
                right = mask.width - 1
                
        if (top < 0) and (bottom >= mask.height):
            top=0
            bottom = mask.height
        else:
            if top < 0:
                bottom -= top
                top = 0
            if bottom >= mask.height:
                top -= (bottom - mask.height + 1)
                bottom = mask.height - 1
    else:
        left=0
        right=mask.width
        top=0
        bottom=mask.height

    mask_crop=mask.crop((left, top, right + 1, bottom + 1))
    img_crop=img.crop((left, top, right + 1, bottom + 1))
    
    img_mask = Image.new('RGBA', img_crop.size)
    img_mask.paste(img_crop, (0, 0))
    img_mask.putalpha(mask_crop)
    detoure_img=img_mask.copy()
    
    blur_bg = img_crop.filter(ImageFilter.GaussianBlur(radius=5))
    img_crop_np = np.array(img_crop)
        
    variance = np.var(img_crop_np)
    bruit = np.random.normal(loc=127.5, scale=np.sqrt(variance), size=img_crop_np.shape).astype(np.uint8)

    #BB
    bb_img = Image.alpha_composite(Image.new('RGBA', img_crop.size,(0,0,0)),img_mask).convert('RGB')
    
    #blurr
    blur_img = Image.alpha_composite(blur_bg.convert('RGBA'),img_mask).convert('RGB')
        
    #noise
    noise_img = np.clip(img_crop_np + bruit, 0, 255).astype(np.uint8)
    noise_img = Image.fromarray(noise_img)
    noise_img = noise_img.convert('RGBA')
    noise_img = Image.alpha_composite(noise_img,img_mask).convert('RGB')
        
    #noise and blurr
    bruit = bruit*(1/255)
    blur_bg_np = np.array(blur_bg)
    noiseblur_img=Image.alpha_composite(Image\
                                        .fromarray(np.clip(blur_bg_np*bruit, 0,255).astype(np.uint8))\
                                        .convert("RGBA"),
                                        img_mask).convert('RGB')
    
    return detoure_img,bb_img,blur_img,noise_img,noiseblur_img,img_crop

def get_max_value(array):
    array=array[0].tolist()
    i_1=0
    i_2=0
    i_3=0
    max_1=0
    max_2=0
    max_3=0
    for i,value in enumerate(array):
        if value >max_1:
            max_1=value
            i_1=i
    for i,value in enumerate(array):
        if value>max_2 and value<max_1:
            max_2=value
            i_2=i
    for i,value in enumerate(array):
        if value>max_3 and value<max_2:
            max_3=value
            i_3=i

    list_index=[i_1,i_2,i_3]
    max_value=[max_1,max_2,max_3]
    return list_index,max_value
#==================================================Partie Grad Cam======================================
def make_gradcam_heatmap(img_array, model,pred_index=None):
    """Fonction qui permet de générer une gradcam, prend en entrée une image à 4 dimensions,
     model: le model générer plus haut
      le dernier nom de la couche de convolution (déjà paramètré plus bas pour le ResNet) """
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer("conv5_block3_3_conv").output, model.output]
    )

    # Then, we compute the gradient of the top predicted class for our input image
    # with respect to the activations of the last conv layer
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        tape.watch(last_conv_layer_output)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])

        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)


    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))


    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]

    heatmap = tf.squeeze(heatmap)
    #Normalisation en zéro et 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)

    return heatmap.numpy()

def save_and_display_gradcam(img_path, heatmap, alpha=0.6):
    #Fonction qui permet de fusionner l'image initial avec la heatmap 
    #Prend en entrée l'image, la heatmap et un paramètre alpha, définissant l'opacité de la heatmap
    img = img_path
    # Repassage de l'image et de la heatmap en 255 et non entre zéro et 1
    heatmap = np.uint8(255 * heatmap)
    # Use jet colormap to colorize heatmap
    jet = cm.get_cmap("jet")

    jet_colors = jet(np.arange(256))[:, :3]# Use RGB values of the colormap
    jet_heatmap = jet_colors[heatmap]

    # Create an image with RGB colorized heatmap
    jet_heatmap = array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = img_to_array(jet_heatmap)


    superimposed_img = jet_heatmap * alpha + img# Superimpose the heatmap on original image
    superimposed_img = array_to_img(superimposed_img)
    return superimposed_img                      
