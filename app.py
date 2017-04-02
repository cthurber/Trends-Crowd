import json,requests,os
from flask import Flask, render_template, request, make_response
from acquire import saveFeed
from forms import Acquire_Feed_Form, Download_CSV

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
        feeds[feed.replace('.csv','')] = output_path + feed # os.path.abspath(output_path + feed)
    return render_template('data.html', feeds=feeds)

@app.route('/download', methods = ['GET', 'POST'])
def download():

    form = Download_CSV(request.form)
    if request.method == 'POST':
        csv = form.csv_file.data
        csv_string = ""
        with open(csv, 'r') as c:
            for line in c:
                csv_string += line
        fname = form.csv_name.data
        response = make_response(csv_string)
        cd = 'attachment; filename='+str(fname)+'.csv'
        response.headers['Content-Disposition'] = cd
        response.mimetype='text/csv'

        return response

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
