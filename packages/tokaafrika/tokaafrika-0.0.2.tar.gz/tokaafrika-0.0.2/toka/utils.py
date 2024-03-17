LANGUAGE_CODES_DESCRIPTIONS = {
    "eng":"english",
    "sep":"sepedi",
    "afr":"afrikaans",
    "tsn":"setswana",
    "nbl":"isindebele",
    "ssw":"siswati",
    "xho":"isixhosa",
    "ven":"tshivenda",
    "zul":"isizulu",
    "tso":"xitsonga",
    "sot":"sesotho",
    "nuu":"n|uu",
}

CLASSIFICATION_LABELS = {

}

SENTIMENT_LABELS = {
    "eng":["Happy", "Angry", "Sad", "Neutral"],
    "sep":["Lethabo", "Befetšwe", "Manyami", "Magareng"],
    "afr":["Bly", "Kwaad", "Hartseer", "Neutraal"],
    "sot":["Ho thaba", "Ho halefa", "Hlonama", "Bogareng"],
    "ssw":["Bajabule", "Utfukutsele", "Lusizi", "Lesemkhatsini"],
    "nbl":["Thabile", "Kwatile", "Danile", "Ukungathathi ihlangothi"],
    "xho":["Bonwabile", "Unomsindo", "Ubuhlungu", "Ukungathathi icala"],
    "ven":["Takala", "Sinyuwa", "Ṱungufhadzaho", "Vhukati"],
    "zul":["Jabulile", "Ethukuthele", "Kuyadabukisa", "Ukungathathi hlangothi"],
    "tso":["Tsaka", "Hlundzukile", "Gome", "Xikarhi"],
    "tsn":["O itumetse", "Go Galefa", "Hutsafala", "Bogare"],
    "nuu":["Khôea", "ǀ'aaka", "ǀe ke ʘ'ui'i", "Kx'u xaoke"],
}


LANGUAGE_DESCRIPTIONS_CODES = {
    "english": "eng",
    "sepedi": "sep",
    "afrikaans": "afr",
    "setswana": "tsn",
    "isindebele": "nbl",
    "siswati": "ssw",
    "isixhosa": "xho",
    "tshivenda": "ven",
    "isizulu": "zul",
    "xitsonga": "tso",
    "sesotho": "sot",
    "n|uu": "nuu",
}


STOPWORDS = {
    
'tso': ['a', 'ku', 'hi', 'na', 'u', 'ri', 'ya', 'va',
        'nga', 'swi', 'wa', 'ndzi', 'ka', 'loko', 'ta',
        'yi', 'yena', 'ra', 'vula', 'xi', 'eka', 'wu',
        'xa', 'leswaku', 'nwi', 'le', 'karhi', 'leswi',
        'kutani', 'kambe'],

'ven': ['a', 'vha', 'u', 'na', 'tshi', 'nga', 'ya', 'ndi',
        'o', 'khou', 'ni', 'uri', 'hu', 'ha', 'kha', 'i',
        'zwi', 'tsha', 'ri', 'yo', 'wa', 'ho', 'vho', 'musi',
        'ḽa', 'zwa', 'ḓo', 'amba', 'nahone', 'no'],

'ssw': ['kutsi','futsi','kwasho','kakhulu','wakhe','make',
        'ngesikhatsi', 'kodvwa','babe','yini','wabese','kute',
        'lapho', 'kepha', 'yakhe', 'kakhulu','nje','tonkhe',
        'bese','neo', 'noma','kwabuta','etulu', 'kanye',
        'tilwane', 'khona', 'lapha', 'sikhatsi', 'watsi', 'manje'],

'tsn': ['a', 'o', 'go', 'le', 'ne', 'e', 'mo', 'ka', 'ga', 'ya', 
        'ba', 'ke', 'se', 'di', 'mme', 'kwa', 'fa', 'gore', 're', 
        'tse', 'tsa', 'la', 'wa', 'sa', 'gagwe', 'nna', 'fela', 
        'bua', 'bona', 'na'],

'nso': ['a', 'ho', 'le', 'o', 'ka', 'e', 'ya', 'ha', 'ba', 'ne', 
        'ke', 'mme', 'se', 'di', 'sa', 'wa', 'hore', 're', 'tse', 
        'hae', 'tsa', 'la', 'rialo', 'na', 'tla', 'mo', 'empa', 
        'eo', 'bona', 'ntse'],

'sep': ['a', 'go', 'ka', 'o', 'le', 'ya', 'ba', 'ke', 'e', 'be', 
        'ile', 'se', 'wa', 'la', 'gomme', 'ga', 'sa', 'tša', 'gore', 
        'di', 're', 'ge', 'mo', 'ye', 'realo', 'gagwe', 'gwa', 'tše', 
        'na', 'efela'],
                
'zul': ['ukuthi', 'kusho', 'futhi', 'kodwa', 'kakhulu', 'lapho', 'kanye',
        'ngesikhathi', 'ukuze', 'wakhe', 'nje', 'umama', 'noma', 'kubuza',
        'zonke', 'uma', 'ngabe', 'bese', 'yini', 'kwasho', 'wase', 'uneo', 
        'izilwane', 'yena', 'ngakho', 'kakhulu', 'lakhe', 'phezulu', 
        'ubaba', 'kanjani'],
                
'xho': ['ukuba', 'watsho', 'kodwa', 'waza', 'kakhulu', 'wakhe', 'ke', 'kwaye',
        'nje', 'xa', 'umama', 'yakhe', 'utata', 'wabuza', 'emva', 'nto', 
        'into', 'ngoko', 'zonke', 'izilwanyana', 'le', 'ngoku', 'uneo', 
        'yonke', 'lo', 'okanye', 'ingaba', 'wathi', 'loo', 'yaye'],

'nbl': ['bona', 'kodwana', 'kutjho', 'lokha', 'kwatjho', 'begodu', 'khulu',
        'bonyana', 'phasi', 'bese', 'uneo', 'le', 'wase', 'ngemva', 'besele',
        'kobana', 'ukuthi', 'phezulu', 'njengombana', 'zoke', 'kuhle', 
        'izinto', 'lakhe', 'kubuza', 'ugogo', 'ilanga', 'nanyana', 'woke',
        'khulu'],

 'afr': ['die', 'en', 'n', 'sy', 'is', 'te', 'hy', 'het', 'om', 'haar', 'vir',
         'in', 'nie', 'van', 'sê', 'ek', 'wat', 'dit', 'toe', 'hulle', 'jy', 
         'op', 'gaan', 'ons', 'kan', 'na', 'met', 'se', 'jou', 'nie'],

 'eng': ['the', 'and', 'to', 'a', 'he', 'of', 'you', 'her', 'she', 'was',
        'in', 'that', 'said', 'his', 'i', 'they', 'it', 'on', 'for', 'had',
        'at', 'but', 'all', 'as', 'with', 'so', 'is', 'up', 'what', 'have'],

 'nuu': ['ke', 'ng', 'na', 'a', 'he', 'u', 'ka', 'ku', 'nǀa', 'si', 'jha', 
        'kin', 'ha', 'ni', 'sa', 'ǂhina', 'ʘone', 'ga', 'se', 'kx’u', 
        'nǀii', 'ki', 'n|a', 'kua', 'nǁaa', 'ǁ’aa']

}