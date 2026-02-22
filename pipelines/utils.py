import unicodedata

#we will recognise these strings as province or terratory names
canadian_provinces_territories = [
    {
        "name": "Alberta",
        "alternates": ["Alberta", "AB"]
    },
    {
        "name": "British Columbia",
        "alternates": ["British Columbia", "B.C.", "Colombie-Britannique", "BC"]
    },
    {
        "name": "Manitoba",
        "alternates": ["Manitoba", "MB"]
    },
    {
        "name": "New Brunswick",
        "alternates": ["New Brunswick", "N.B.", "Nouveau-Brunswick", "NB"]
    },
    {
        "name": "Newfoundland and Labrador",
        "alternates": ["Newfoundland and Labrador", "Newfoundland & Labrador", "Terre-Neuve-et-Labrador", "N.L.", "NL"]
    },
    {
        "name": "Nova Scotia",
        "alternates": ["Nova Scotia", "N.S.", "Nouvelle-Écosse", "NS"]
    },
    {
        "name": "Ontario",
        "alternates": ["Ontario", "ON"]
    },
    {
        "name": "Prince Edward Island",
        "alternates": ["Prince Edward Island", "P.E.I.", "Île-du-Prince-Édouard", "PE"]
    },
    {
        "name": "Quebec",
        "alternates": ["Quebec", "Québec", "Q.C.", "QC"]
    },
    {
        "name": "Saskatchewan",
        "alternates": ["Saskatchewan", "Sask.", "SK"]
    },
    {
        "name": "Northwest Territories",
        "alternates": ["Northwest Territories", "N.W.T.", "Territoires du Nord-Ouest", "NT"]
    },
    {
        "name": "Nunavut",
        "alternates": ["Nunavut", "NU"]
    },
    {
        "name": "Yukon",
        "alternates": ["Yukon", "Y.T.", "YT"]
    }
]

def normalize_text(text: str):
    """Convert accented characters to their unaccented equivalents."""
    return ''.join(
        c for c in unicodedata.normalize('NFKD', text) #chanage accented letters to non-accented
        if not unicodedata.combining(c) #remove accents on their own
    ).lower()

def extract_provinces(text: str):
    """
    Return a list of province/territory names found in "text"
    
    - Recognizes alternative using above dict
    - Returns each province only once
    - Is not case-sensitive
    """
    import re

    found = []

    text_norm = normalize_text(text)

    #search for each province
    for province in canadian_provinces_territories:

        # search for each alternative name for the province
        patterns = [province["name"]] + province.get("alternatives", [])
        for pat in patterns:
            pat_with_boundary = r"\b" + normalize_text(pat) + r"\b"

            if re.search(pat_with_boundary, text_norm):
                found.append(province["name"])
                break  # No need to check other alternatives

    return ' and '.join(found) #in case multiple province are mentioned