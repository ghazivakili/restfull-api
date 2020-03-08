#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

dbhost = '127.0.0.1'
dbuser = 'root'
dbpass = ''
dbname = 'lanzi'

db_connect = create_engine('mysql+pymysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' + dbname, pool_recycle=3600)
app = Flask(__name__)
api = Api(app)


class Value(Resource):
    # Example http://127.0.0.1:5000/value/<boardid>/<sensorid>/value
    # INSERT INTO `measur` (`id`, `sensor_id`, `board_id`, `value`) VALUES (NULL, '1', '2', '100');
    def get(self, board_id,sensor_id,value):
        conn = db_connect.connect()
        #strs = "SELECT senderID,PacketType,timestamp FROM incoming WHERE senderID={} AND(PacketType=6 OR PacketType=76) AND timestamp LIKE '{}%%'".format(
        #    senderID, day)
        strs = "INSERT INTO measur (id, sensor_id, board_id, value) VALUES (NULL, '{}', '{}', '{}')".format(
            board_id,sensor_id,value)
        query = conn.execute(strs)
        # result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        result ={'respond':True}
        return jsonify(result)


class Read(Resource):
    # Example http://127.0.0.1:5000/read/1/1
    def get(self,  board_id,sensor_id):
        conn = db_connect.connect()
        queryStrs = "SELECT value FROM measur WHERE (sensor_id={} AND board_id={})  ORDER BY id ASC".format(
            board_id,sensor_id)
        query = conn.execute(queryStrs)
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Read, '/read/<board_id>/<sensor_id>')
# Example http://127.0.0.1:5000/value/<boardid>/<sensorid>/value
api.add_resource(Value, '/value/<board_id>/<sensor_id>/<value>')

if __name__ == '__main__':
    app.run()
