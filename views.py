"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

# from crypt import methods
import site

from pymongo import MongoClient 

from app import app, Config,  mongo, Mqtt
from flask import escape, render_template, request, jsonify, send_file, redirect, make_response, send_from_directory 
from json import dumps, loads 
from werkzeug.utils import secure_filename
from datetime import datetime,timedelta, timezone
from os import getcwd
from os.path import join, exists
from time import time, ctime
from math import floor
from app.functions import update_passcode, check_passcode, update_and_publish_data, get_data_between_timestamps, calculate_average_between_timestamps
from . import get_db
from bson.objectid import ObjectId
 



#####################################
#   Routing for your application    #
#####################################


# 1. CREATE ROUTE FOR '/api/set/combination'

@app.route('/api/set/combination', methods=['POST'])
def set_combination():
    # Get the passcode from the form data
    passcode = request.form['passcode']

    # Check if the passcode is a 4-digit integer
    if not passcode.isdigit() or len(passcode) != 4:
        return jsonify({'status': 'failed', 'data': 'Invalid passcode'}), 400

    # Get the database
    db = get_db()

    # Update the document in the 'code' collection
    result = db.code.find_one_and_update(
        {'_id': ObjectId('620137859')},  # ObjectId of the document
        {'$set': {'code': passcode}},  # Set the 'code' field to the new passcode
        upsert=True  
    )

    # Check if the operation was successful
    if result is None:
        return jsonify({'status': 'failed', 'data': 'Failed to update the passcode'}), 500

    # Return a success message
    return jsonify({'status': 'complete', 'data': 'Passcode updated successfully'})

    
# 2. CREATE ROUTE FOR '/api/check/combination'

@app.route('/api/check/combination', methods=['POST'])
def check_combination():
    # Get the passcode from the form data
    passcode = request.form['passcode']

    # Connect to the MongoDB database
    client = MongoClient('mongodb://localhost:27017/')
    db = client['elet2415']
    code_collection = db['code']

    # Check if a document with the given passcode exists in the 'code' collection
    num_docs = code_collection.count_documents({'code': passcode})

    # Close the MongoDB connection
    client.close()

    # Return a success message if a document with the given passcode was found, otherwise return an error message
    if num_docs > 0:
        return jsonify({'status': 'complete', 'data': 'complete'})
    else:
        return jsonify({'status': 'failed', 'data': 'failed'})

# 3. CREATE ROUTE FOR '/api/update'

@app.route('/api/update', methods=['POST'])
def update_data():
    # Ensure that the request is a POST request and contains JSON data
    if request.method == 'POST' and request.is_json:
        data = request.get_json()

        try:
            # Call the function to update and publish the data
            result = update_and_publish_data(data)

            if result:
                return jsonify({"status": "complete", "data": "complete"})
            else:
                return jsonify({"status": "failed", "data": "failed"}), 500  # Internal Server Error

        except ValueError as e:
            return jsonify({"status": "failed", "data": str(e)}), 400  # Bad Request

    else:
        return jsonify({"status": "failed", "data": "Method not allowed"}), 405  # Method Not Allowed
   
# 4. CREATE ROUTE FOR '/api/reserve/<start>/<end>'

@app.route('/api/reserve/<start>/<end>', methods=['GET'])
def reserve_data(start, end):
    try:
        # Call the function to retrieve data between the specified timestamps
        data = get_data_between_timestamps(start, end)

        if data:
            return jsonify({"status": "found", "data": data})
        else:
            return jsonify({"status": "failed", "data": 0})

    except ValueError as e:
        return jsonify({"status": "failed", "data": str(e)}), 400  # Bad Request

# 5. CREATE ROUTE FOR '/api/avg/<start>/<end>'

@app.route('/api/avg/<start>/<end>', methods=['GET'])
def calculate_average(start, end):
    try:
        # Call the function to calculate the average of 'reserve' field
        average = calculate_average_between_timestamps(start, end)

        if average is not None:
            return jsonify({"status": "found", "data": average})
        else:
            return jsonify({"status": "failed", "data": 0})

    except ValueError as e:
        return jsonify({"status": "failed", "data": str(e)}), 400  # Bad Request


   






@app.route('/api/file/get/<filename>', methods=['GET']) 
def get_images(filename):   
    '''Returns requested file from uploads folder'''
   
    if request.method == "GET":
        directory   = join( getcwd(), Config.UPLOADS_FOLDER) 
        filePath    = join( getcwd(), Config.UPLOADS_FOLDER, filename) 

        # RETURN FILE IF IT EXISTS IN FOLDER
        if exists(filePath):        
            return send_from_directory(directory, filename)
        
        # FILE DOES NOT EXIST
        return jsonify({"status":"file not found"}), 404


@app.route('/api/file/upload',methods=["POST"])  
def upload():
    '''Saves a file to the uploads folder'''
    
    if request.method == "POST": 
        file     = request.files['file']
        filename = secure_filename(file.filename)
        file.save(join(getcwd(),Config.UPLOADS_FOLDER , filename))
        return jsonify({"status":"File upload successful", "filename":f"{filename}" })

 


###############################################################
# The functions below should be applicable to all Flask apps. #
###############################################################


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.errorhandler(405)
def page_not_found(error):
    """Custom 404 page."""    
    return jsonify({"status": 404}), 404



