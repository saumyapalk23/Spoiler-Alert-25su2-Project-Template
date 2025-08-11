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
    cursor.execute('''
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
    cursor.execute('''SSELECT articleId, title, content
FROM articles
ORDER BY createdAt DESC
LIM 3;
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
def user_favorite():
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
def user_favorite():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT reviewId, title, COUNT(comments) as num_comments
FROM reviews JOIN comments ON reviews.writtenrevID = comments.commentId
GROUP BY reviewId 
ORDER BY num_comments DESC
LIM 3;
);
    ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# users submit/create feedback
@amanda.route('/users/<userId>/feedback/', methods=['POST'])
def user_favorite():
    cursor = db.get_db().cursor()
    cursor.execute('''INSERT INTO userFeedback(feedbackId, title, content, createdAt)
VALUES ({feedbackId}, {title}, {content}, {createdAt});
    ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
