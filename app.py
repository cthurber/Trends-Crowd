import json,requests,os
from flask import Flask, render_template, request
from acquire import saveFeed
from forms import Acquire_Feed_Form

app = Flask(__name__)

def add_feed(page_url,schedule="./schedule.csv"):

    with open(schedule,'r') as sch:
        queue = [line.replace('\n','') for line in sch]

    if(page_url not in queue):

        with open(schedule,'a') as sch:
            print(page_url,file=sch)

    return True

@app.route('/', methods = ['GET', 'POST'])
def home():
    form = Acquire_Feed_Form(request.form)
    if request.method == 'POST':
        turl = form.trends_url.data
        add_feed(turl)
        return render_template('confirmation.html', form=form)
    else:
        return render_template('index.html', form=form)

@app.route('/data')
def data():
    output_path = "./data/"
    feeds = {}
    for feed in os.listdir(output_path):
        feeds[feed.replace('.csv','')] = os.path.abspath(output_path + feed)
    return render_template('data.html', feeds=feeds)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
