import json,requests
from flask import Flask, render_template, request
from acquire import saveFeed
from forms import Acquire_Feed_Form

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    form = Acquire_Feed_Form(request.form)
    if request.method == 'POST':

        turl = form.trends_url.data

        print(turl)
        saveFeed(turl)
        return render_template('confirmation.html', form=form)
    else:
        return render_template('index.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
