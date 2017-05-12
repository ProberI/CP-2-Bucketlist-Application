from flask import jsonify, request, abort, make_response
import json
import re
from app import app
from app.v1.models import Users
from sqlalchemy.exc import IntegrityError
from app import databases
databases.create_all()


@app.route('/bucketlist/api/v1/register', methods=['POST'])
def register():
    request.get_json(force=True)
    uname = request.json['username']
    passwd = request.json['password']
    if not uname:
        response = jsonify({'error': 'Username cannot be blank'})
        return response
    elif not re.match("^[a-zA-Z0-9_]*$", uname):
        response = jsonify({'error': 'Username cannot contain special characters'})
        return response
    elif len(passwd) < 5:
        response = jsonify({'error': 'Password should be more than 5 characters'})
        return response
    else:
        res = Users.query.all()
        uname_check = [r.username for r in res]
        if uname in uname_check:
            response = jsonify({'error': 'This username is already in use'})
            return response
        else:
            userInfo = Users(username=uname, password_hash=passwd)
            userInfo.save()
            response = jsonify(
                {'Registration status': 'Successfully registered ' + userInfo.username})
            response.status_code = 201
            return response


@app.route('/bucketlist/api/v1/login', methods=['POST'])
def login():
    request.get_json(force=True)
    uname = request.json['username']
    passwd = request.json['password']
    res = Users.query.all()
    uname_check = [u.username for u in res if u.password_hash == passwd]
    if not uname:
        response = jsonify({'error': 'Username field cannot be blank'})
        response.status_code = 400
        return response
    elif not passwd:
        response = jsonify({'error': 'Password field cannot be blank'})
        response.status_code = 400
        return response

    elif not re.match("^[a-zA-Z0-9_]*$", uname):
        response = jsonify({'error': 'Username cannot contain special characters'})
        response.status_code = 400
        return response
    elif uname in uname_check:
        response = jsonify(
            {'Login status': 'Successfully Logged in '})
        response.status_code = 200
        return response
    else:
        response = jsonify(
            {'Login status': 'Invalid credentials'})
        response.status_code = 200
        return response
