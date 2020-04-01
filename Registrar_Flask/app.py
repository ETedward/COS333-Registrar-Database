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
    index = url.find('=')
    classid = url[index + 1:]
    idlist = ["regdetails","-h", classid]
    output = regdetails.runDetails(idlist)

    print("THIS IS OUTPUT:")
    print(output)
    input = output.splitlines()
    print("THIS IS INPUT:")

    html = render_template('indexreg.html',
                           classid = classid,
                           output = output,
                           input1 = input[0:6],
                           input2 = input[6:])
    response = make_response(html)
    return response

@app.route('/', methods=['GET'])
def index():
    dept = request.args.get('dept')
    coursenum = request.args.get('coursenum')
    area = request.args.get('area')
    title = request.args.get('title')
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

    html = render_template('index.html',
                           dept=dept,
                           coursenum=coursenum,
                           area=area,
                           title=title,
                           result=result)

    response = make_response(html)
    if (dept is not None):
        response.set_cookie('prevDept', dept)
    if (coursenum is not None):
        response.set_cookie('pCoursenum', coursenum)
    if (area is not None):
        response.set_cookie('prevArea', area)
    if (title is not None):
        response.set_cookie('prevTitle', title)
    return response
    
# ---------------------------------------------------


if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
