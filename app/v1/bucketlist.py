from flask import jsonify, request, abort
import json
from app import app
from app.v1.models import Users
from sqlalchemy.exc import IntegrityError
from app import databases


@app.route('/bucketlist/api/v1/register', methods=['POST'])
def register():
    request.get_json(force=True)
    uname = request.json['username']
    passwd = request.json['password']
    userInfo = Users(username=uname, password_hash=passwd)
    userInfo.save()
    response = jsonify({'Registration status': 'Successfully registered ' + userInfo.username})
    response.status_code = 201
    return response


@app.route('/bucketlist/api/v1/register', methods=['GET'])
def get_user():
    results = []
    res = Users.query.all()
    for r in res:
        data = {
            'id': r.id,
            'username': r.username,
            'password': r.password_hash
        }
        results.append(data)
    response = jsonify({'Success': results})
    response.status_code = 200
    return response
