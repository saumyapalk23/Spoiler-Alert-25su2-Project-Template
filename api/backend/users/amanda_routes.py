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
amanda = Blueprint('amanda', __name__)


#------------------------------------------------------------
# Get top five most reviewed shows
@amanda.route('/shows/most-reviewed', methods=['GET'])
def top_reviewed():


    cursor = db.get_db().cursor()
    cursor.execute('''SELECT s.showId, s.title, COUNT(r.writtenrevId) AS num_reviews
FROM shows s JOIN reviews r ON s.showId = r.showId
GROUP BY s.showId, s.title
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
# Get genres of three most recent articles
@amanda.route('/articles/most-recent/genres', methods=['GET'])
def get_recent_articles_genres():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT a.articleID, a.title, a.createdAt, g.title as genre_title
        FROM articles a
        JOIN article_genre ag ON a.articleID = ag.articleId
        JOIN genre g ON ag.genreId = g.genreId
        JOIN (
            SELECT articleID
            FROM articles
            ORDER BY createdAt DESC
            LIMIT 3
        ) recent_articles ON a.articleID = recent_articles.articleID
        ORDER BY a.createdAt DESC, g.title;
    ''')
   
    genres = cursor.fetchall()
   
    the_response = make_response(jsonify({"genres": genres}))
    the_response.status_code = 200
    return the_response




#------------------------------------------------------------
# adds a show to favorites
@amanda.route('/users/<user_id>/favorites/', methods=['POST'])
def user_favorite(user_id):
    cursor = db.get_db().cursor()
    
    request_data = request.get_json()
    favorite_id = request_data.get('favoriteID')
    show_id = request_data.get('showId')
    
    cursor.execute('''
        INSERT INTO favorites (userID, favoriteID, showId)
        VALUES (%s, %s, %s)
    ''', (user_id, favorite_id, show_id))
    
    db.get_db().commit()
    
    the_response = make_response(jsonify({"message": "Favorite added successfully"}))
    the_response.status_code = 200
    return the_response
   
#------------------------------------------------------------
# removes a show/actor to favorites
@amanda.route('/users/<user_id>/favorites/', methods=['DELETE'])
def remove_user_favorite(user_id):
    cursor = db.get_db().cursor()
    
    request_data = request.get_json()
    favorite_id = request_data.get('favoriteID')
    show_id = request_data.get('showId')
    
    cursor.execute('''
        DELETE FROM favorites 
        WHERE userID = %s AND favoriteID = %s AND showId = %s
    ''', (user_id, favorite_id, show_id))
    
    db.get_db().commit()
    
    the_response = make_response(jsonify({"message": "Favorite removed successfully"}))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# retrieves most popular reviews by comments
@amanda.route('/reviews/most-popular', methods=['GET'])
def get_pop():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT s.title, r.writtenrevId, r.content, COUNT(c.commentId) as num_comments
FROM reviews r JOIN comments c ON r.writtenrevId = c.writtenrevId
JOIN shows s ON r.showId = s.showId
GROUP BY r.writtenrevId
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
def give_fb(userId):
    the_data = request.json
    current_app.logger.info(the_data)
    content = the_data['content']
    userId = the_data['userId']
    query = f'''
        INSERT INTO userFeedback (content, userId)
        VALUES (%s, %s);'''
    current_app.logger.info(query)


    # executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query, (content, userId))
    db.get_db().commit()
   
    response = make_response("Successfully added feedback!")
    response.status_code = 200
    return 'feedback submitted!'


    # users submit/create feedback
@amanda.route('/users/feedback/', methods=['GET'])
def get_fb():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT userId, content, createdAt
    FROM userFeedback
    ORDER BY createdAt
    ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# get all favorites
@amanda.route('/users/favorites/', methods=['GET'])
def get_user_favorites():
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        SELECT userID, favoriteID, showId
        FROM favorites 
        ORDER BY favoritedAt
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
