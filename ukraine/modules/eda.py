import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
from nltk.tokenize import word_tokenize

sns.set_style('darkgrid')

class TextExploratory:
    """
    Exploratory Data Analysis performed on extracted text.
    """

    def __init__(self, df: pd.DataFrame, text_column):

        self.df = df
        self.text_column = text_column

    def word_count(self):
        """Generate word_count column in data df"""

        self.df.loc[:, 'word_count'] = self.df[self.text_column] \
                            .apply(lambda x: len(str(x).split(' ')))

    def plot_distribution(self, save_image=False, save_path=None):
        """Plot a histogram of the word counts of raw text"""

        self.fig = plt.figure(figsize=(10, 5))

        plt.hist(self.df['word_count'], bins=20, color='#60505C')
        plt.title('Distribution - Document Word Count', fontsize=16)
        plt.ylabel('Frequency', fontsize=12)
        plt.xlabel('Word Count', fontsize=12)
        plt.yticks(np.arange(0, 2500, 200))
        plt.xticks(np.arange(0, 1500, 200))

        if save_image:
            self.fig.savefig(save_path+'word_count_histogram.png',
                                dpi=self.fig.dpi,
                                bbox_inches='tight')

    def plot_boxplot(self, save_image=False, save_path=None):
        """Plot a boxplot of the word counts of raw text"""

        self.fig = plt.figure(figsize=(10, 5))

        sns.boxplot(x=self.df['word_count'], color='#60505C')

        plt.xlabel("Word Count", fontsize=12)
        plt.title('Distribution - Document Word Count', fontsize=16)

        if save_image:
            self.fig.savefig(save_path+'word_count_boxplot.png',
                                dpi=self.fig.dpi,
                                bbox_inches='tight')

    def get_n_most_frequent(self, n, text_column, plot=False):
        """Plot the top n most common words among all documents"""

        self.df.loc[:, 'tokens_text'] = self.df[text_column].apply(
            lambda x: word_tokenize(x))

        self.p_text = self.df['tokens_text']
        self.p_text = [item for sublist in self.p_text for item in sublist]

        self.top_n = pd.DataFrame(Counter(self.p_text).most_common(n),
                              columns=['word', 'frequency'])

        self.fig = plt.figure(figsize=(20, 7))
        g = sns.barplot(x='word',
                        y='frequency',
                        data=self.top_n,
                        palette='GnBu_d')

        g.set_xticklabels(g.get_xticklabels(), rotation=45, fontsize=14)

        plt.yticks(fontsize=14)
        plt.xlabel('Words', fontsize=14)
        plt.ylabel('Frequency', fontsize=14)
        plt.title(f'Top {n} Words', fontsize=17)

    def get_corpus_count(self):

        corpus_count = dict(Counter(self.p_text))
        self.corpus_dict = sorted(corpus_count.items(),
                key=lambda x: x[1], reverse=True)

    def plot_wordcloud(self, text_column: str, category: str, target:int)->None:
        """Show most commonly used words in each target class with wordcloud"""

        words = ' '.join(self.df[self.df['Indentifier'] == category][text_column].values)

        plt.rcParams['figure.figsize'] = 10, 20
        wordcloud = WordCloud(stopwords=STOPWORDS,
                            background_color='white',
                            max_words=1000).generate(words)

        plt.title('WordCloud For {}'.format(category))
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()