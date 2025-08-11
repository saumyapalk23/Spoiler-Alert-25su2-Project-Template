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
john = Blueprint('john', __name__)


#------------------------------------------------------------
# Get all shows based on release date
@john.route('/shows', methods=['GET'])
def get_shows_by_date():

    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT showId, title, releaseDate, genre, description
    FROM shows
    ORDER BY releaseDate DESC; 
    ''')
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get all shows based on certain keywords
@john.route('/shows/search', methods=['GET'])
def search_shows():
    # Get search keyword from query parameters
    search_keyword = request.args.get('keyword', '').strip()
    cursor = db.get_db().cursor()
    if search_keyword: 
        cursor.execute('''
            SELECT DISTINCT s.showID, s.title, s.rating, s.releaseDate, s.season, s.ageRating, s.writers, s.viewers
            FROM shows s 
            LEFT JOIN keywords k ON k.showID = s.showID
            WHERE k.keyword LIKE %s 
                OR s.title LIKE %s
                OR s.description LIKE %s
            ORDER BY s.title ASC;
        ''', (f'%{search_keyword}%', f'%{search_keyword}%', f'%{search_keyword}%'))
    else: 
        cursor.execute('''
            SELECT s.showID, s.title, s.rating, s.releaseDate, s.season, s.ageRating, s.writers, s.viewers
            FROM shows s
            ORDER BY s.title ASC;
        ''')
    
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get genres of all articles
@john.route('/articles/genres', methods=['GET'])
def article_genre():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT DISTINCT g.genre 
        FROM articles a 
        JOIN articles_genres ag ON a.articleID = ag.articleID 
        JOIN genres g ON ag.genreId = g.genreId
        ORDER BY g.genre ASC;
    ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get shows ordered by genre
@john.route('/shows/genre/<int:genreId>', methods=['GET'])
def get_shows_by_genre(genreId):
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT DISTINCT s.showID, s.title, s.rating, s.releaseDate, s.season, s.ageRating, s.writers, s.viewers, g.genre, g.description as genre_description
    FROM shows s 
    JOIN show_genre sg ON s.showID = sg.showID
    JOIN genre g ON sg.genreId = g.genreId
    WHERE g.genreId = %s
    ORDER BY s.title ASC;
    ''', (genreId,))
    
    theData = cursor.fetchall()
    
    if not theData:
        response_data = {'message': 'No shows found for this genre', 'genreId': genreId}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 404
        return the_response
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# Retrieves all shows based on certain streaming platform
@john.route('/shows/streaming_platform/<platformId>', methods=['GET'])
def get_shows_by_platform(platformId):
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT s.showID, s.title, s.rating, s.releaseDate, s.season, s.ageRating, s.writers, s.viewers, sp.streaming_platform
FROM Shows s 
JOIN streaming_pltfm sp ON s.showID = sp.showID
WHERE sp.streaming_platform = %s
ORDER BY s.title ASC;
    ''', (platformId,))
    
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Create a new comment for a particular review
@john.route('/reviews/<reviewId>/comments', methods=['POST'])
def create_comment(reviewId):
    request_data = request.json
    user_id = request_data.get('userID')
    comment_content = request_data.get('content')
    
    # Verify the review exists
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT writtenrevID FROM Reviews WHERE writtenrevID = %s''', (reviewId,))
    
    if not cursor.fetchone():
        response_data = {'error': 'Review not found'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 404
        return the_response
    
    cursor.execute('''INSERT INTO Comments (writtenrevID, userID, content, createdAt)
VALUES (%s, %s, %s, NOW());
    ''', (reviewId, user_id, comment_content))
    
    db.get_db().commit()
    
    # Get the newly created comment ID
    comment_id = cursor.lastrowid
    
    response_data = {
        'message': 'Comment created successfully', 
        'writtencomID': comment_id,
        'writtenrevID': reviewId
    }
    the_response = make_response(jsonify(response_data))
    the_response.status_code = 201
    return the_response

#------------------------------------------------------------
# Update a comment for a particular review
@john.route('/reviews/<reviewId>/comments', methods=['PUT'])
def update_comment(reviewId):
    request_data = request.json
    comment_id = request_data.get('writtencomID')
    new_content = request_data.get('content')
    user_id = request_data.get('userID')
    
    cursor = db.get_db().cursor()
    cursor.execute('''UPDATE Comments 
SET content = %s, createdAt = NOW()
WHERE writtencomID = %s AND writtenrevID = %s AND userID = %s;
    ''', (new_content, comment_id, reviewId, user_id))
    
    db.get_db().commit()
    
    if cursor.rowcount == 0:
        response_data = {'error': 'Comment not found or user not authorized to update this comment'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 404
    else:
        response_data = {
            'message': 'Comment updated successfully',
            'writtencomID': comment_id,
            'writtenrevID': reviewId
        }
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 200
    
    return the_response

#------------------------------------------------------------
# Delete a comment for a particular review
@john.route('/reviews/<reviewId>/comments', methods=['DELETE'])
def delete_comment(reviewId):
    request_data = request.json
    comment_id = request_data.get('writtencomID')
    user_id = request_data.get('userID')
    
    cursor = db.get_db().cursor()
    cursor.execute('''DELETE FROM Comments 
WHERE writtencomID = %s AND writtenrevID = %s AND userID = %s;
    ''', (comment_id, reviewId, user_id))
    
    db.get_db().commit()
    
    if cursor.rowcount == 0:
        response_data = {'error': 'Comment not found or user not authorized to delete this comment'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 404
    else:
        response_data = {
            'message': 'Comment deleted successfully',
            'writtencomID': comment_id,
            'writtenrevID': reviewId
        }
        the_response = make_response(jsonify(response_data))
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