#!/usr/bin/env python

# ---------------------------------------------------------------------
# penny.py
# Author: Bharat and Edward
# ---------------------------------------------------------------------
import regserver
import regdetails
from sys import argv
from database import Database
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template

# ---------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

# ---------------------------------------------------------------------

@app.route('/regdetails', methods=['GET'])
def handlereg():
    url = request.url

    prev_url = request.cookies.get('prevAddress')
    url_index = prev_url.find('?')
    redir_url = prev_url[url_index:]

    index = url.find('=')
    classid = url[index + 1:]

    idlist = ["regdetails","-h", classid]

    try:
        output = regdetails.runDetails(idlist)
        input = output.splitlines()

        html = render_template('indexreg.html',
                               classid=classid,
                               input1=input[0:6],
                               input2=input[6:],
                               redir_url=redir_url)
    except:
        if (not isinstance(classid, int)):
            html = render_template('missing.html', message="classid is not numeric")
        if (classid):
            html = render_template('missing.html', message="classid does not exist")
        else:
            html = render_template('missing.html', message="Missing class id")

    response = make_response(html)
    return response

@app.route('/', methods=['GET'])
def index():

    html = render_template('index.html')
    response = make_response(html)
    return response

# ---------------------------------------------------

@app.route('/regoverviews', methods=['GET'])
def overview():

    if request.args.get('dept'):
        dept = request.args.get('dept')
    else:
        dept = ''
    if request.args.get('coursenum'):
        coursenum = request.args.get('coursenum')
    else:
        coursenum = ''
    if request.args.get('area'):
        area = request.args.get('area')
    else:
        area = ''
    if request.args.get('title'):
        title = request.args.get('title')
    else:
        title = ''

    reg = 'reg'
    args = [reg]
    args.append("-h")
    if dept:
        args.append('-dept')
        args.append(dept)
    if coursenum:
        args.append('-coursenum')
        args.append(coursenum)
    if area:
        args.append('-area')
        args.append(area)
    if title:
        args.append('-title')
        args.append(title)
    result = regserver.managedb(args)


    html = render_template('result.html',
                           dept=dept,
                           coursenum=coursenum,
                           area=area,
                           title=title,
                           result=result)
    response = make_response(html)
    return response


# ---------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
