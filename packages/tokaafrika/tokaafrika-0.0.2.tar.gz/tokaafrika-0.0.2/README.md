# Toka (`tokaafrika`)

Justice for African Languages

---

This package helps with utility functions to provide african language `StopWords` and helps in generating the new `StopWords` with ease and help in cleaning the text dataset, We are working on improving it and help you get reliable `StopWords` and `Quality Aligned Datasets`.

#### Currently we support the following languages

- Throughout our application we will use the language code or description of the language interchangiably, this mean we will use the description of language code consistently. Refer to the table below.

| Language Code / ISO CODE | Language Name |
| :----------------------- | ------------: |
| eng                      |       English |
| sep                      |        Sepedi |
| afr                      |     Afrikaans |
| tsn                      |      Setswana |
| nbl                      |    isiNdebele |
| ssw                      |       Siswati |
| xho                      |      isiXhosa |
| ven                      |     Tshivenda |
| zul                      |       isiZulu |
| tso                      |      Xitsonga |
| sot                      |       Sesotho |
| nuu                      |     N&#124;uu |

## Installation

### Dependencies

We are using type hinting on this project.

- Toka-api requires  
  `python>=3.9.13`

---

To get started started and install the package execute the following.

```bash
>>> pip install tokaafrika==0.0.1
```

To start using the package, follow the steps below

### Get `StopWords` - (Prebuild Stopwords )

At the moment the `StopWords` are based on `South African Languages` including `N|uu`

```python
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
```

### To Clean Symbols

This helps in cleaning symbols ensuring your data is clean and free of symbols

```python

>>> from toka.toka import TokaAPI
>>> toka_object = TokaAPI()
>>> clean_text = \
>>> ... toka_object.clean_symbols('Hello! This is an example\
>>> ... text with numbers like 123 ')
>>> print(clean_text)
>>> hello this is an example text with numbers like
```

### Get Frequent Words

This helps in quickly getting the frequent words and how many times is appears from given text

```python
>>> from toka.toka import TokaAPI
>>> toka_object = TokaAPI()
>>> english = toka_object.get_frequent_words('Hello test')
>>> print(english)
{'hello': 1, 'test': 1}
```

### Compute `StopWords `

This helps with in computing the stop words from given documents or text, it is accurate when using long text or big document

```python
>>> from toka.toka import TokaAPI
>>> api = TokaAPI()
>>> stopwords = api.compute_stopwords(
...    "the the are are the are on the on", 3)
>>> print(stopwords)
['the', 'are', 'on']
```

### Load model

This Assummes you have vectorizer pickle and model that is already trained and are both pickle files

```python
>>> from toka.toka import TokaAPI
>>> api = TokaAPI()
>>> model = 'model.pkl'
>>> vector = 'vector.pkl'
>>> clf, vector = api.load_model_from_pickle(model,
...                     vector)
```

### Development

We welcome new contribution and if you have spotted a bug or have ideas around the improvement leave then in issues or fork the repo and develop the feature and create PR to merge the changes to the repository, ensure tests are written with edge cases.

# Citations

If you used`tokaafrika` package and it helped you a lot we would appreciate citations.

```latex
@article{tokaafrika,
  title={tokaafrika: African Languages - Machine Learning Package},
  author={Ofentswe Lebogo, Shaun Damon},
  howpublished={\url{https://pypi.org/project/tokaafrika/}},
  year={2024}
}

```
