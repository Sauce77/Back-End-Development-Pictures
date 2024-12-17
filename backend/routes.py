from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """muestra todas las imagenes"""
    if data:
        resp = make_response(jsonify(data))
        resp.status_code = 200
        return resp
    
    return {"Message":"Data not available"}, 500


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:

        for picture in data:
            if id == picture['id']:
                resp = make_response(jsonify(picture))
                resp.status_code = 200
                return resp
        
    return {"Message": "Picture not found!"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    
    if request:
        picture_add = request.get_json()
        
        for picture in data:
            if picture_add['id'] == picture['id']:
                return {"Message": f"picture with id {picture['id']} already present"}, 302

        data.append(picture_add)
        resp = make_response(jsonify(picture_add))
        resp.status_code = 201
        return resp

    return {"Message": "Server problem"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    
    if data:

        for index,picture in enumerate(data):
            if picture['id'] == id:
                data[index] = request.get_json()
                return {"Message": f"Picture with id:{id} updated!"}, 200
        
    return {"Message": "Picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if data:

        for index,picture in enumerate(data):

            if picture['id'] == id:
                data.pop(index)
                return {"Message": f"Picture with id:{id} deleted!"}, 204
    
    return {"Message": f"Picture not found"}, 404
