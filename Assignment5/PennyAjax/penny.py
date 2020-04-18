#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import argv
from database import Database
from flask import Flask, request, make_response, render_template

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')
   
#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/search', methods=['GET'])
def search():
    
    html = render_template('search.html')
    response = make_response(html)
    return response
    
#-----------------------------------------------------------------------

@app.route('/searchresults', methods=['GET'])
def searchResults():
    
    author = request.args.get('author')
    if (author is None) or (author.strip() == ''):
        return ''

    database = Database()
    database.connect()
    books = database.search(author)
    database.disconnect()
    
    html = ''
    for book in books:
        html += '<strong>' + book.getAuthor() + ': </strong>' + \
            book.getTitle() + ' ($' + str(book.getPrice()) + ')<br>'

    response = make_response(html)
    return response
    
#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
