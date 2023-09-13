import bottle
import mysql.connector as connector
from bottle import route, run
from bottle import error
from bottle import response
from bottle import template
from bottle import request
import json

app = bottle.Bottle()
# enter your server IP address/domain name
HOST = "34677.hosts1.ma-cloud.nl" # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "c8248smart"
# this is the user you create
USER = "c8248guest"
# user password
PASSWORD = "guestNumber"
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
    one = data['moisture']
    two = data['time']
    sql = "INSERT INTO smartDeviceData (moisture, time) VALUES('{}', '{}');".format(one, two)
    mycursor.execute(sql)

@route('/fetch')
@enable_cors
def fetch():
    sql = "SELECT * FROM smartDeviceData;"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if myresult:
        myresult = json.dumps(myresult)
        return myresult
    return error404

@route('/hello')
def hello():
    return "Hello World!"

@error(404)
def error404(error):
    return 'Nothing here, sorry'

run(host='localhost', port=8080, debug=True)