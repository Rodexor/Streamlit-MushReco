from PIL import Image
import streamlit as st
from streamlit_extras.stateful_button import button
from .utils import set_states,vspace,round_corners

import functools #TODO est-ce qu'on peut pas s'en sortir avec des lambda fonction ?

def display_gallery(paths,n_cols,border_width=0,border_color=(0,0,0),radius=0,overlay=(0,0,0,0)):
    # Find the dimensions of the largest image
    max_width = 0
    max_height = 0
    for image_path in paths:
        image = Image.open(image_path)
        image_width, image_height = image.size
        if image_width > max_width:
            max_width = image_width
        if image_height > max_height:
            max_height = image_height
    max_dim=max(max_height,max_width)
    groups = []
    for i in range(0,len(paths),n_cols):
        groups.append(paths[i:i+n_cols])
    
    for group in groups:
        cols= st.columns(n_cols)
        for i, img_file in enumerate(group):
            img=Image.open(img_file)
            cols[i].image(round_corners(img.resize((max_dim,max_dim)),
                                            radius=radius,
                                            border_width=border_width,
                                            border_color=border_color,
                                            overlay=overlay
                                            )
                              ,use_column_width=True)

def select_buttons(options,main_key,name=None,horizontal=True,use_container_width=True,default=None,unselect=False):

    #TODO Mettre une option pour changer la couleur, la police et la taille de ce titre
    if name is not None:
        st.markdown("""
                    <h1 style='text-align: center;'>{}</h1>
                    """.format(name),
                    unsafe_allow_html=True
                    )

    #syntax des clés individuelles des boutons
    button_keys=[main_key+str(i) for i in range(len(options))]
    
    if main_key not in st.session_state:
        st.session_state[main_key]=button_keys[default]
        for button_key in button_keys:
            if (button_key == button_keys[default]):
                st.session_state[button_key]=True
            else:
                st.session_state[button_key]=False
          
    else:
        for i,key in enumerate(button_keys):
            if key==st.session_state[main_key]:
                if unselect:
                    set_states(key,not(st.session_state[key]))
                else:
                    set_states(key, True)
            else:
                set_states(key, False)
        
    if horizontal:
        cols=st.columns(len(options))
        for i,col in enumerate(cols):
            with col:
                button(options[i],key=button_keys[i]
                          ,on_click= functools.partial(set_states, main_key,button_keys[i]) 
                          ,use_container_width =use_container_width)

    else:
        with st.columns(1)[0]:
            for i,option in enumerate(options):
                button(options[i],key=button_keys[i]
                          ,on_click= functools.partial(set_states, main_key,button_keys[i]) 
                          ,use_container_width =use_container_width)
                
    for i,key in enumerate(button_keys):
        if st.session_state[key]:
            return options[i]


def select_gallery(options,main_key,paths,n_cols,border_width=0,border_colors=["#646464","#DF7F5F"],radius=0,overlay=(0,0,0,0),v=2,default=None,unselect=False):

    #syntax des clés individuelles des boutons
    button_keys=[main_key+str(i) for i in range(len(options))]
    
    if main_key not in st.session_state:
        st.session_state[main_key]=button_keys[default]
        for button_key in button_keys:
            if (button_key == button_keys[default]):
                st.session_state[button_key]=True
            else:
                st.session_state[button_key]=False
          
    else:
        for i,key in enumerate(button_keys):
            if key==st.session_state[main_key]:
                if unselect:
                    set_states(key,not(st.session_state[key]))
                else:
                    set_states(key, True)
            else:
                set_states(key, False)
    
    # Find the dimensions of the largest image
    max_width = 0
    max_height = 0
    for image_path in paths:
        image = Image.open(image_path)
        image_width, image_height = image.size
        if image_width > max_width:
            max_width = image_width
        if image_height > max_height:
            max_height = image_height
    max_dim=max(max_height,max_width)
    path_groups = []
    option_groups=[]
    key_groups=[]
    
    for i in range(0,len(paths),n_cols):
        path_groups.append(paths[i:i+n_cols])
        option_groups.append(options[i:i+n_cols])
        key_groups.append(button_keys[i:i+n_cols])
        
    for path_group,option_group,key_group in zip(path_groups,option_groups,key_groups):
        cols= st.columns(n_cols)
        for i,(path,option,key) in enumerate(zip(path_group,option_group,key_group)):
            with cols[i]:
                img=Image.open(path)
                
                if st.session_state[key]:
                    color=border_colors[1]
                    overlay_color=overlay
                else:
                    color=border_colors[0]
                    overlay_color=(0,0,0,0)
                cols[i].image(round_corners(img.resize((max_dim,max_dim)),
                                            radius=radius,
                                            border_width=border_width,
                                            border_color=color,
                                            overlay=overlay_color
                                            )
                              ,use_column_width=True)
                button(option
                       ,key=key
                       ,on_click= functools.partial(set_states, main_key,key) 
                       ,use_container_width =True)
        vspace(1)
 
    for i,key in enumerate(button_keys):
        if st.session_state[key]:
            return options[i]
                    
