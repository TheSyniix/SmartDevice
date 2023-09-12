import bottle
import mysql.connector as connector
import bottle_mysql
from bottle import route, run
from bottle import error
from bottle import response
from bottle import template
from bottle import request
import json

app = bottle.Bottle()
# enter your server IP address/domain name
HOST = "x.x.x.x" # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "database"
# this is the user you create
USER = "python-user"
# user password
PASSWORD = "Password1$"
# connect to MySQL server
db_connection = connector.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
print("Connected to:", db_connection.get_server_info())
# enter your code here!

mycursor = db_connection.cursor

def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

@route('/insert')
@enable_cors
def insert():
    data = request.get_json()
    one = data['one']
    two = data['two']
    sql = "INSERT INTO xxxx (xxxx, xxxx) VALUES('{}', '{}');".format(one, two)
    mycursor.execute(sql)