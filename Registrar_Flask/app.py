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
                           output = output,
                           input = input)
    response = make_response(html)
    return response

@app.route('/', methods=['GET'])
def index():
    dept = coursenum = area = title = ''
    if request.cookies.get('prevDept'):
        dept = request.cookies.get('prevDept')
    if request.cookies.get('pCourseNum'):
        coursenum = request.cookies.get('pCourseNum')
    if request.cookies.get('prevArea'):
        area = request.cookies.get('prevArea')
    if request.cookies.get('prevTitle'):
        title = request.cookies.get('prevTitle')

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
    print(args)
    result = regserver.managedb(args)

    html = render_template('index.html',
                           dept=dept,
                           coursenum=coursenum,
                           area=area,
                           title=title,
                           result=result)
    response = make_response(html)

    if request.args.get('dept'):
        response.set_cookie('prevDept', value=dept)
    else:
        response.set_cookie('prevDept', max_age=0)
    if request.args.get('coursenum'):
        response.set_cookie('pCourseNum', value=coursenum)
    else:
        response.set_cookie('pCourseNum', max_age=0)
    if request.args.get('area'):
        response.set_cookie('prevArea', value=area)
    else:
        response.set_cookie('prevArea', max_age=0)
    if request.args.get('title'):
        response.set_cookie('prevTitle', value=title)
    else:
        response.set_cookie('prevTitle', max_age=0)

    return response

# ---------------------------------------------------


if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
