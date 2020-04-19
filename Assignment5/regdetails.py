#!/usr/bin/env python

# -----------------------------------------------------------------------
# regdetails.py
# Author: Edward and Bharat
# -----------------------------------------------------------------------

from os import path
from sys import argv, stderr, exit
from sqlite3 import connect


def errorcheck(argv):
    if len(argv) < 2:
        raise NameError
    if len(argv) < 3 and argv[1] == '-h':
        raise NameError

    if argv[1] == '-h':
        if len(argv) > 3:
            raise SyntaxError
        if not isinstance(int(argv[2]), int):
            raise ValueError
    elif len(argv) > 2:
        raise SyntaxError
    elif not isinstance(int(argv[1]), int):
        raise ValueError


def selectStr1():
    # Create a prepared statement and substitute values.
    stmtStr = 'Select ' +\
        'c.courseid,c.days,c.starttime,c.endtime,c.bldg,c.roomnum,' +\
        'cl.courseid,cl.dept,cl.coursenum, ' +\
        'cr.area,cr.title, cr.descrip,cr.prereqs,cr.courseid ' +\
        'FROM classes c, crosslistings cl, courses cr ' +\
        'WHERE c.courseid = cr.courseid ' +\
        'AND c.courseid = cl.courseid ' +\
        'AND c.classid = ?' +\
        'ORDER BY dept '
    return stmtStr


def selectStr2():
    # Create a prepared statement and substitute values.
    stmtStr = 'Select ' +\
        'c.courseid,' +\
        'p.profid, p.profname '+\
        'FROM classes c, coursesprofs cp, profs p ' +\
        'WHERE c.courseid = cp.courseid ' +\
        'AND cp.profid = p.profid ' +\
        'AND c.classid = ?' +\
        'ORDER BY profname'

    return stmtStr


def outputStr(row, finalStr):
    output = ''
    if len(row) == 2:
        finalStr += 'Dept and Number: ' + str(row[0]) + ' ' + \
                 str(row[1]) + '\n'
    elif len(row) == 4:
        finalStr += ('Area: ' + str(row[0]) + '\n')
        title = 'Title: ' + str(row[1])
        finalStr += (title + '\n\n')
        desc = 'Description: ' + str(row[2])
        finalStr += (desc + '\n\n')
        prereq = 'Prerequisites: ' + str(row[3])
        finalStr += (prereq + '\n\n')
        return finalStr
    else:
        finalStr += 'Course Id: ' + str(row[0]) + '\n' + \
                 'Days: ' + str(row[1]) + '\n' + \
                 'Start time: ' + str(row[2]) + '\n' + \
                 'End time: ' + str(row[3]) + '\n' + \
                 'Building: ' + str(row[4]) + '\n' + \
                 'Room: ' + str(row[5] + '\n')
    return finalStr


def stdStr(row):
    if len(row) == 2:
        output = str(row[0]) + ' ' + \
                 str(row[1])
    elif len(row) == 4:
        output = str(row[0]) + '\n' + \
                 str(row[1]) + '\n' + \
                 str(row[2]) + '\n' + \
                 str(row[3])
    else:
        output = str(row[0]) + '\n' + \
                 str(row[1]) + '\n' + \
                 str(row[2]) + '\n' + \
                 str(row[3]) + '\n' + \
                 str(row[4]) + '\n' + \
                 str(row[5])

def runDetails(argv):
    DATABASE_NAME = 'reg.sqlite'
    finalStr = ''
    if not path.isfile(DATABASE_NAME):
        raise LookupError

    # try:
    errorcheck(argv)
    # except NameError:
    #     print('regdetails: missing classid')
    #     exit(1)
    # except SyntaxError:
    #     print('regdetails: too many arguments')
    #     exit(1)
    # except ValueError:
    #     print('regdetails: classid is not an integer')
    #     exit(1)

    connection = connect(DATABASE_NAME)
    cursor = connection.cursor()

    stmtStr = selectStr1()
    try:
        if argv[1] == '-h':
            values = argv[2]
            cursor.execute(stmtStr, [values])
        else:
            values = argv[1]
            cursor.execute(stmtStr, [values])
    except Exception as e:
        print(e)
        raise NameError

    row = cursor.fetchone()

    try:
        if argv[1] == '-h':
            finalStr = outputStr(row, finalStr)
        else:
            stdStr(row)
    except TypeError:
        print('regdetails: classid does not exist')
        exit(1)

    while row is not None:
        if argv[1] == '-h':
            finalStr = outputStr(row[7:9], finalStr)
        else:
            stdStr(row[7:9])
        row2 = row
        row = cursor.fetchone()

    if argv[1] == '-h':
        finalStr = outputStr(row2[9:13], finalStr)
    else:
        stdStr(row2[9:13])

    stmtStr = selectStr2()
    cursor.execute(stmtStr, [values])

    row = cursor.fetchone()
    while row is not None:
        if argv[1] == '-h':
            finalStr += ('Professor: ' + row[2] + '\n')
        else:
            print(row[2])
        row = cursor.fetchone()
    cursor.close()
    connection.close()
    return finalStr

