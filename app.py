from flask import *
import sqlite3
import json

class Phonebook():
    def postNumber( socket, data ):
        number = data['number']
        name = data['name']

        cursor = socket.cursor()
        cursor.execute( "INSERT INTO phones(phone, name) VALUES (?, ?)", (number, name))
        socket.commit()
        pass

    def search( socket, query ):
        cursor = socket.cursor()
        cursor.execute( "SELECT * FROM phones WHERE name LIKE ?", ['%' + query + r'%'])
        return cursor.fetchall()
        pass

    def removeItem( socket, id ):
        cursor = socket.cursor()
        cursor.execute( "DELETE FROM phones WHERE id = ?", [id])
        socket.commit()
        pass
        

app = Flask(__name__)
@app.route("/api/v1/search", methods=['POST'])
def search():
    socket = sqlite3.connect("phonebook.db")

    payload = request.get_json()
    return json.dumps(Phonebook.search( socket, payload['query'] ))
    pass

@app.route("/api/v1/number/<id>", methods=['DELETE'])
def remove( id ):
    socket = sqlite3.connect("phonebook.db")

    Phonebook.removeItem( socket, id )

    return json.dumps({'code': 200, 'error': False})
    pass

@app.route("/api/v1/number/post", methods=['POST'])
def post():
    socket = sqlite3.connect("phonebook.db")

    payload = request.get_json()
    Phonebook.postNumber( socket, payload )

    return json.dumps({'code': 200, 'error': False})
    pass

# LOADING STATICS FILES
@app.route('/<path:path>')
def assets( path ):
    return send_from_directory('static', path)
    pass

@app.route("/")
def index():
    return render_template('index.html')
    pass

if __name__ == '__main__':
    ################################################################################
    # This file is the worker file, there is the source-code. It will start the    #
    # listen the connection from the clients and it will send a payload back to    #
    # the client.                                                                  #
    ################################################################################
    app.run()
