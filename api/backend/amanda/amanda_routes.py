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
# from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
amanda = Blueprint('amanda', __name__)


#------------------------------------------------------------
# Get top five most reviewed shows
@amanda.route('/shows/most-reviewed', methods=['GET'])
def top_reviewed():
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT s.showID, s.title, COUNT(writtenrevID) AS num_reviews
    FROM shows s JOIN reviews r ON s.showID = r.showID
    GROUP BY s.showID, s.title
    ORDER BY num_reviews DESC
    LIMIT 5;
    ''')
    
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get top three most recent articles
@amanda.route('/articles/most-recent', methods=['GET'])
def most_recent():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT articleId, title, content
FROM articles
ORDER BY createdAt DESC
LIMIT 3;
    ''')
    
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# Get genres of all articles
@amanda.route('/articles/genres', methods=['GET'])
def article_genre():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT DISTINCT G.genre FROM articles a 
    JOIN articles_genres ag ON a.articleID = ag.articleID 
    JOIN genres g ON ag.genreID = g.genreID
    ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# adds a show/actor to favorites
@amanda.route('/users/<userId>/favorites/', methods=['POST'])
def add_favorites():
    cursor = db.get_db().cursor()
    cursor.execute('''INSERT INTO favorites (userID, favoriteID)
VALUES ({userId}, {favoriteID}, {showId}, {actorId});
    ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
    
#------------------------------------------------------------
# removes a show/actor to favorites
@amanda.route('/users/<userId>/favorites/', methods=['DELETE'])
def delete_favorites():
    cursor = db.get_db().cursor()
    cursor.execute('''DELETE FROM favorites (userID, favoriteID)
VALUES ({userId}, {favoriteID}, {showId}, {actorId});
    ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# retrieves most popular reviews by comments
@amanda.route('/reviews/most-popular', methods=['GET'])
def popular_reviews():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT reviewId, title, COUNT(comments) as num_comments
FROM reviews JOIN comments ON reviews.writtenrevID = comments.commentId
GROUP BY reviewId 
ORDER BY num_comments DESC
LIMIT 3;
    ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# users submit/create feedback
@amanda.route('/users/<userId>/feedback/', methods=['POST'])
def add_feedback():
    cursor = db.get_db().cursor()
    cursor.execute('''INSERT INTO userFeedback(feedbackId, title, content, createdAt)
VALUES ({feedbackId}, {title}, {content}, {createdAt});
    ''')
    theData = cursor.fetchall()
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