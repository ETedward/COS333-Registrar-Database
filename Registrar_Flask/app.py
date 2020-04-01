#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Bharat and Edward
#-----------------------------------------------------------------------

from sys import argv
#from database import Database
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    Dept = request.args.get('Dept')
    Numb = request.args.get('Numb')
    Area = request.args.get('Area')
    Title = request.args.get('Title')

    html = render_template('index.html',
                           Dept=Dept,
                           Numb=Numb,
                           Area=Area,
                           Title=Title)
    response = make_response(html)
    return response
    
#---------------------------------------------------
if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
