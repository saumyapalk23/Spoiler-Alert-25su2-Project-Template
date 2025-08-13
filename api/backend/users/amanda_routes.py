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
# adds a show/actor to favorites
@amanda.route('/users/<userId>/favorites/', methods=['POST'])
def user_favorite():
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
def delete_favorite():
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
def get_pop():
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
def get_fb(userId):
    the_data = request.json
    current_app.logger.info(the_data)
    title = the_data['title']
    content = the_data['content']
    userId = the_data['userId']
    query = f'''
        INSERT INTO userFeedback (title, content, userId)
        VALUES (%s, %s, %s);'''
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query, (title, content, userId))
    db.get_db().commit()
    
    response = make_response("Successfully added feedback!")
    response.status_code = 200
    return 'feedback submitted!'