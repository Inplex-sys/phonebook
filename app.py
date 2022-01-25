################################################################################
#                          Copyrights and license                              #
################################################################################
#                                                                              #
# Copyright 2021 Inplex-sys <Inplex-sys@protonmail.ch>                         #
#                                                                              #
# This file is part of DarkUtilities.                                          #
#                                                                              #
# DarkUtilities is list of software: you can redistribute it and/or modify     #
# it under the terms of the GNU Lesser General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# DarkUtilities is distributed in the hope that it will be useful, but WITHOUT #
# ANY  WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License  #
# for more details.                                                            #
#                                                                              #
# You should DarkUtilities received a copy of the GNU Lesser General Public    #
# License.                                                                     #
# along with DarkUtilities. If not, see <http://www.gnu.org/licenses/>.        #
#                                                                              #
################################################################################
#                     Made with ❤️ by github.com/Inplex-sys                    #
################################################################################

from flask import *
import sqlite3
import json

class Phonebook():
    def postNumber( socket, data ):
        number = data['number']
        name = data['name']

        cursor = socket.cursor()
        cursor.execute( "INSERT INTO phones(phone, name) VALUES (%(number)s, %(name)s)", {number: number, name: name})
        socket.commit()
        pass

    def search( socket, query ):
        cursor = socket.cursor()
        cursor.execute( "SELECT * FROM phones WHERE name LIKE '%(query)s'", {query: '%' + query + '%'})
        return cursor.fetchall()
        pass
        

app = Flask(__name__)
@app.route("/api/v1/search", methods=['POST'])
def search():
    socket = sqlite3.connect("phonebook.db")

    payload = request.get_json()
    return json.dumps(Phonebook.search( socket, payload['query'] ))
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