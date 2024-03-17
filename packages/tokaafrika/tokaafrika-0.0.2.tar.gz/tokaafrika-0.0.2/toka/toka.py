import re
import pickle
from collections import Counter
from typing import List, Dict, Tuple, Any, Union
from toka.utils import STOPWORDS, LANGUAGE_CODES_DESCRIPTIONS, \
LANGUAGE_DESCRIPTIONS_CODES, SENTIMENT_LABELS, CLASSIFICATION_LABELS

class TokaAPI:
    
    def __init__(self, model_path: str=None, vectorizer_path: str=None):
        """
        """
        self.model_path = model_path 
        self.vectorizer_path = vectorizer_path
        self.model = None 
        self.vectorizer = None

        if model_path and vectorizer_path:
            self.model, self.vectorizer = self.load_model_from_pickle(
                model_filename=self.model_path,
                vectorizer_filename=self.vectorizer_path
            )
        
    
    def get_stopwords(self, language: str = "", default_all: bool = False)\
     -> Union[frozenset, Dict[str, List[str]]]:
        """ Prebuild stop words accross all languages in South Africa

            Attributes
            ----------
            language: this require language name or code
                    (refer to langauge code and name)
            default_all: False, True return all stopwords for all SA 
                        languages including N|uu
            
            Returns
            ----------
            stopwords : stopwords for a language or all
                
            Notes
            ----------
            This can be complemented with some of the stopwords known or can 
            be customized.

            
            Examples
            ----------
            >>> from toka.toka import TokaAPI
            >>> api = TokaAPI()
            >>> stopwords = api.get_stopwords('tshivenda') # use fullname
            >>> print(stopwords)
            frozenset({'a', 'vha', 'u', 'na', 'tshi', 'nga', 'ya', 'ndi',
            ... 'o', 'khou', 'ni', 'uri', 'hu', 'ha', 'kha', 'i',
            ... 'zwi', 'tsha', 'ri', 'yo', 'wa', 'ho', 'vho', 'musi',
            ... 'ḽa', 'zwa', 'ḓo', 'amba', 'nahone', 'no'})
            >>> stopwords = api.get_stopwords('ven') # use shotname/code
            >>> print(stopwords)
            frozenset({'a', 'vha', 'u', 'na', 'tshi', 'nga', 'ya', 'ndi',
            ... 'o', 'khou', 'ni', 'uri', 'hu', 'ha', 'kha', 'i',
            ... 'zwi', 'tsha', 'ri', 'yo', 'wa', 'ho', 'vho', 'musi',
            ... 'ḽa', 'zwa', 'ḓo', 'amba', 'nahone', 'no'})
            >>> .
        """

        if language is not None:
            language = language.lower()
        else:
            raise TypeError("language must be (str), cannot be 'NoneType'")

        if default_all:
            return STOPWORDS
        try:
            if len(language) == 3:
                lang_code = language
            else:
                lang_code = LANGUAGE_DESCRIPTIONS_CODES[language]
            return frozenset(STOPWORDS[lang_code])
        except KeyError:
            raise ValueError(f"language '{language}' name or code not found!")
    

    def clean_symbols(self, text: str) -> str:
        """ Clean symbols in a text like punctuations 
            Attributes
            ----------
            text: text given to clean
            
            Returns
            ----------
            clean_text : removed symbol text
                
            Notes
            ----------
            Assumes the text is not empty 
            
            Examples
            ----------
            >>> from toka.toka import TokaAPI
            >>> toka_object = TokaAPI()
            >>> clean_text = \
            ...    toka_object.clean_symbols('Hello! This is an example\
            ...     text with numbers like 123 ')
            >>> print(clean_text)
            hello this is an example text with numbers like 
            >>> .
        """
        if text is not None:
            clean_text = re.sub(r'[!@#$(),\n"%^*?\:;~`’0-9\[\]]', '', text)
            return clean_text
        else:
            raise TypeError('text must be string!')

    
    def get_frequent_words(self, text: str, clean_symbols: bool = True)\
     -> Dict[str, int]:
        """Count frequent words in a given text
        
            Attributes
            ----------
            text: text to split and count words
            
            Returns
            ----------
            dictionary object with count of each word
                
            Notes
            ----------
            This assumes text is string type
            
            Examples
            ----------
            >>> from toka.toka import TokaAPI
            >>> toka_object = TokaAPI()
            >>> english = toka_object.get_frequent_words('Hello test')
            >>> print(english) 
            {'hello': 1, 'test': 1}
            >>> .
            
        """
        if text is not None:
            if clean_symbols:
                text = self.clean_symbols(text.lower()).split()
            else:
                text = text.lower().split()
            frequency = Counter(text)
            return frequency
        else:
            raise TypeError('text must be string!')
    

    def compute_stopwords(self, text: str, n_words: int) -> List[str]:
        """ This function get the top n most frequent words
            
            Attributes
            ----------
            text: text to use to process the frequency and stopwords
            n_words: number of words to limit
            
            Returns
            ----------
            self : object
                Fitted estimator.
                
            Notes
            ----------
            This assumes text is string and not empty
            
            Examples
            ----------
            >>> from toka.toka import TokaAPI
            >>> api = TokaAPI()
            >>> stopwords = api.compute_stopwords(
            ...    "the the are are the are on the on", 3)
            >>> print(stopwords)
            ['the', 'are', 'on']
            >>> .
            
        """
        top_words = self.get_frequent_words(text)
        top_words = top_words.most_common(n_words)
        top_words = list(list(zip(*top_words))[0])
        return top_words
    
    def load_model_from_pickle(self, model_filename: str, 
                vectorizer_filename: str) -> Tuple[Any, Any]:
        """ Loads pickle files for both vector and its model 
            Attributes
            ----------
            model_filename: path and file name for model
            vectorizer_filename: path and filename for vectorizer
            
            Returns
            ----------
            Tuple : object
                Fitted estimator.
                
            Notes
            ----------
            Model and Vector filename should be of model and vector type
            
            Examples
            ----------
            >>> from toka.toka import TokaAPI
            >>> api = TokaAPI()
            >>> model = 'model.pkl'
            >>> vector = 'vector.pkl'
            >>> clf, vector = api.load_model_from_pickle(model,
            ...                     vector)
            >>> .

        """
        # Load the trained model from the pickle file
        with open(model_filename, "rb") as model_file:
            loaded_model = pickle.load(model_file)

        # Load the vectorizer from the pickle file
        with open(vectorizer_filename, "rb") as vectorizer_file:
            loaded_vectorizer = pickle.load(vectorizer_file)

        return loaded_model, loaded_vectorizer
    
    def lang_code_to_name(self, code: str) -> str:
        """Maps an ISO language code to it's full language name.

            Attributes
            ----------
            code: the iso language code.

            Returns
            ----------
            String: str
                The full name of the language.
 
            Notes
            ----------
            This assumes text is a string and not empty

            Examples
            ----------
            >>> from toka.toka import TokaAPI
            >>> api = tokaAPI()
            >>> iso_code_map = api.lang_code_to_name("xho")
            >>> print(iso_code_map)
            isixhosa
            >>> .
        """
        return LANGUAGE_CODES_DESCRIPTIONS.get(code, 'Unknown Language')
    
    def get_labels(self, language: str, task: str = "sentiment") ->\
        Union[List[str], str]:
        """Get Labels in any languages
        
            Attributes
            ----------
            language: language
            task: options ["sentiment", "classification"]
            
            Returns
            ----------
            List of labels for language passed
                
            Notes
            ----------
            This assumes language is valid
            
            Examples
            ----------
            >>> from toka.toka import TokaAPI
            >>> toka_object = TokaAPI()
            >>> nuu = toka_object.get_labels('N|uu')
            >>> print(nuu) 
            ["Khôea", "ǀ'aaka", "ǀe ke ʘ'ui'i", "Kx'u xaoke"]
            >>> .
            
        """
        if language is not None:
            language = language.lower()
        else:
            raise TypeError("language must be (str), cannot be 'NoneType'")

        try:
            if len(language) == 3:
                lang_code = language
            else:
                lang_code = LANGUAGE_DESCRIPTIONS_CODES[language]

            if task == "sentiment":
                labels = SENTIMENT_LABELS.get(lang_code, 'Unknown Language')
            elif task == "classification":
                labels = CLASSIFICATION_LABELS.get(lang_code, 'Unknown Language')
            return labels
        except KeyError:
            raise ValueError(f"language '{language}' name or code not found!")

    
    def get_label(self, source: str, label: str, target: str, 
                  task: str ="sentiment") -> str:
        """Get Label in any languages
        
            Attributes
            ----------
            source: language 
            label: label to translate 
            target: language
            task: options["sentiment", "classification"]
            
            Returns
            ----------
            Label of target language
                
            Notes
            ----------
            This assumes text is string type
            
            Examples
            ----------
            >>> from toka.toka import TokaAPI
            >>> toka_object = TokaAPI()
            >>> eng_nuu = toka_object.get_label('eng', 'Neutral', 'nuu')
            >>> print(eng_nuu) 
            Kx'u xaoke
            >>> .
            
        """
        
        if source and target:
            source = source.lower()
            target = target.lower()
        else:
            raise TypeError("language must be (str), cannot be 'NoneType'")

        try:
            label = label.capitalize()
            if len(source) == 3 and len(target):
                if task == "sentiment":
                    index = SENTIMENT_LABELS[source].index(label)
                    label_target = SENTIMENT_LABELS[target][index]
                elif task == "classification":
                    index = CLASSIFICATION_LABELS[source].index(label)
                    label_target = CLASSIFICATION_LABELS[target][index]
            else:
                source = LANGUAGE_DESCRIPTIONS_CODES[source]
                target = LANGUAGE_DESCRIPTIONS_CODES[target]
                if task == "sentiment":
                    index = SENTIMENT_LABELS[source].index(label)
                    label_target = SENTIMENT_LABELS[target][index]
                elif task == "classification":
                    index = CLASSIFICATION_LABELS[source].index(label)
                    label_target = CLASSIFICATION_LABELS[target][index]

            return label_target
        except KeyError:
            raise ValueError(f"One of languages name or code not found!")
    
    def inference(self, new_text, batch=None):
        """Get Labels in any languages
        
            Attributes
            ----------
            new_text: text to predict
            model: model 
            vectorizer: Vectorizer
            
            Returns
            ----------
            Label text prediction
                
            Notes
            ----------
            This assumes text is string type
            
            Examples
            ----------
            >>> from toka.toka import TokaAPI
            >>> model_path = "model.pkl"
            >>> vector_path = "vector.pkl"
            >>> toka_object = TokaAPI(
            ... model_path,
            ... vector_path)
            >>> english = toka_object.inference('Hello test')
            >>> print(english) 
            English
            >>> .
            
        """
        # Vectorize the new text using the loaded vectorizer
        new_text = re.sub(r"[@#$(),\n%^*?\:;~`’\[\]0-9]", '', new_text)
        new_text_vectorized = self.vectorizer.transform([new_text])

        # Make predictions using the loaded model
        predictions = self.model.predict(new_text_vectorized)

        return predictions