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
@john.route('/shows/release_date/<int:year>', methods=['GET'])
def get_shows_by_date(year):
    cursor = db.get_db().cursor()
    
    # Filter shows by release year
    cursor.execute('''
        SELECT showId, title, rating, releaseDate
        FROM shows
        WHERE YEAR(releaseDate) = %s
        ORDER BY releaseDate DESC
    ''', (year,))
    
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
@john.route('/shows/streaming_platform/<int:platformId>', methods=['GET'])
def get_shows_by_platform(platformId):
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT s.showID, s.title, s.rating, s.releaseDate, s.season, s.ageRating, s.writers, s.viewers, sp.streaming_platform
FROM shows s 
JOIN streaming_pltfm sp ON s.showID = sp.showID
WHERE sp.platformID = %s
ORDER BY s.title ASC;
    ''', (platformId,))
    theData = cursor.fetchall()

    if not theData: 
        response_data = {'message': 'No shows found for this streaming platform', 'platformId': platformId}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 404
        return the_response
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Create a new comment for a particular review
@john.route('/reviews/<int:reviewId>/comments', methods=['POST'])
def create_comment(reviewId):
    data = request.get_json(silent=True) or {}
    user_id = data.get('userID')
    content = (data.get('content') or '').strip()

    if not user_id or not content:
        return make_response(jsonify({'error': 'userID and content are required'}), 400)

    try:
        with db.get_db().cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM reviews WHERE writtenrevId = %s",
                (reviewId,)
            )
            if cursor.fetchone() is None:
                return make_response(jsonify({'error': 'Review not found'}), 404)

            cursor.execute(
                """
                INSERT INTO comments (writtenrevId, userId, content, createdAt)
                VALUES (%s, %s, %s, NOW())
                """,
                (reviewId, user_id, content)
            )
            comment_id = cursor.lastrowid 

        db.get_db().commit()

        return make_response(jsonify({
            'message': 'Comment created successfully',
            'commentId': comment_id,
            'writtencomID': comment_id,
            'writtenrevId': reviewId
        }), 201)

    except Exception:
        db.get_db().rollback()
        return make_response(jsonify({'error': 'Internal server error'}), 500)
#------------------------------------------------------------

# Update a comment for a particular review
@john.route('/reviews/<int:reviewId>/comments/<int:commentId>', methods=['PUT'])
def update_comment(reviewId, commentId):
    req = request.get_json(force=True) or {}
    new_content = (req.get('content') or '').strip()
    user_id = int(req.get('userID', 0))

    if not new_content:
        the_response = make_response(jsonify({"error": "content is required"}))
        the_response.status_code = 400
        return the_response

    sql = """
        UPDATE comments
        SET content = %s
        WHERE commentId = %s AND writtenrevId = %s AND userId = %s
    """
    args = (new_content, commentId, reviewId, user_id)

    cur = db.get_db().cursor()
    cur.execute(sql, args)
    db.get_db().commit()

    if cur.rowcount == 0:
        the_response = make_response(jsonify(
            {"error": "Comment not found or user not authorized to update this comment"}
        ))
        the_response.status_code = 404
        return the_response

    the_response = make_response(jsonify({"message": "Comment updated successfully"}))
    the_response.status_code = 200
    return the_response
    
    
#------------------------------------------------------------
# Delete a comment for a particular review
@john.route('/reviews/<int:reviewId>/comments/<int:commentId>', methods=['DELETE'])
def delete_comment(reviewId, commentId):
    req = request.get_json(force=True) or {}
    user_id = int(req.get('userID', 0))

    if not user_id:
        the_response = make_response(jsonify({"error": "userID is required"}))
        the_response.status_code = 400
        return the_response

    sql = """
        DELETE FROM comments
        WHERE commentId = %s AND writtenrevId = %s AND userId = %s
    """
    args = (commentId, reviewId, user_id)

    cur = db.get_db().cursor()
    cur.execute(sql, args)
    db.get_db().commit()

    if cur.rowcount == 0:
        the_response = make_response(jsonify(
            {"error": "Comment not found or user not authorized to delete this comment"}
        ))
        the_response.status_code = 404
        return the_response

    the_response = make_response(jsonify({"message": "Comment deleted successfully"}))
    the_response.status_code = 200
    return the_response