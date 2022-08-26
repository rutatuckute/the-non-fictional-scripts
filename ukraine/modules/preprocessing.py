import re
import nltk
import spacy
import string
import unidecode
import contractions
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import inflect
p = inflect.engine()

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nlp = spacy.load('en_core_web_sm')

postags_selected = ['NN', 'NNP', 'NNS', 'JJ', 'RB', 'CD']

class TextPreprocessing:
    """
    TextPreprocessing allows to preprocess extracted text.
    """

    def __init__(self,
                 text,
                 allowed_postags=None):

        self.text = text
        self.allowed_postags = allowed_postags

        self.text = self.text.lower()
        self.text = re.sub(' +', ' ', self.text)

        self.remove_accents()
        self.strip_html_tags()
        self.expand_contractions()
        self.remove_url()
        self.remove_punctuation()
        self.remove_digits()
        self.remove_stopwords()
        self.lemmatize()
        self.remove_stopwords()

    def remove_accents(self):
        """Remove accented characters from text"""

        self.text = unidecode.unidecode(self.text)

    def strip_html_tags(self):
        """Remove html tags from text"""

        soup = BeautifulSoup(self.text, 'html.parser')
        self.text = soup.get_text(separator=' ')

    def expand_contractions(self):
        """Expand shortened words, e.g. don't to do not"""

        self.text = contractions.fix(self.text)

    def remove_punctuation(self):
        """Remove punctuation"""

        self.text = ''.join([w for w in self.text if w not in string.punctuation])

    def remove_digits(self):
        """Remove digits"""

        self.text = ''.join(w for w in self.text if not w.isdigit())

    def remove_stopwords(self):
        """Remove stopwords"""

        self.nlp_stopwords = list(nlp.Defaults.stop_words)
        self.nltk_stopwords = stopwords.words('english')
        self.all_stopwords = list(set(self.nlp_stopwords+
                                    self.nltk_stopwords))

        word_tokens = word_tokenize(self.text)
        self.text = [w for w in word_tokens if not w in self.all_stopwords]
        self.text = ' '.join(self.text)

    def remove_url(self):
        """Remove url addresses"""

        self.text = re.sub(r'http\S+', '', self.text)

    def lemmatize(self):
        """Lemmatize text"""

        lemmatizer = WordNetLemmatizer()
        word_tokens = word_tokenize(self.text)

        if self.allowed_postags:
            self.text = [lemmatizer.lemmatize(w) for (w, pos) in pos_tag(word_tokens)
                                                if pos in self.allowed_postags]
        else:
            self.text = [lemmatizer.lemmatize(w) for w in word_tokens]

        self.text = ' '.join(self.text)