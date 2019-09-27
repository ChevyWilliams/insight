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
def load_data():
    appdf_sub = pd.read_pickle('appdf_sub.pkl')
    filename = 'GoogleNews-vectors-negative300.bin.gz'
    emb_model = KeyedVectors.load_word2vec_format(filename, binary=True)
    return appdf_sub, emb_model

# Define a function that cleans strings: lowercase, remove select punctuation, tokenize
def clean_text(my_str):
    str_low = my_str.lower()
    remove = string.punctuation
    remove = remove.replace(".", " ").replace(",", " ").replace("'", " ")
    pattern = r"[{}]".format(remove) # create the pattern
    cleanstr = re.sub(pattern, " ", str_low)
    finalword = word_tokenize(cleanstr)
    return finalword



# def ideavetter():
#     if request.method == 'POST':
#         for aKey in request.form:
#             if aKey == 'pitch':
#                 text = request.form[aKey]
#         # text = request.form('pitch')
#
#         print(request.form['pitch'])
#         print(text)
#
#         appdf_sub, emb_model = load_data()
#     # accept user input
#         # text = input("Pitch your idea here: ")
#
#     # clean and tokenize user input
#         clean_input = clean_text(text)
#
#     # get vectors for input text
# #     input_vecs = get_vectors(clean_input)
#
#     # calculate WMD distance
#         input_list = []
#         for i in appdf_sub['cleanblurb']:
#             distance = emb_model.wmdistance(clean_input, i)
#             input_list.append(distance)
#
#     # add input_veclist to df
#         appdf_sub['distance'] = input_list
#
#     # sort dataframe in ascending order by distance
#         appdf_sub.sort_values(by=['distance'])
#
#     # return url for top 3 rows
#         for i in appdf_sub['state']:
#             if i == 'successful':
#                 return print(appdf_sub['projecturls'].head(3))
    # return


# Define a function that strips all punctuation and stop words
# def stripper(my_str):
#     str_low = my_str.lower()
#     allpunc = string.punctuation
#     pattern = r"[{}]".format(allpunc) # create the pattern
#     cleanstr = re.sub(pattern, " ", str_low)
#     tokenword = word_tokenize(cleanstr)
#     cleanstr = [word for word in tokenword if word not in nltk.corpus.stopwords.words('english')]
#     return cleanstr
