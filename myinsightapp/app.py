from flask import Flask, request, flash, render_template
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, HiddenField
import pandas as pd
import sim_tool as st


app = Flask(__name__)
# app.config.from_object('yourapplication.default_settings')
# app.config.from_envvar('YOURAPPLICATION_SETTINGS')

# Home Page
@app.route('/', methods=['GET', 'POST'])
def index():
    categories = ['Art/Visual Art/Photography', 'Books/Zine/Print', 'Crafts/Textiles', 'Design/Architecture', 'Equipment/Tools/DIY', 'Fashion/Apparel', 'Food/Beverage', 'Games/Gaming', 'Media', 'Music', 'Performance Art', 'Spaces/Places/Events', 'Tech/Web', 'TV/Film/Webseries', 'Other']
    return render_template("home.html", categories=categories)


@app.route('/pitchidea', methods=['POST'])
def ideavetter():
    if request.method == 'POST':
        selection = request.form['selection']

        for aKey in request.form:
            if aKey == 'pitch':
                text = request.form[aKey]
        # text = request.form('pitch')
        print(request.form['pitch'])
        print(text)

        if selection == 'Art/Visual Art/Photography':
            df = pd.read_pickle('df_art.pkl')
        elif selection == 'Books/Zine/Print':
            df = pd.read_pickle('df_book.pkl')
        elif selection == 'Crafts/Textiles':
            df = pd.read_pickle('df_craft.pkl')
        elif selection == 'Design/Architecture':
            df = pd.read_pickle('df_design.pkl')
        elif selection == 'Equipment/Tools/DIY':
            df = pd.read_pickle('df_diy.pkl')
        elif selection == 'Fashion/Apparel':
            df = pd.read_pickle('df_fashion.pkl')
        elif selection == 'Food/Beverage':
            df = pd.read_pickle('df_food.pkl')
        elif selection == 'Games/Gaming':
            df = pd.read_pickle('df_games.pkl')
        elif selection == 'Media':
            df = pd.read_pickle('df_media.pkl')
        elif selection == 'Music':
            df = pd.read_pickle('df_music.pkl')
        elif selection == 'Performance Art':
            df = pd.read_pickle('df_perform.pkl')
        elif selection == 'Spaces/Places/Events':
            df = pd.read_pickle('df_events.pkl')
        elif selection == 'Tech/Web':
            df = pd.read_pickle('df_tech.pkl')
        elif selection == 'TV/Film/Webseries':
            df = pd.read_pickle('df_film.pkl')
        else:
            df = pd.read_pickle('df_other.pkl')


        # df = st.load_data()
        emb_model = st.load_model()


    # clean and tokenize user input
        clean_input = st.stripper(text)

    # get vectors for input text
#     input_vecs = get_vectors(clean_input)

    # calculate WMD distance
        df['distance'] = 0
        for n in range(len(df)):
            distance = emb_model.wmdistance(clean_input, df.loc[n,'stripblurb'])
            df.loc[n,'distance'] = distance
        # input_list = []
        # for i in df['stripblurb']:
        #     distance = emb_model.wmdistance(clean_input, i)
        #     input_list.append(distance)


    # add input_veclist to df
        # df['distance'] = input_list

    # sort dataframe in ascending order by distance
        df.sort_values(by=['distance'])

    # return url for top 3 rows
        for i in df['state']:
            if i == 'successful':
                output_url1 = df.loc[0,'urls.web.project']
                output_url2 = df.loc[1,'urls.web.project']
                output_url3 = df.loc[2,'urls.web.project']
                name1 = df.loc[0,'name']
                name2 = df.loc[1,'name']
                name3 = df.loc[2,'name']
                backers1 = df.loc[0, 'backers_count']
                backers2 = df.loc[1, 'backers_count']
                backers3 = df.loc[2, 'backers_count']
                pledged1 = int(df.loc[0, 'pledged'])
                pledged2 = int(df.loc[1, 'pledged'])
                pledged3 = int(df.loc[2, 'pledged'])

    # return print(results)
    return render_template("output.html", output_url1=output_url1, output_url2=output_url2, output_url3=output_url3, name1=name1, name2=name2, name3=name3, backers1=backers1, backers2=backers2, backers3=backers3, pledged1=pledged1, pledged2=pledged2, pledged3=pledged3)



if __name__ == '__main__':
    app.run(debug=True)
