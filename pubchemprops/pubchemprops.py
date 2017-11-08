"""
	This is a module for getting various data from PubChem using it's amazing
	PUG REST API. More info can be found within functions docs.

	Copyright 2017 Maxim Shevelev <mdshev7@gmail.com>

	For details about PubChem's PUG REST API please visit
	https://pubchem.ncbi.nlm.nih.gov/pug_rest/PUG_REST.html
"""

import urllib.request, json, requests


def pubchem_parsing(url):
    """
        Get the link to PubChem API, parse it for JSON and then translate that
        to Python dictionary;
        This is just to follow the DRY principle
    """
    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req).read()
    fin = json.loads(res.decode())
    return fin


def get_cid_by_name(compound_name):
    """
        1. Accepts the compound name
        2. Searches PubChem by this name
        3. Returns the compound's PubChem CID
    """

    # Construct the link to PubChem's PUG REST API
    pubchem_record_link = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
    pubchem_record_link += "name/%s/record/JSON" % compound_name

    # Parse the JSON received from PubChem to Python Dictionary
    general_info = pubchem_parsing(pubchem_record_link)

    # Get the CID
    compound_cid = general_info['PC_Compounds'][0]['id']['id']['cid']

    return compound_cid


def get_first_layer_props(compound_name, first_layer_props):
    """
        1. Accepts the compound name as a String and the required first layer
           props as a List
        2. Finds its CID
        3. Creates a link to PubChem PUG REST API to get the required properties
        4. Returns a dictionary with the required props
        NOTE: <First layer props> means that these properties can be directly
              accessed via the convenient PubChem PUG REST API
    """
    compound_cid = get_cid_by_name(compound_name)

    # Make a string out of the required first layer props list
    req_props_string = ','.join(first_layer_props)

    pubchem_pug_rest_api_link = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
    pubchem_pug_rest_api_link += "compound/cid/%s/property/%s/JSON" % (
        compound_cid, req_props_string)

    first_layer_props_data = pubchem_parsing(pubchem_pug_rest_api_link)['PropertyTable']['Properties'][0]

    return first_layer_props_data


def get_second_layer_props(compound_name, required_properties):
    """
        1. Accepts the compound name
        2. Gets the CID for this compound
        3. Searches PubChem for data for the specified CID
        4. Cycles through the fetched data to select required fields
        5. Returns a dictionary with specified properties of specified compound

        NOTE: <Second layer properties> means that these properties can not be
              accessed directly via the PubChem PUG REST API.
    """
    # Get the compound's PubChem CID
    compound_cid = get_cid_by_name(compound_name)

    # Contsruct the link
    pubchem_all_data_link = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/"
    pubchem_all_data_link += "data/compound/%s/JSON" % compound_cid

    # Get the JSON from the constructed link and convert it to Python Dictionary
    all_the_data = pubchem_parsing(pubchem_all_data_link)

    # Get to the data sections, get rid of References
    data_sections = all_the_data['Record']['Section']

    """
        Out of all the sections

        (2D structure, 3D conformer, LCSS, Names and Idenrifers, Chemical and 
        Physical Properties, Related Records, Chemical Vendors, Food additives, 
        Agrochemical Info, Pharmacology and Biochemistry, Use and Manufacturing,
        Identification, Safety and Hazards, Toxicity, Literature, Patents, 
        Biomolecular Interactions, Biological Tests Result, Classification)

        choose only the most chemically interesting ones: 

        <Names and Identifies> and <Chemical and Physical Properties>
    """

    # this could be customizable, actually - please send PR or raise an issue
    # if you'd like to have this done
    sections_of_interests = ['Names and Identifiers',
                             'Chemical and Physical Properties']

    # Empty array to store all the data of the sections of interes
    sections_of_interests_data = []

    # the required parameters can be accesed via
    # dictionary in the array => Section => TOCHeading == 'parameter name' =>
    # => Information

    # Construct an array of only interesting data
    for section_title in sections_of_interests:
        sample_list = list(filter(lambda section: section['TOCHeading'] == section_title, data_sections))
        sections_of_interests_data.append(sample_list[0])

    # However, we are still away from getting the parameters values
    # The sections_of_interests_data contains lots of interesting information,
    # however it is not that useful for the chemist's everyday usage,
    # so I limit the data we can get to 3 identifiers listed below:

    required_identifiers = ['Computed Descriptors',
                            'Other Identifiers',
                            'Experimental Properties']

    # The data for each identifier (stated above) will be stored in this array
    # To get the parameters for these identifiers one will have to look for
    # dictionary => 'Section' array, which will yield yet another array,
    # but this time it will be full of parameters one can grab
    all_pubchem_data_array_for_section = []

    # if section_dictionary['Section'] contains a dictionary with
    # 'TOCHeading' equaling to anything from required_identifiers,
    # add the matching dictionary into the new array initialized above
    for section_dictionary in sections_of_interests_data:
        sample_list = list(
            filter(lambda section: section['TOCHeading'] in required_identifiers, section_dictionary['Section']))
        all_pubchem_data_array_for_section = all_pubchem_data_array_for_section + sample_list

    # it's not full, though, you can also extract more data from PubChem
    # but I've just found these parameters to be of the most interest
    # for a chemist's everyday use
    list_of_all_possible_params = ['IUPAC Name',
                                   'InChI',
                                   'InChI Key',
                                   'Canonical SMILES',
                                   'Wikipedia',
                                   'Boiling Point',
                                   'Melting Point',
                                   'Flash Point',
                                   'Solubility',
                                   'Density',
                                   'Vapor Density',
                                   'Vapor Pressure',
                                   'LogP',
                                   'Stability',
                                   'Auto-Ignition',
                                   'Viscosity',
                                   'Heat of Combustion',
                                   'Heat of Vaporization',
                                   'Surface Tension',
                                   'Ionization Potential',
                                   'Dissociation Constants']

    # this array will later store the data about requested parameters
    # in the PubChem format
    required_data_in_pubchem_format = []

    for molecule_desc_object in all_pubchem_data_array_for_section:
        sample_list = list(
            filter(lambda section: section['TOCHeading'] in required_properties, molecule_desc_object['Section']))
        required_data_in_pubchem_format = required_data_in_pubchem_format + sample_list

    # Final dictionary of compound properties that will be returned in the end
    compound_properties_dictionary = {}

    for property_object in required_data_in_pubchem_format:
        compound_properties_dictionary[property_object['TOCHeading']] = property_object['Information']

    return compound_properties_dictionary



# print(get_second_layer_props('acetone', ['IUPAC Name', 'Canonical SMILES', 'Boiling Point', 'Vapor Pressure', 'LogP']))
# print(get_cid_by_name('methane'))
# print(get_first_layer_props('acetone', ['MolecularWeight', 'IUPACName']))