#!/usr/bin/python
import psycopg2
from configparser import ConfigParser
from sys import argv, stderr, exit
import entryInfo
import googlemaps
from datetime import datetime
import requests

# gmaps = googlemaps.Client(key='AIzaSyDQe5G3tqd5Vfwefn7w3Djrv1L1bmlKkTw')

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


# returns latitude and longitude of a given address
def geocode(address):
    try:
        url = ('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'
            .format(address.replace(' ','+'), 'AIzaSyDQe5G3tqd5Vfwefn7w3Djrv1L1bmlKkTw'))

        response = requests.get(url)
        resp_json_payload = response.json()
        lat = resp_json_payload['results'][0]['geometry']['location']['lat']
        lng = resp_json_payload['results'][0]['geometry']['location']['lng']
        return lat, lng
    except Exception as e:
        print(e)



# inserts userEntry into database
# entryInfo is an entryInfo object
def insertEntry(entryInfo):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        insertUser = """INSERT INTO userInformation (netid, name, phone, email, description, address)
               VALUES(%s, %s, %s, %s, %s, %s)"""

        insertCoordinates = """INSERT INTO coordinates (netid, address, latitude, longitude)
               VALUES(%s, %s, %s, %s)"""
        # execute a statement
        name = entryInfo.getName()
        netid = entryInfo.getNetid()
        phone = entryInfo.getPhone()
        email = entryInfo.getEmail()
        address = entryInfo.getAddress()
        description = entryInfo.getDescription()

        cur.execute(insertUser, (netid, name, phone, email, description, address))

        print('before')
        coordinates = geocode(address)
        print('after')

        latitude = float(coordinates[0])
        longitude = float(coordinates[1])

        print(latitude)
        print(longitude)

        cur.execute(insertCoordinates, (netid, address, latitude, longitude))


        conn.commit()
        print('success')
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

# based on fields of entry, returns a list of all rows in database containing these fields
# in which each row is a userInfo object
# entry is a entryInfo object
def searchEntry(entry):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql = """
            SELECT *
            FROM userInformation
            WHERE userInformation.netid LIKE %s AND
            userInformation.name LIKE %s AND
            userInformation.email LIKE %s AND
            userInformation.phone LIKE %s AND
            userInformation.description LIKE %s AND
            userInformation.address LIKE %s;
        """


        # execute a statement
        name = entry.retName()
        netid = entry.retNetid()
        phone = entry.retPhone()
        email = entry.retEmail()
        address = entry.retAddress()
        description = entry.retDescription()


        cur.execute(sql, (netid, name, email, phone, description, address))
        row = cur.fetchone()

        entries = []
        while row is not None:
            user = entryInfo.entryInfo()
            user.setNetid(str(row[0]))
            user.setName(str(row[1]))
            user.setEmail(str(row[2]))
            user.setPhone(str(row[3]))
            user.setDescription(str(row[4]))
            user.setAddress(str(row[5]))
            entries.append(user)
            row = cur.fetchone()

        print('success')
        # close the communication with the PostgreSQL
        cur.close()
        return entries

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


# prints all rows in userInformation table
def displayRows():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

   # execute a statement
        cur.execute('SELECT * from userInformation;')


        row = cur.fetchone()

        while row is not None:
            for item in row:
                print(item + " ", end=' ')
            print()
            row = cur.fetchone()

        cur.execute('SELECT * from coordinates;')

        print('--Coordinates--')
        row = cur.fetchone()

        while row is not None:
            for item in row:
                print(str(item) + " ", end=' ')
            print()
            row = cur.fetchone()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def main(argv):

    displayRows()

if __name__ == '__main__':
    main(argv)
