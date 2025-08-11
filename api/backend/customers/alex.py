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
alex = Blueprint('Alex', __name__)


#------------------------------------------------------------
# Get the season length of a specific show
@alex.route('/shows/season-length', methods=['GET'])
def get_season_length():
    # Get showID from query parameters
    show_id = request.args.get('showID')
    
    if not show_id:
        response_data = {'error': 'showID parameter is required'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 400
        return the_response
    
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT showID, title, season
FROM Shows 
WHERE showID = %s;
    ''', (show_id,))
    
    theData = cursor.fetchone()
    
    if not theData:
        response_data = {'error': 'Show not found', 'showID': show_id}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 404
        return the_response
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
#------------------------------------------------------------
# Get all users on the app
@alex.route('/users', methods=['GET'])
def get_all_users():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT *
FROM Users 
ORDER BY name ASC;
    ''')
    
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get the mean star ranking for a specific show
@alex.route('/shows/<showId>/average-ranking', methods=['GET'])
def get_average_ranking(showId):
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT s.showID, s.title, AVG(r.starRating) as average_rating, COUNT(r.writtenrevID) as total_reviews
FROM Shows s 
LEFT JOIN Reviews r ON s.showID = r.showID
WHERE s.showID = %s
GROUP BY s.showID, s.title;
    ''', (showId,))
    
    theData = cursor.fetchone()
    
    if not theData:
        response_data = {'error': 'Show not found', 'showID': showId}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 404
        return the_response
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get the most recent reviews for a specific show
@alex.route('/shows/<showId>/reviews/most-recent', methods=['GET'])
def get_most_recent_reviews(showId):
    # Optional limit parameter, default to 5
    limit = request.args.get('limit', 5, type=int)
    
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT r.writtenrevID, r.userID, r.starRating, r.content, r.createdAt, u.name as reviewer_name
FROM Reviews r 
JOIN Users u ON r.userID = u.userID
WHERE r.showID = %s
ORDER BY r.createdAt DESC
LIMIT %s;
    ''', (showId, limit))
    
    theData = cursor.fetchall()
    
    if not theData:
        response_data = {'message': 'No reviews found for this show', 'showID': showId}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 200
        return the_response
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# Get the most popular/common time that reviews are written at
@alex.route('/reviews/time-most-reviewed', methods=['GET'])
def get_most_popular_review_time():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT HOUR(createdAt) as review_hour, COUNT(*) as review_count
FROM Reviews
GROUP BY HOUR(createdAt)
ORDER BY review_count DESC
LIMIT 5;
    ''')
    
    theData = cursor.fetchall()
    
    if not theData:
        response_data = {'message': 'No review data available'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 200
        return the_response
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# Get the number of times a specific show has been watched
@alex.route('/shows/<showId>/watches/num-watches', methods=['GET'])
def get_show_watch_count(showId):
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT s.showID, s.title, COUNT(w.viewerID) as total_watches
FROM Shows s 
LEFT JOIN Watches w ON s.showID = w.showID
WHERE s.showID = %s
GROUP BY s.showID, s.title;
    ''', (showId,))
    
    theData = cursor.fetchone()
    
    if not theData:
        response_data = {'error': 'Show not found', 'showID': showId}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 404
        return the_response
    
    the_response = make_response(jsonify(theData))
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