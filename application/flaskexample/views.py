from flask import Flask, request, flash, render_template
from flaskexample import app
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, HiddenField
import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
import csv
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

categories = ['Art/Visual Art/Photography', 'Books/Zine/Print', 'Crafts/Textiles', 'Design/Architecture', 'Equipment/Tools/DIY', 'Fashion/Apparel', 'Food/Beverage', 'Games/Gaming', 'Media', 'Music', 'Performance Art', 'Spaces/Places/Events', 'Tech/Web', 'TV/Film/Webseries', 'Other']

df2art = pd.read_pickle('flaskexample/df2art_vec.pkl')
df2book = pd.read_pickle('flaskexample/df2book_vec.pkl')
df2craft = pd.read_pickle('flaskexample/df2craft_vec.pkl')
df2design = pd.read_pickle('flaskexample/df2design_vec.pkl')
df2diy = pd.read_pickle('flaskexample/df2diy_vec.pkl')
df2fashion = pd.read_pickle('flaskexample/df2fashion_vec.pkl')
df2food = pd.read_pickle('flaskexample/df2food_vec.pkl')
df2games = pd.read_pickle('flaskexample/df2games_vec.pkl')
df2media = pd.read_pickle('flaskexample/df2media_vec.pkl')
df2music = pd.read_pickle('flaskexample/df2music_vec.pkl')
df2perform = pd.read_pickle('flaskexample/df2perform_vec.pkl')
df2events = pd.read_pickle('flaskexample/df2events_vec.pkl')
df2tech = pd.read_pickle('flaskexample/df2tech_vec.pkl')
df2film = pd.read_pickle('flaskexample/df2film_vec.pkl')
df2other = pd.read_pickle('flaskexample/df2other_vec.pkl')

# df2slim = pd.read_pickle('flaskexample/df2slim_vec.pkl')
# df2dict = {'Art/Visual Art/Photography': df_art}
# df2dict['Art/Visual Art/Photography']

norm_model = KeyedVectors.load_word2vec_format('flaskexample/GoogleNews-vectors-negative300-SLIM.bin', binary=True)
norm_model.init_sims(replace=True)

def cleaner(my_str):
    str_low = my_str.lower()
    remove = string.punctuation
    remove = remove.replace(".", " ").replace(",", " ").replace("'", " ")
    pattern = r"[{}]".format(remove) # create the pattern
    cleanstr = re.sub(pattern, " ", str_low)
    finalword = word_tokenize(cleanstr)
    return finalword

def get_vectors_norm(listcol):
    nvectors = []
    for word in listcol:
        try:
            nvector = norm_model[word]
            nvectors.append(nvector)
        except KeyError:
            pass
    if len(nvectors)==0:
        return np.zeros(300)
    else:
        return sum(nvectors)/len(nvectors)

def cos_wrapper(vec1, vec2):
    try:
        return cosine(vec1, vec2)
    except:
        return -1


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    # global categories
    return render_template("home.html", categories=categories)


@app.route('/pitchidea', methods=['POST'])
def ideavetter():
    global df2art
    global df2book
    global df2craft
    global df2design
    global df2diy
    global df2fashion
    global df2food
    global df2games
    global df2media
    global df2music
    global df2perform
    global df2events
    global df2tech
    global df2film
    global df2other
    global norm_model


    if request.method == 'POST':
        selection = request.form['selection']

        for aKey in request.form:
            if aKey == 'pitch':
                text = request.form[aKey]

        print(request.form['pitch'])
        print(text)
        #df = df_dict[selection]

        if selection == 'Art/Visual Art/Photography':
            df = df2art
        elif selection == 'Books/Zine/Print':
            df = df2book
        elif selection == 'Crafts/Textiles':
            df = df2craft
        elif selection == 'Design/Architecture':
            df = df2design
        elif selection == 'Equipment/Tools/DIY':
            df = df2diy
        elif selection == 'Fashion/Apparel':
            df = df2fashion
        elif selection == 'Food/Beverage':
            df = df2food
        elif selection == 'Games/Gaming':
            df = df2games
        elif selection == 'Media':
            df = df2media
        elif selection == 'Music':
            df = df2music
        elif selection == 'Performance Art':
            df = df2perform
        elif selection == 'Spaces/Places/Events':
            df = df2events
        elif selection == 'Tech/Web':
            df = df2tech
        elif selection == 'TV/Film/Webseries':
            df = df2film
        else:
            df = df2other

        # print(df['newcat'].head(1))
        # df = df2slim

        # clean and tokenize user input
        clean_input = cleaner(text)
        print(clean_input)

        # apply vectors to clean_input
        input_vec = get_vectors_norm(clean_input)

        # calculate cosine similarity score
        df['cos_sim'] = df['nvectors'].apply(lambda x: cos_wrapper(input_vec, x))


        # sort dataframe in ascending order by distance
        # df[['cos_sim']].to_csv('before_sort.csv')
        df.sort_values(by=['cos_sim'], ascending = True, inplace = True)
        # df[['cos_sim']].to_csv('after_sort.csv')
        df_results = df[df['state'] == 'successful'].head(3)
        print(df['cos_sim'].head(3))
        df_results = df_results.reset_index(drop=True)
        print(df['cos_sim'].head(3))

        # return url for top 6 rows
        output_url1 = df_results.at[0,'urls.web.project']
        output_url2 = df_results.at[1,'urls.web.project']
        output_url3 = df_results.at[2,'urls.web.project']
        # output_url1 = df_results.at[3,'urls.web.project']
        # output_url2 = df_results.at[4,'urls.web.project']
        # output_url3 = df_results.at[5,'urls.web.project']
        name1 = df_results.at[0,'name']
        name2 = df_results.at[1,'name']
        name3 = df_results.at[2,'name']
        # name1 = df_results.at[3,'name']
        # name2 = df_results.at[4,'name']
        # name3 = df_results.at[5,'name']
        backers1 = df_results.at[0, 'backers_count']
        backers2 = df_results.at[1, 'backers_count']
        backers3 = df_results.at[2, 'backers_count']
        # backers1 = df_results.at[3, 'backers_count']
        # backers2 = df_results.at[4, 'backers_count']
        # backers3 = df_results.at[5, 'backers_count']
        pledged1 = int(df_results.at[0, 'pledged'])
        pledged2 = int(df_results.at[1, 'pledged'])
        pledged3 = int(df_results.at[2, 'pledged'])
        # pledged1 = int(df_results.at[3, 'pledged'])
        # pledged2 = int(df_results.at[4, 'pledged'])
        # pledged3 = int(df_results.at[5, 'pledged'])

    # return print(results)
    return render_template("output.html", categories=categories, output_url1=output_url1, output_url2=output_url2, output_url3=output_url3, name1=name1, name2=name2, name3=name3, backers1=backers1, backers2=backers2, backers3=backers3, pledged1=pledged1, pledged2=pledged2, pledged3=pledged3)



if __name__ == '__main__':
    app.run(debug=True)
