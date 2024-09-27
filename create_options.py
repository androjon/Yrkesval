def create_options(input):
    options_all = {}
    options_field = {}
    options_ssyk_level_4 = {}
    options_occupations = {}
    options_titles = {}
    for v in input.values():
        options_all[v.showname] = v.id
        if v.type == "yrkesområde":
            options_field[v.showname] = v.id
        elif v.type == "yrkesgrupp":
            options_ssyk_level_4[v.showname] = v.id
        elif v.type == "yrkesbenämning":
            options_occupations[v.showname] = v.id
        elif v.type == "jobbtitel":
            options_titles[v.showname] = v.id
    return options_all, options_field, options_ssyk_level_4, options_occupations, options_titles