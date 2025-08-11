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
# Users add a rating to a show
@sally.route('/shows/{id}', methods=['POST'])
def user_rating():
    cursor = db.get_db().cursor()
    cursor.execute('''
INSERT INTO shows (showID, title, rating, releaseDate, season, ageRating)
VALUES ({showID}, '{title}', {rating}, '{releaseDate}', {season}, '{ageRating}');''')
    db.get_db().commit()
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Retrieve all of a user's watchlists
@sally.route('/users/<id>/watchlist', methods=['GET'])
def get_watchlists():
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT name, showId
    FROM watchlist
    WHERE userId = %s
    ORDER BY createdAt DESC;''', (id, ))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Create a watchlist
@sally.route('/users/<id>/watchlist', methods=['POST'])
def addto_watchlist():
    cursor = db.get_db().cursor()
    # TODO: watchId, name, showId
    cursor.execute('''
    INSERT INTO watchlist (%s,%s,%s,%s,)''', (watchId, id, name, showId))
    db.get_db().commit()
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add shows to watchlist
@sally.route('users/<u_id>/watchlist/<name>/shows/<s_id>', methods=['POST'])
def addto_watchlist():
    cursor = db.get_db().cursor()
    # TODO: watchId, name, showId
    cursor.execute('''
    INSERT INTO watchlist (%s,%s,%s,%s,)''', (_, u_id, name, s_id))
    db.get_db().commit()
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Delete shows from watchlist

#------------------------------------------------------------
# Recommendations from age group

#------------------------------------------------------------
# User adds a user to following

#------------------------------------------------------------
# User removes a user from following

#------------------------------------------------------------
# Creates a new review for a show

#------------------------------------------------------------
# Updates a review

#------------------------------------------------------------
# Deletes a review
