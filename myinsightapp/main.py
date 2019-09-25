from flask import Flask, request, flash, render_template
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, HiddenField

app = Flask(__name__)
app.config.from_object('yourapplication.default_settings')
app.config.from_envvar('YOURAPPLICATION_SETTINGS')


@app.route('/', methods=['GET', 'POST'])
def ideaform():
    idea = TextField('Please describe your idea:')
    submit = SubmitField('Submit')
    if request.method == 'POST':
        inputtext = request.form['Describe your idea here']
        processed_idea = inputtext.upper()
        return processed_idea
        print(processed_idea)
    else:
        return render_template("home.html")
        # if form.validate():
        #     flash(idea)
        # else:
        #     flash('Idea description is required. ')
        # return render_template("home.html", form = inputtext)


if __name__ == '__main__':
    app.run(debug=True)
