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
from datetime import datetime, date

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
    kw = (request.args.get('keyword') or '').strip()

    cursor = db.get_db().cursor()

    base_sql = """
        SELECT DISTINCT
            s.showID, s.title, s.rating, s.releaseDate, s.season, s.ageRating, s.streamingPlatform
        FROM shows s
        LEFT JOIN keyword k ON k.showId = s.showID
    """

    if kw:
        like = f"%{kw}%"
        sql = base_sql + """
            WHERE k.keyword LIKE %s
               OR s.title LIKE %s
               OR s.streamingPlatform LIKE %s
            ORDER BY s.title ASC;
        """
        cursor.execute(sql, (like, like, like))
    else:
        sql = base_sql + " ORDER BY s.title ASC;"
        cursor.execute(sql)

    rows = cursor.fetchall()

    if rows and isinstance(rows[0], dict):
        data = rows
    else:
        cols = [d[0] for d in cursor.description]
        data = [dict(zip(cols, r)) for r in rows]

    resp = make_response(jsonify(data))
    resp.status_code = 200
    return resp

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
    cursor.execute(
        """
        SELECT DISTINCT
            s.showID, s.title, s.rating, s.releaseDate, s.season, s.ageRating,
            g.title AS genreTitle
        FROM shows s
        JOIN show_genre sg ON sg.showId = s.showID
        JOIN genre g ON g.genreId = sg.genreId
        WHERE g.genreId = %s
        ORDER BY s.title ASC;
        """,
        (genreId,)
    )
    rows = cursor.fetchall()
    the_response = make_response(jsonify(rows))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Retrieves all shows based on certain streaming platform
PLATFORMS = {
    "Netflix": 1, "Hulu": 2, "Prime Video": 3, "Disney+": 4,
    "HBO Max": 5, "Apple TV+": 6, "Peacock": 7, "Paramount+": 8,
    "Fubo": 9, "BBC": 10, "Crunchyroll": 11, "Discovery+": 12,
    "ESPN": 13, "FandangoNow": 14, "YouTube": 15, "PlutoTV": 16,
}
PLATFORM_ID2NAME = {v: k for k, v in PLATFORMS.items()}

@john.route('/shows/streaming_platform/<int:platform_id>', methods=['GET'])
def get_shows_by_platform(platform_id):
    name = PLATFORM_ID2NAME.get(platform_id)
    if not name:
        return make_response(jsonify({"error": "unknown platform id"}), 400)

    sql = """
        SELECT s.showID, s.title, s.rating, s.releaseDate, s.season, s.ageRating, s.streamingPlatform
        FROM shows s
        JOIN streaming_pltfm sp ON sp.showId = s.showID
        WHERE sp.platform = %s
        ORDER BY s.title ASC
    """
    cursor = db.get_db().cursor()
    cursor.execute(sql, (name,))
    rows = cursor.fetchall()
    if rows and not isinstance(rows[0], dict):
        cols = [d[0] for d in cursor.description]
        rows = [dict(zip(cols, r)) for r in rows]
    return make_response(jsonify(rows), 200)

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
@john.route('/reviews/<int:writtenrevId>/comments/<int:commentId>', methods=['PUT'])
def update_comment(writtenrevId, commentId):
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
    args = (new_content, commentId, writtenrevId, user_id)

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
@john.route('/reviews/<int:writtenrevId>/comments/<int:commentId>', methods=['DELETE'])
def delete_comment(writtenrevId, commentId):
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
    args = (commentId, writtenrevId, user_id)

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

#Comments display route 
@john.route('/users/<int:user_id>/comments/activity', methods=['GET'])
def user_comment_activity(user_id):
    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT COUNT(*) AS has_col
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'comments'
          AND COLUMN_NAME = 'updatedAt'
    """)
    row = cursor.fetchone()
    has_updated = (row['has_col'] if isinstance(row, dict) else row[0]) > 0

    if has_updated:
        sql = """
            SELECT * FROM (
                SELECT
                    c.commentId      AS commentId,
                    c.writtenrevId   AS reviewId,
                    c.userId         AS userId,
                    c.content        AS content,
                    c.createdAt      AS activityAt,
                    'created'        AS action
                FROM comments c
                WHERE c.userId = %s

                UNION ALL

                SELECT
                    c.commentId      AS commentId,
                    c.writtenrevId   AS reviewId,
                    c.userId         AS userId,
                    c.content        AS content,
                    c.updatedAt      AS activityAt,
                    'updated'        AS action
                FROM comments c
                WHERE c.userId = %s
                  AND c.updatedAt IS NOT NULL
                  AND c.updatedAt > c.createdAt
            ) x
            ORDER BY x.activityAt DESC;
        """
        cursor.execute(sql, (user_id, user_id))
    else:
        sql = """
            SELECT
                c.commentId      AS commentId,
                c.writtenrevId   AS reviewId,
                c.userId         AS userId,
                c.content        AS content,
                c.createdAt      AS activityAt,
                'created'        AS action
            FROM comments c
            WHERE c.userId = %s
            ORDER BY c.createdAt DESC;
        """
        cursor.execute(sql, (user_id,))

    rows = cursor.fetchall()
    if rows and not isinstance(rows[0], dict):
        cols = [d[0] for d in cursor.description]
        rows = [dict(zip(cols, r)) for r in rows]

    resp = make_response(jsonify(rows))
    resp.status_code = 200
    return resp