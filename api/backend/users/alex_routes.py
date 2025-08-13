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
#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
alex = Blueprint('alex', __name__)

# ------------------------------------------------------------
# Get number of szns from the system
@alex.route('/shows', methods=['GET'])
def get_szn():
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT
                showId,
                title,
                season     
            FROM
                shows
            ORDER BY
                season, title;
        ''')
        theData = cursor.fetchall()
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
        return the_response
# ------------------------------------------------------------
# Get all customers from the system
@alex.route('/users', methods=['GET'])
def get_userCount():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT COUNT(userId) as num_users
FROM users
ORDER BY num_users;
   ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# ------------------------------------------------------------
# Get average ratings for a top 5 shows
@alex.route('/shows/<showId>', methods=['GET'])
def show_avgrev(showId):
    current_app.logger.info('GET /shows/<showId> route')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT s.title, AVG(r.rating) as average_rating
FROM reviews r JOIN shows s ON r.showId = s.showId
GROUP BY r.showId
ORDER BY average_rating DESC
LIMIT 5;
   ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# ------------------------------------------------------------
# Get most recent reviews for a particular show
@alex.route('/shows/<id>/reviews/most-recent', methods=['GET'])
def most_recentrev(id):
    cursor = db.get_db().cursor()
    cursor.execute('''
SELECT r.userId, u.userName, s.title, s.showId, writtenrevId, content, createdAt, r.rating
FROM reviews r JOIN shows s ON r.showId = s.showId
JOIN users u ON r.userId = u.userId
ORDER BY s.showId, createdAt DESC
LIMIT 5;
   ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# ------------------------------------------------------------
# Get when reviews are made (timestamps)
@alex.route('/reviews/time-reviewed', methods=['GET'])
def time_reviewed():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT writtenrevId, createdAt, content
        FROM reviews;
   ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# ------------------------------------------------------------
# Get how many times a show has been watched
@alex.route('/shows/<id>/watches/num-watches', methods=['GET'])
def view_times(id):
    cursor = db.get_db().cursor()
    cursor.execute('''
SELECT w.showId, s.title, COUNT(*) as num_watches
FROM watches w JOIN shows s ON w.showId = s.showId
GROUP BY w.showId
ORDER BY num_watches DESC;
   ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


