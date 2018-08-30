# coding:utf-8
from . import api
from ..models import User,Bucketlist
from flask import request, jsonify, abort, make_response

@api.route('/bucketlists/', methods=['POST', 'GET'])
def bucketlists():
    # get the access token
    access_token = request.headers.get('Authorization')

    if access_token:
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
            # Go ahead and handle the request, the user is authed
            if request.method == "POST":
                name = str(request.data.get('name', ''))
                if name:
                    bucketlist = Bucketlist(name=name, created_by=user_id)
                    bucketlist.save()
                    response = jsonify({
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'created_by': user_id
                    })

                    return make_response(response), 201

            else:
                # GET
                # get all the bucketlists for this user
                bucketlists = Bucketlist.get_all(user_id)
                results = []

                for bucketlist in bucketlists:
                    obj = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'created_by': bucketlist.created_by
                    }
                    results.append(obj)

                return make_response(jsonify(results)), 200
        else:
            # user is not legit, so the payload is an error message
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401


@api.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def bucketlist_manipulation(id, **kwargs):

    access_token = request.headers.get('Authorization')

    if access_token:
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
            bucketlist = Bucketlist.query.filter_by(id=id).first()
            if not bucketlist:
                # Raise an HTTPException with a 404 not found status code
                abort(404)

            if request.method == "DELETE":
                bucketlist.delete()
                return {
                    "message": "bucketlist {} deleted".format(bucketlist.id)
                }, 200
            elif request.method == 'PUT':
                name = str(request.data.get('name', ''))
                bucketlist.name = name
                bucketlist.save()
                response = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified,
                    'created_by': bucketlist.created_by
                }
                return make_response(jsonify(response)), 200
            else:
                # GET
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified,
                    'created_by': bucketlist.created_by
                })
                return make_response(response), 200
        else:
            # user is not legit, so the payload is an error message
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401
