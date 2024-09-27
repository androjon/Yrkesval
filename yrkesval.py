import streamlit as st
import json
import itertools
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
def import_options(input):
    options_all, options_field, options_ssyk_level_4, options_occupations, options_titles = create_options(input)
    return options_all, options_field, options_ssyk_level_4, options_occupations, options_titles

@st.cache_data
def show_info_selected(fields, groups, occupation, title, description):
    with st.sidebar:
        PIPE = "│"
        ELBOW = "└──"
        SHORT_ELBOW = "└─"
        LONG_ELBOW = "    └──"
        TEE = "├──"
        PIPE_PREFIX = "│   "
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
        if title:
            title_str = SPACE_PREFIX + SPACE_PREFIX + SHORT_ELBOW + title
            strings.append(title_str)
        string = "<br />".join(strings)
        tree = f"<p style='font-size:8px;'>{string}</p>"
        st.markdown(tree, unsafe_allow_html=True)

        text = f"<p style='font-size:12px;'>{description}</p>"
        st.markdown(text, unsafe_allow_html=True)

st.logo("af-logotyp-rgb-540px.jpg")

st.title("Yrkesväljare")

text1 = "Vill du starta om tryck cmd + r"
st.markdown(f"<p style='font-size:12px;'>{text1}</p>", unsafe_allow_html=True)

data_occupations = import_occupationdata()

options_all, options_field, options_ssyk_level_4, options_occupations, options_titles = import_options(data_occupations)

descriptions = import_data("id_definitions.json")

st.write("Välj nedan om du vill exkludera något från den översta rullistan")

col1, col2 = st.columns(2)

with col1:
    exclude_field = st.toggle("yrkesområden", value = False)
    exclude_groups = st.toggle("yrkesgrupper", value = False)

with col2:
    exclude_occupations = st.toggle("yrkesbenämningar", value = False)
    exclude_titles = st.toggle("jobbtitlar", value = False)

valid_options_dict = {}

if exclude_field == False:
    valid_options_dict = valid_options_dict | options_field
if exclude_groups == False:
    valid_options_dict = valid_options_dict | options_ssyk_level_4
if exclude_occupations == False:
    valid_options_dict = valid_options_dict | options_occupations
if exclude_titles == False:
    valid_options_dict = valid_options_dict | options_titles

valid_options_list = sorted(list(valid_options_dict.keys()))

selected_option = st.selectbox(
    "Välj ett yrke/område som du tidigare har arbetat som/inom",
    (valid_options_list), placeholder = "", index = None)

if selected_option:
    id_selected_option = valid_options_dict.get(selected_option)
    type_selected_option = data_occupations[id_selected_option].type
    related_field_names = []
    related_group_names = []
    related_occupation_names = []
    for f in data_occupations[id_selected_option].related_occupation_fields:
        related_field_names.append(data_occupations[f].id)
    for g in data_occupations[id_selected_option].related_occupation_groups:
        related_group_names.append(data_occupations[g].id)
    for o in data_occupations[id_selected_option].related_occupation:
        related_occupation_names.append(data_occupations[o].id)

    if type_selected_option == "yrkesområde":
        description = descriptions.get(id_selected_option)
        show_info_selected(data_occupations[id_selected_option].showname, None, None, None, description)
        valid_group_names_dict = {}
        for g in related_group_names:
            valid_group_names_dict[data_occupations[g].name] = g
        valid_group_names_list = sorted(list(valid_group_names_dict.keys()))
        selected_option_below_field = st.selectbox(
            "Välj en yrkesgrupp",
            (valid_group_names_list), placeholder = "", index = None)
        
        if selected_option_below_field:
            id_selected_group = valid_group_names_dict.get(selected_option_below_field)
            description = descriptions.get(id_selected_group)
            show_info_selected(data_occupations[id_selected_option].showname, data_occupations[id_selected_group].showname, None, None, description)
            related_occupation_names = data_occupations[id_selected_group].related_occupation
            valid_occupation_names_dict = {}
            for g in related_occupation_names:
                valid_occupation_names_dict[data_occupations[g].name] = g
            valid_occupation_names_list = sorted(list(valid_occupation_names_dict.keys()))
            selected_option_below_group = st.selectbox(
                "Välj en yrkesbenämning",
                (valid_occupation_names_list), placeholder = "", index = None)
            
            if selected_option_below_group:
                id_selected_option_below_group = valid_occupation_names_dict.get(selected_option_below_group)
                description = descriptions.get(id_selected_option_below_group)
                show_info_selected(data_occupations[id_selected_option].showname, data_occupations[id_selected_group].showname, data_occupations[id_selected_option_below_group].showname, None, description)
    
    elif type_selected_option == "yrkesgrupp":
        name = data_occupations[id_selected_option].showname
        related_fields = data_occupations[id_selected_option].related_occupation_fields
        related_fields_names = []
        for f in related_fields:
            related_fields_names.append(data_occupations[f].showname)
        related_fields_str = " & ".join(related_fields_names)
        description = descriptions.get(id_selected_option)
        show_info_selected(related_fields_str, name, None, None, description)

        valid_occupation_names_dict = {}
        for g in related_occupation_names:
            valid_occupation_names_dict[data_occupations[g].name] = g
        valid_occupation_names_list = sorted(list(valid_occupation_names_dict.keys()))
        selected_option_below_group = st.selectbox(
            "Välj en yrkesbenämning",
            (valid_occupation_names_list), placeholder = "", index = None)
        
        if selected_option_below_group:
            id = valid_occupation_names_dict.get(selected_option_below_group)
            name = data_occupations[id].showname
            related_fields = data_occupations[id].related_occupation_fields
            related_fields_names = []
            for f in related_fields:
                related_fields_names.append(data_occupations[f].showname)
            related_fields_str = " & ".join(related_fields_names)
            related_groups = data_occupations[id].related_occupation_groups
            related_groups_names = []
            for g in related_groups:
                related_groups_names.append(data_occupations[g].showname)
            related_groups_str = " & ".join(related_groups_names)
            description = descriptions.get(id)
            show_info_selected(related_fields_str, related_groups_str, name, None, description)

    elif type_selected_option == "jobbtitel":
        valid_occupation_names_dict = {}
        for g in related_occupation_names:
            valid_occupation_names_dict[data_occupations[g].name] = g
        valid_occupation_names_list = sorted(list(valid_occupation_names_dict.keys()))
        selected_option_above_title = st.selectbox(
            "Välj en yrkesbenämning",
            (valid_occupation_names_list), placeholder = "", index = None)
        
        if selected_option_above_title:
            selected_option_above_title_id = valid_occupation_names_dict.get(selected_option_above_title)
            name = data_occupations[selected_option_above_title_id].showname
            related_fields = data_occupations[selected_option_above_title_id].related_occupation_fields
            related_fields_names = []
            for f in related_fields:
                related_fields_names.append(data_occupations[f].showname)
            related_fields_str = " & ".join(related_fields_names)
            related_groups = data_occupations[selected_option_above_title_id].related_occupation_groups
            related_groups_names = []
            for g in related_groups:
                related_groups_names.append(data_occupations[g].showname)
            related_groups_str = " & ".join(related_groups_names)
            description = descriptions.get(selected_option_above_title_id)      
            show_info_selected(related_fields_str, related_groups_str, data_occupations[selected_option_above_title_id].showname, data_occupations[id_selected_option].showname, description)
        
    elif type_selected_option == "yrkesbenämning":
        id = valid_options_dict.get(selected_option)
        name = data_occupations[id].showname
        related_fields = data_occupations[id].related_occupation_fields
        related_fields_names = []
        for f in related_fields:
            related_fields_names.append(data_occupations[f].showname)
        related_fields_str = " & ".join(related_fields_names)
        related_groups = data_occupations[id].related_occupation_groups
        related_groups_names = []
        for g in related_groups:
            related_groups_names.append(data_occupations[g].showname)
        related_groups_str = " & ".join(related_groups_names)
        description = descriptions.get(id)
        show_info_selected(related_fields_str, related_groups_str, name, None, description)   
