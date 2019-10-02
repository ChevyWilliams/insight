import numpy as np
import pandas as pd
import csv
import numpy as np
import scipy
import six
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import string
import re
import smart_open as so
import gensim
from gensim.models import KeyedVectors
import pickle


# Load Data
# def load_data():
#     if selection == 'Art/Visual Art/Photography':
#         df = pd.read_pickle('df_art.pkl')
#     elif selection == 'Books/Zine/Print':
#         df = pd.read_pickle('df_book.pkl')
#     elif selection == 'Crafts/Textiles':
#         df = pd.read_pickle('df_craft.pkl')
#     elif selection == 'Design/Architecture':
#         df = pd.read_pickle('df_design.pkl')
#     elif selection == 'Equipment/Tools/DIY':
#         df = pd.read_pickle('df_diy.pkl')
#     elif selection == 'Fashion/Apparel':
#         df = pd.read_pickle('df_fashion.pkl')
#     elif selection == 'Food/Beverage':
#         df = pd.read_pickle('df_food.pkl')
#     elif selection == 'Games/Gaming':
#         df = pd.read_pickle('df_games.pkl')
#     elif selection == 'Media':
#         df = pd.read_pickle('df_media.pkl')
#     elif selection == 'Music':
#         df = pd.read_pickle('df_music.pkl')
#     elif selection == 'Performance Art':
#         df = pd.read_pickle('df_perform.pkl')
#     elif selection == 'Spaces/Places/Events':
#         df = pd.read_pickle('df_events.pkl')
#     elif selection == 'Tech/Web':
#         df = pd.read_pickle('df_tech.pkl')
#     elif selection == 'TV/Film/Webseries':
#         df = pd.read_pickle('df_film.pkl')
#     else:
#         df = pd.read_pickle('df_other.pkl')
#     return df

def load_model():
    filename = 'GoogleNews-vectors-negative300-SLIM.bin'
    emb_model = KeyedVectors.load_word2vec_format(filename, binary=True)
    return emb_model

# Define a function that strips all punctuation and stop words
def stripper(my_str):
    str_low = my_str.lower()
    allpunc = string.punctuation
    pattern = r"[{}]".format(allpunc) # create the pattern
    cleanstr = re.sub(pattern, " ", str_low)
    tokenword = word_tokenize(cleanstr)
    cleanstr = [word for word in tokenword if word not in stopwords.words('english')]
    return cleanstr
