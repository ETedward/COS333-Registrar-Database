#!/usr/bin/env python

#-----------------------------------------------------------------------
# regserver
# Author: Edward Tian
#-----------------------------------------------------------------------
import regdetails

from os import path
from sys import argv, stderr, exit

from socket import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from pickle import dump
from pickle import load
from sqlite3 import connect


def buildStr(argv):
    dept = coursenum = area = title = loopskip = 0
    deptVal = coursenumVal = areaVal = titleVal = ''
    length = len(argv)
    for i in range(length):
        if loopskip or i == 0:
            loopskip = 0
            continue
        if argv[i] == '-h' and i == 1:
            continue
        if argv[i] == '-dept' and dept == 1:
            raise ValueError
        elif argv[i] == "-dept":
            dept = 1
            try:
                deptVal = argv[i + 1]
                loopskip = 1
                continue
            except:
                print('reg: missing value')
                exit(1)
        if argv[i] == '-coursenum' and coursenum == 1:
            raise ValueError
        elif argv[i] == "-coursenum":
            coursenum = 1
            try:
                coursenumVal = argv[i + 1]
                loopskip = 1
                continue
            except:
                print('reg: missing value')
                exit(1)
        if argv[i] == '-area' and area == 1:
            raise ValueError
        elif argv[i] == "-area":
            area = 1
            try:
                areaVal = argv[i + 1]
                loopskip = 1
                continue
            except:
                print('reg: missing value')
                exit(1)
        if argv[i] == '-title' and title == 1:
            raise ValueError
        elif argv[i] == "-title":
            title = 1
            try:
                titleVal = argv[i + 1]
                loopskip = 1
                continue
            except:
                print('reg: missing value')
                exit(1)
        raise SyntaxError

    return [dept, coursenum, area, title, deptVal, coursenumVal, areaVal, titleVal]


def selectStr(param):
    # Create a prepared statement and substitute values.
    stmtStr = 'SELECT classid, dept, coursenum, area, title ' + \
              'FROM crosslistings, classes, courses ' + \
              'WHERE classes.courseid = courses.courseid ' + \
              'AND classes.courseid = crosslistings.courseid '
    return stmtStr


def managedb(argv):
    DATABASE_NAME = 'reg.sqlite'
    sb = []

    if not path.isfile(DATABASE_NAME):
        raise Exception('reg: database reg.sqlite not found')

    try:
        param = buildStr(argv)

    except ValueError:
        print('reg: duplicate key')
        exit(1)
    except SyntaxError:
        print('reg: invalid key')
        exit(1)

    try:
        connection = connect(DATABASE_NAME)
        cursor = connection.cursor()
    except:
        print("reg: database reg.sqlite not found")

    try:
        stmtStr = selectStr(param)
    except:
        print("sqlite3.OperationalError: no such table: classes")

    values = []
    if param[0]:  # dept is true
        if '%' in param[4]:
            index = param[4].find('%')
            param[4] = param[4][:index] + '/' + param[4][index:]
        if '_' in param[4]:
            index = param[4].find('_')
            param[4] = param[4][:index] + '/' + param[4][index:]
        param[4] = "%" + param[4] + "%"
        stmtStr += "AND dept LIKE ? "
        values.append(param[4])

    if param[1]:  # coursenum is true
        if '%' in param[5]:
            index = param[5].find('%')
            param[5] = param[5][:index] + '/' + param[5][index:]
        if '_' in param[5]:
            index = param[5].find('_')
            param[5] = param[5][:index] + '/' + param[5][index:]
        param[5] = "%" + param[5] + "%"
        stmtStr += "AND coursenum LIKE ? "
        values.append(param[5])

    if param[2]:  # area is true
        if '%' in param[6]:
            index = param[6].find('%')
            param[6] = param[6][:index] + '/' + param[6][index:]
        if '_' in param[6]:
            index = param[6].find('_')
            param[6] = param[6][:index] + '/' + param[6][index:]
        param[6] = "%" + param[6] + "%"
        stmtStr += "AND area LIKE ? "
        values.append(param[6])

    if param[3]:  # title is true
        if '%' in param[7]:
            index = param[7].find('%')
            param[7] = param[7][:index] + '/' + param[7][index:]
        if '_' in param[7]:
            index = param[7].find('_')
            param[7] = param[7][:index] + '/' + param[7][index:]
        param[7] = "%" + param[7] + "%"
        stmtStr += "AND title LIKE ? "
        values.append(param[7])

    stmtStr += 'ORDER BY dept, coursenum, classid '

    cursor.execute(stmtStr, values)

    row = cursor.fetchone()
    while row is not None:
        output = stdStr(row)
        # if len(argv) > 1 and argv[1] == '-h' and len(output) > 100:
        #     concat = output.rfind(' ', 0, 68)
        #     output = output[0:concat]
        #     output = output + ' ... '

        sb.append(output)
        row = cursor.fetchone()

    cursor.close()
    connection.close()
    return sb

def stdStr(row):
    output = str(row[0]) + '  \t' + \
             str(row[1]) + '\t\t' + \
             str(row[2]) + '\t\t' + \
             str(row[3]) + '\t\t' + \
             str(row[4])
    return output


# -----------------------------------------------------------------------

def handleClientreg(allvars):

    finaloutput = managedb(allvars)
    return finaloutput

# -----------------------------------------------------------------------


def handleClientregdetails(allvars):

    finaloutput = regdetails.runDetails(allvars)
    return finaloutput

# -----------------------------------------------------------------------

def main(argv):
    BACKLOG = 5

    if len(argv) != 2:
        print('Usage: python %s port' % argv[0])
        exit(1)

    try:
        port = int(argv[1])

        serverSock = socket(AF_INET, SOCK_STREAM)
        print('Opened server socket')
        serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serverSock.bind(('', port))
        print('Bound server socket to port')
        serverSock.listen(BACKLOG)
        print('Listening')

        while True:
            try:
                sock, clientAddr = serverSock.accept()
                print('Accepted connection, opened socket')
                floread = sock.makefile(mode='rb')
                allvars = load(floread)
                if allvars[0] == 'reg.py':
                    print('Received command: getOverviews')
                    output = handleClientreg(allvars)
                elif allvars[0] == 'regdetails.py':
                    print('Received command: getDetails')
                    output = handleClientregdetails(allvars)
                else:
                    output = ''
                flowrite = sock.makefile(mode='wb')
                dump(output, flowrite)
                flowrite.flush()
                sock.close()
                print('Closed socket' + str(clientAddr))
            except Exception as e:
                print(e, file=stderr)
    except Exception as e:
        print(e, file=stderr)


# -----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)