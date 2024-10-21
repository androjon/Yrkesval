import streamlit as st
import json

from occupation_class import create_occupation_index
from create_options import create_options

@st.cache_data
def import_data(filename):
    with open(filename) as file:
        content = file.read()
    output = json.loads(content)
    return output

@st.cache_data
def import_occupationdata():
    ocupation_data = create_occupation_index()
    return ocupation_data

@st.cache_data
def import_options():
    options_field, options_ssyk_level_4, options_occupations, options_titles = create_options(input)
    st.session_state.options_field = options_field
    st.session_state.options_ssyk_level_4 = options_ssyk_level_4
    st.session_state.options_occupations = options_occupations
    st.session_state.options_titles = options_titles

def show_info_selected_sidebar(fields, groups, occupation, description, taxonomy):
    with st.sidebar:
        SHORT_ELBOW = "└─"
        SPACE_PREFIX = "&nbsp;&nbsp;&nbsp;&nbsp;"
        strings = []
        if fields:
            strings.append(fields)
        if groups:
            group_str = SHORT_ELBOW + groups
            strings.append(group_str)
        if occupation:
            occupations_str = SPACE_PREFIX + SHORT_ELBOW + occupation
            strings.append(occupations_str)
        string = "<br />".join(strings)
        tree = f"<p style='font-size:10px;'>{string}</p>"
        st.markdown(tree, unsafe_allow_html=True)
        definition = f"<p style='font-size:10px;'>{description}</p>"
        st.markdown(definition, unsafe_allow_html=True)
        if taxonomy:
            taxonomy_text = taxonomy[0:5]
            taxonomy_text_string = "<br />".join(taxonomy_text)
            taxonomy_text_string = f"Efterfrågade kompetenser:<br />{taxonomy_text_string}"
            taxonomy_text = f"<p style='font-size:10px;'>{taxonomy_text_string}</p>"
            st.markdown(taxonomy_text, unsafe_allow_html=True)

def show_info_selected(description):
    definition = f"<p style='font-size:10px;'>{description}</p>"
    st.markdown(definition, unsafe_allow_html=True)

def show_initial_information():
    st.logo("af-logotyp-rgb-540px.jpg")
    st.title("Yrkesväljare")
    initial_text = "Vill du starta om tryck cmd + r"
    st.markdown(f"<p style='font-size:12px;'>{initial_text}</p>", unsafe_allow_html=True)

def change_state_chosen_background():
    st.session_state.chosen_background = False

def initiate_session_state():
    if "chosen_background" not in st.session_state:
        st.session_state.chosen_background = False
        st.session_state.stored_backgrounds = []
        st.session_state.words_of_experience = []
        st.session_state.words_of_interest = []
        st.session_state.similar_occupations = []

    if len(st.session_state.stored_backgrounds) > 2:
        st.button("Testa om annons- och utbildningsdata kan hjälpa dig att upptäcka dina dolda kompetenser") #on_click = ?

    if st.session_state.chosen_background == True:
        st.button("Lägga till fler yrkes- eller utbildningsbakgrunder", on_click = change_state_chosen_background)


def create_valid_options(input, fields, groups, occupations, titles):
    output = {}
    if fields:
        output = output | dict(sorted(st.session_state.options_field.items(), key = lambda item: item[0]))
    if groups:
        output = output | dict(sorted(st.session_state.options_ssyk_level_4.items(), key = lambda item: item[0]))
    if occupations:
        output = output | dict(sorted(st.session_state.options_occupations.items(), key = lambda item: item[0]))
    if titles:
        output = output | dict(sorted(st.session_state.options_titles.items(), key = lambda item: item[0]))
    return output

def post_selected_ssyk_level_4(id_ssyk_level_4):
    ssyk_level_4_definition = st.session_state.definitions.get(id_ssyk_level_4)
    show_info_selected(ssyk_level_4_definition)
    occupation_name_options = {}
    for o in st.session_state.occupationdata[id_ssyk_level_4].related_occupation:
        occupation_name_options[st.session_state.occupationdata[o].showname] = st.session_state.occupationdata[o].id
    choose_occupation_name(occupation_name_options)

def post_selected_occupation(id_occupation):
    related_fields = st.session_state.occupationdata[id_occupation].related_occupation_fields
    related_fields_names = []
    for f in related_fields:
        related_fields_names.append(st.session_state.occupationdata[f].showname)
    related_fields_str = "<br />".join(related_fields_names)
    related_groups = st.session_state.occupationdata[id_occupation].related_occupation_groups
    related_groups_names = []
    for g in related_groups:
        related_groups_names.append(st.session_state.occupationdata[g].showname)
    related_groups_str = "<br />".join(related_groups_names)
    definition_occupation = st.session_state.definitions.get(id_occupation)
    related_taxonomy = st.session_state.taxonomy.get(id_occupation)
    show_info_selected_sidebar(related_fields_str, related_groups_str, st.session_state.occupationdata[id_occupation].showname, definition_occupation, related_taxonomy)
    

def choose_ssyk_level_4(field_id):
    ssyk_level_4_options = {}
    for g in st.session_state.occupationdata[field_id].related_occupation_groups:
        ssyk_level_4_options[st.session_state.occupationdata[g].showname] = st.session_state.occupationdata[g].id
    valid_ssyk_level_4 = list(ssyk_level_4_options.keys())
    selected_ssyk_level_4 = st.selectbox(
        "Välj en yrkesgrupp",
        (valid_ssyk_level_4), placeholder = "", index = None)
    if selected_ssyk_level_4:
        id_selected_ssyk_level_4 = ssyk_level_4_options.get(selected_ssyk_level_4)
        ssyk_level_4_definition = st.session_state.definitions.get(id_selected_ssyk_level_4)
        post_selected_ssyk_level_4(id_selected_ssyk_level_4)

def choose_occupation_name(dict_valid_occupations):
    valid_occupations = list(dict_valid_occupations.keys())
    selected_occupation_name = st.selectbox(
        "Välj en yrkesbenämning",
        (valid_occupations), placeholder = "", index = None)
    if selected_occupation_name:
        id_selected_occupation = dict_valid_occupations.get(selected_occupation_name)
        post_selected_occupation(id_selected_occupation)
        
def choose_occupational_background():
    st.session_state.occupationdata = import_occupationdata()
    st.session_state.definitions = import_data("id_definitions.json")
    st.session_state.taxonomy = import_data("id_taxonomy.json")

    col1, col2 = st.columns(2)

    with col1:
        exclude_fields = st.toggle("inkludera yrkesområden", value = True)
        exclude_groups = st.toggle("inkludera yrkesgrupper", value = False)

    with col2:
        exclude_occupations = st.toggle("inkludera yrkesbenämningar", value = False)
        exclude_titles = st.toggle("inkludera jobbtitlar", value = False)

    valid_options_dict = create_valid_options(st.session_state.occupationdata, exclude_fields, exclude_groups, exclude_occupations, exclude_titles)
    valid_options_list = list(valid_options_dict.keys())

    selected_option_occupation_field = st.selectbox(
    "Välj ett yrke/område som du tidigare har arbetat som/inom",
    (valid_options_list), placeholder = "", index = None)

    if selected_option_occupation_field:
        id_selected_option_occupation_field = valid_options_dict.get(selected_option_occupation_field)
        type_selected_option_occupation_field = st.session_state.occupationdata[id_selected_option_occupation_field].type

        if type_selected_option_occupation_field == "yrkesområde":
            field_definition = st.session_state.definitions.get(id_selected_option_occupation_field)
            show_info_selected(field_definition)
            choose_ssyk_level_4(id_selected_option_occupation_field)

        if type_selected_option_occupation_field == "yrkesgrupp":
            post_selected_ssyk_level_4(id_selected_option_occupation_field)

        if type_selected_option_occupation_field == "jobbtitel":
            occupation_name_options = {}
            for o in st.session_state.occupationdata[id_selected_option_occupation_field].related_occupation:
                occupation_name_options[st.session_state.occupationdata[o].showname] = st.session_state.occupationdata[o].id            
            choose_occupation_name(occupation_name_options)

        if type_selected_option_occupation_field == "yrkesbenämning":
            post_selected_occupation(id_selected_option_occupation_field)

def main ():
    show_initial_information()
    initiate_session_state()
    import_options()
    choose_occupational_background()

if __name__ == '__main__':
    main ()
