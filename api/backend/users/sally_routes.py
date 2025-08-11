########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
sally = Blueprint('sally', __name__)


#------------------------------------------------------------
# Add a rating for a particular show
@sally.route('/shows/<int:showId>', methods=['POST'])
def add_show_rating(showId):
    data = request.get_json()
    rating = data.get('rating')

    cursor = db.get_db().cursor()
    cursor.execute('''
        INSERT INTO ratings (showId, rating)
        VALUES (%s, %s);
    ''', (showId, rating))
    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Rating added successfully"}))
    the_response.status_code = 201
    return the_response

#------------------------------------------------------------
# Retrive all watchlists for a user 
@sally.route('/users/<int:userId>/watchlists', methods=['GET'])
def get_user_watchlists(userId): 
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT watchlistId, userId, name, createdAt
        FROM watchlists
        WHERE userId = %s;
    ''', (userId))
    theData = cursor.fetchall()

    the_response = make_response(jsonify())
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Create a new watchlist for user
@sally.route('/users/<int:userId>/watchlists', methods=['POST'])
def create_watchlist(userId): 
    data = request.get_json()
    name = data.get('name')

    cursor = db.get_db().cursor()
    cursor.execute('''
        INSERT INTO watchlists (userId, name)
        VALUES (%s, %s);
    ''', (userId, name))
    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Watchlist created"}))
    the_response.status_code = 201
    return the_response

#------------------------------------------------------------
# Delete an existing watchlist for a user
@sally.route('/users/<int:userId>/watchlists/<int:watchlistId>', methods=['DELETE'])
def delete_watchlist(userId, watchlistId):
    cursor = db.get_db().cursor()
    cursor.execute('''
        DELETE FROM watchlists
        WHERE watchlistId = %s AND userId = %s;
    ''', (watchlistId, userId))
    db.get_db().commit()

    if cursor.rowcount == 0:
        the_response = make_response(jsonify({"error": "Watchlist not found"}))
        the_response.status_code = 404
        return the_response

    the_response = make_response(jsonify({"message": "Watchlist deleted successfully"}))
    the_response.status_code = 200
    return the_response

# #------------------------------------------------------------
# # Update customer info for customer with particular userID
# #   Notice the manner of constructing the query.
# @customers.route('/customers', methods=['PUT'])
# def update_customer():
#     current_app.logger.info('PUT /customers route')
#     cust_info = request.json
#     cust_id = cust_info['id']
#     first = cust_info['first_name']
#     last = cust_info['last_name']
#     company = cust_info['company']

#     query = 'UPDATE customers SET first_name = %s, last_name = %s, company = %s where id = %s'
#     data = (first, last, company, cust_id)
#     cursor = db.get_db().cursor()
#     r = cursor.execute(query, data)
#     db.get_db().commit()
#     return 'customer updated!'

# #------------------------------------------------------------
# # Get customer detail for customer with particular userID
# #   Notice the manner of constructing the query. 
# @customers.route('/customers/<userID>', methods=['GET'])
# def get_customer(userID):
#     current_app.logger.info('GET /customers/<userID> route')
#     cursor = db.get_db().cursor()
#     cursor.execute('SELECT id, first_name, last_name FROM customers WHERE id = {0}'.format(userID))
    
#     theData = cursor.fetchall()
    
#     the_response = make_response(jsonify(theData))
#     the_response.status_code = 200
#     return the_response

# #------------------------------------------------------------
# # Makes use of the very simple ML model in to predict a value
# # and returns it to the user
# @customers.route('/prediction/<var01>/<var02>', methods=['GET'])
# def predict_value(var01, var02):
#     current_app.logger.info(f'var01 = {var01}')
#     current_app.logger.info(f'var02 = {var02}')

#     returnVal = predict(var01, var02)
#     return_dict = {'result': returnVal}

#     the_response = make_response(jsonify(return_dict))
#     the_response.status_code = 200
#     the_response.mimetype = 'application/json'
#     return the_response