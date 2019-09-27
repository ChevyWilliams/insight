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
    return render_template("home.html")

@app.route('/pitchidea', methods=['POST'])
def ideavetter():
    if request.method == 'POST':
        for aKey in request.form:
            if aKey == 'pitch':
                text = request.form[aKey]
        # text = request.form('pitch')
        print(request.form['pitch'])
        print(text)

        appdf_sub, emb_model = st.load_data()
    # accept user input
        # text = input("Pitch your idea here: ")

    # clean and tokenize user input
        clean_input = st.clean_text(text)

    # get vectors for input text
#     input_vecs = get_vectors(clean_input)

    # calculate WMD distance
        input_list = []
        for i in appdf_sub['cleanblurb']:
            distance = emb_model.wmdistance(clean_input, i)
            input_list.append(distance)

    # add input_veclist to df
        appdf_sub['distance'] = input_list

    # sort dataframe in ascending order by distance
        appdf_sub.sort_values(by=['distance'])

    # return url for top 3 rows
        for i in appdf_sub['state']:
            if i == 'successful':
                results = appdf_sub['projecturls'].head(3)

    # return print(results)
    return render_template("output.html", results=results)
        # if form.validate():
        #     flash(idea)
        # else:
        #     flash('Idea description is required. ')
        # return render_template("home.html", form = inputtext)


if __name__ == '__main__':
    app.run(debug=True)
