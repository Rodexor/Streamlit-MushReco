import streamlit as st
from app_lib.widgets import select_buttons
from app_lib.data_loaders import load_metadata,load_img_paths
import os
from app_lib.utils import sample,change_number,vspace
from streamlit_extras.badges import badge
import random

# TODO : you can (and should) rename and add tabs in the ./tabs folder, and import them here.
from tabs import home,dataset,preproc, model,resultats


st.set_page_config(page_title="RECONNAISSANCE DE CHAMPIGNONS",
                   page_icon="",#les emoticones ne semblent pas marcher
                   #layout="wide",
                   initial_sidebar_state="expanded"
                   )


tab_sidebar_names=[home.sidebar_name,
                   dataset.sidebar_name,
                   preproc.sidebar_name,
                   model.sidebar_name,
                   resultats.sidebar_name,
                   ]

#%%
#DATA LOADING

# Trick to keep the same sampling between each run 
# except when we change the "rn" key in st.sessions_state
if "rn" not in st.session_state:
    st.session_state["rn"] = 42
    
random.seed(st.session_state.rn)

df_filtered = load_metadata(os.path.relpath("assets/csv_file"))

data_dir=os.path.relpath("assets/data_test")
data_types=["data_simple",
            "data_FG",
            "data_crop",
            "data_bb",
            "data_blur"
            ,"data_noise"
            ,"data_noise&blur"]
paths={}
for data_type in data_types:
    paths[data_type[5:]]=load_img_paths(os.path.join(data_dir,data_type))

# Sélectionner une image aléatoire par classe
# keys : paths , class , filename
for i,key in enumerate(paths):
    if i==0:
        paths[key] = paths[key].groupby('class')\
                            .apply(lambda x: sample(x,10,st.session_state["rn"]))\
                            .reset_index(drop=True)
        filnames_sample = paths[key]["filename"]
    else:
        paths[key] = paths[key][paths[key]["filename"].isin(filnames_sample)]
        
    paths[key]=paths[key].sort_values(["class","filename"])


#%%
def run():
    #st.sidebar.image(
        #"https://dst-studio-template.s3.eu-west-3.amazonaws.com/logo-datascientest.png",
        #width=200,
    #)
        
    with st.sidebar:
        cols_logo=st.columns([0.25,0.5,0.25])
        with cols_logo[1]:
            st.image(os.path.join(os.path.join(os.getcwd(),"static"),"logo_hexa_shadow_256.png"),use_column_width=True)
        
        st.markdown("""
                    <h2 style='text-align: center;'>RECONNAISSANCE DE CHAMPIGNONS</h2>
                    """,
                    unsafe_allow_html=True
                    )

        menu_select=select_buttons(options=tab_sidebar_names,
                                   name=None,
                                   main_key="MENU",
                                   horizontal=False,
                                   use_container_width=True,
                                   default = 0,
                                   unselect=False
                                   )
        vspace(1)
        st.markdown(""" Github du projet&nbsp;&nbsp;
                        [![Github](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/MenguGay/AVR2023_BootcampDS_Repo_Champ)
                    """)
        st.markdown(""" Enguerran Gay&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        [![Github](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/MenguGay)
                        [![Linkedin](./app/static/logo_linkedin_20.png)](https://www.linkedin.com/in/enguerran-gay-aa34a2250/)
                        [![Mail](./app/static/mail_20.jpg)](mailto:enguerrangay@gmail.com) 
                    """)
        st.markdown(""" Louis Pailler&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        [![Github](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/louispailler)
                        [![Linkedin](./app/static/logo_linkedin_20.png)](https://fr.linkedin.com/in/louis-pailler-056224170) 
                        [![Mail](./app/static/mail_20.jpg)](mailto:louis.pailler@outlook.fr) 
                    """)

        st.markdown(""" Rodrigo Jolly&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        [![Github](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/Rodexor)
                        [![Linkedin](./app/static/logo_linkedin_20.png)](https://www.linkedin.com/in/rodrigo-jolly-92a703224/) 
                        [![Mail](./app/static/mail_20.jpg)](mailto:rodrigo.jolly@gmail.com) 
                    """)
        
        cols_logo_2=st.columns([0.1,0.40,0.50])
        with cols_logo_2[1]:
            st.markdown("[![datascientest.com](./app/static/logo_datascientest_100.png)](https://datascientest.com)",unsafe_allow_html=True)
        with cols_logo_2[2]:
            st.markdown("[![mushroomobserver.org](./app/static/logo_mushroom_observer_100.png)](https://mushroomobserver.org/info/intro)")
        st.markdown("Rembg : [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/danielgatis/rembg)")
    
    if menu_select == tab_sidebar_names[0]:
        home.run()
        
    elif menu_select == tab_sidebar_names[1]:
        dataset.run(paths,df_filtered)
        
    elif menu_select == tab_sidebar_names[2]:
        preproc.run(paths)
    
    elif menu_select == tab_sidebar_names[3]:
        model.run(paths)
    
    elif menu_select == tab_sidebar_names[4]:
        resultats.run(paths)

if __name__ == "__main__":
    run()
