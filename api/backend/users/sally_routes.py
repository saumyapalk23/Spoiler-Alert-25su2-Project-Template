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
# Updates a rating of a review for a particular show
@sally.route('/shows/<int:showId>/reviews/<int:reviewId>', methods=['PUT'])
def update_review_rating(showId, reviewId):
    data = request.get_json()
    rating = data.get('rating')

    cursor = db.get_db().cursor()
    cursor.execute('''
        UPDATE reviews SET rating = %s 
        WHERE writtenrevID = %s AND showID = %s;
    ''', (rating, reviewId, showId))
    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Review rating updated successfully"}))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Retrive all watchlists for a user 
@sally.route('/users/<int:userId>/watchlist', methods=['GET'])
def get_user_watchlists(userId):
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT toWatchId, userId, name, createdAt
        FROM watchlist
        WHERE userId = %s;
    ''', (userId,))
    theData = cursor.fetchall()
    
    # Convert to list of dictionaries if needed
    watchlists = []
    for row in theData:
        watchlists.append({
            'toWatchId': row['toWatchId'],  # or row[0] if using tuple
            'userId': row['userId'],        # or row[1]
            'name': row['name'],           # or row[2]
            'createdAt': row['createdAt']  # or row[3]
        })
    
    return make_response(jsonify(watchlists), 200)

#------------------------------------------------------------
# Create a new watchlist for user
@sally.route('/users/<int:userId>/watchlist', methods=['POST'])
def create_watchlist(userId): 
    data = request.get_json()
    name = data.get('name')
    show_id = data.get('showId')  # Add showId from request
    
    # Validate required fields
    if not name or not show_id:
        return make_response(jsonify({"error": "Both name and showId are required"}), 400)

    cursor = db.get_db().cursor()
    
    # Use alias to make column access easier
    cursor.execute('SELECT MAX(toWatchId) as max_id FROM watchlist')
    max_id_result = cursor.fetchone()
    
    # Now we can access it consistently
    max_id = max_id_result['max_id'] if max_id_result['max_id'] is not None else 0
    new_to_watch_id = max_id + 1
    
    # Insert with the calculated toWatchId and showId
    cursor.execute('''
        INSERT INTO watchlist (toWatchId, userId, name, showId)
        VALUES (%s, %s, %s, %s);
    ''', (new_to_watch_id, userId, name, show_id))
    
    db.get_db().commit()

    the_response = make_response(jsonify({
        "message": "Watchlist created",
        "toWatchId": new_to_watch_id,
        "showId": show_id
    }))
    the_response.status_code = 201
    return the_response


#------------------------------------------------------------
# Adds new shows in a watchlist
@sally.route('/user/<int:userId>/watchlist/shows/<int:showId>', methods=['PUT'])
def add_to_watchlist(userId, showId): 
    data = request.get_json()
    watchlist_id = data.get('toWatchId')  
    
    if not watchlist_id:
        response_data = {'error': 'toWatchId is required in request body'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 400
        return the_response

    cursor = db.get_db().cursor()
    
    # Check that watchlist exists and belongs to the user
    cursor.execute('''SELECT toWatchId FROM watchlist WHERE toWatchId = %s AND userId = %s''', 
                   (watchlist_id, userId))
    
    if not cursor.fetchone():
        response_data = {'error': 'Watchlist not found or does not belong to user'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 404
        return the_response
    
    # Check that the show exists
    cursor.execute('''SELECT showID FROM shows WHERE showID = %s''', (showId,))
    
    if not cursor.fetchone():
        response_data = {'error': 'Show not found'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 404
        return the_response
    
    # Check if the show is already in this watchlist
    cursor.execute('''SELECT * FROM comp_lists WHERE toWatchId = %s AND showId = %s''', 
                   (watchlist_id, showId))
    
    if cursor.fetchone():
        response_data = {'error': 'Show already in watchlist'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 409  
        return the_response
    
    # Add the show to the watchlist via the comp_lists junction table
    cursor.execute('''INSERT INTO comp_lists (toWatchId, showId) VALUES (%s, %s)''', 
                   (watchlist_id, showId))
    
    # Update the numberOfElements in the watchlist table
    cursor.execute('''UPDATE watchlist 
                      SET numberOfElements = numberOfElements + 1
                      WHERE toWatchId = %s AND userId = %s''', 
                   (watchlist_id, userId))
    
    db.get_db().commit()
    
    if cursor.rowcount == 0:
        response_data = {'error': 'Failed to update watchlist element count'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 500
    else:
        response_data = {
            'message': 'Show added to watchlist successfully',
            'userId': userId,
            'showId': showId,
            'toWatchId': watchlist_id
        }
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 201  # Created
    
    return the_response

#------------------------------------------------------------
# Deletes shows in a watchlist

@sally.route('/user/<int:userId>/watchlist/shows/<int:showId>', methods=['DELETE'])
def delete_from_watchlist(userId, showId): 
    data = request.get_json()
    watchlist_id = data.get('toWatchId')  
    
    if not watchlist_id:
        response_data = {'error': 'toWatchId is required in request body'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 400
        return the_response

    cursor = db.get_db().cursor()
    
    # Check that watchlist exists and belongs to the user
    cursor.execute('''SELECT toWatchId FROM watchlist WHERE toWatchId = %s AND userId = %s''', 
                   (watchlist_id, userId))
    
    if not cursor.fetchone():
        response_data = {'error': 'Watchlist not found or does not belong to user'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 404
        return the_response
    
    # Check that the show exists
    cursor.execute('''SELECT showID FROM shows WHERE showID = %s''', (showId,))
    
    if not cursor.fetchone():
        response_data = {'error': 'Show not found'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 404
        return the_response
    
    # Check if the show is actually in this watchlist
    cursor.execute('''SELECT * FROM comp_lists WHERE toWatchId = %s AND showId = %s''', 
                   (watchlist_id, showId))
    
    if not cursor.fetchone():
        response_data = {'error': 'Show not found in watchlist'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 409  
        return the_response
    
    # Add the show to the watchlist via the comp_lists junction table
    cursor.execute('''DELETE FROM comp_lists WHERE toWatchId = %s AND showId = %s''', 
                   (watchlist_id, showId))
    
    # Update the numberOfElements in the watchlist table
    cursor.execute('''UPDATE watchlist 
                      SET numberOfElements = GREATEST(numberOfElements - 1, 0)
                      WHERE toWatchId = %s AND userId = %s''', 
                   (watchlist_id, userId))
    
    db.get_db().commit()
    
    if cursor.rowcount == 0:
        response_data = {'error': 'Failed to update watchlist element count'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 500
    else:
        response_data = {
            'message': 'Show added to watchlist successfully',
            'userId': userId,
            'showId': showId,
            'toWatchId': watchlist_id
        }
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 201  # Created
    
    return the_response


#------------------------------------------------------------
# Gets shows favorited by users in a specific age group

@sally.route('/shows/favorites/users', methods=['GET'])
def get_favorite_shows_by_users():

    age = request.args.get('age')
    
    cursor = db.get_db().cursor()
    
    if age:
 
        cursor.execute('''
            SELECT s.showID, s.title, s.rating, s.releaseDate, 
                   s.season, s.ageRating, s.streamingPlatform,
                   COUNT(f.favoriteId) as favorite_count
            FROM shows s
            JOIN favorites f ON s.showID = f.showId
            JOIN users u ON f.userId = u.userId
            WHERE u.age = %s
            GROUP BY s.showID, s.title, s.rating, s.releaseDate, s.season, s.ageRating, s.streamingPlatform
            ORDER BY favorite_count DESC, s.rating DESC;
        ''', (age,))
    else:

        cursor.execute('''
            SELECT s.showID, s.title, s.rating, s.releaseDate, 
                   s.season, s.ageRating, s.streamingPlatform,
                   COUNT(f.favoriteId) as favorite_count
            FROM shows s
            JOIN favorites f ON s.showID = f.showId
            JOIN users u ON f.userId = u.userId
            GROUP BY s.showID, s.title, s.rating, s.releaseDate, s.season, s.ageRating, s.streamingPlatform
            ORDER BY favorite_count DESC, s.rating DESC;
        ''')
    
    favorites = cursor.fetchall()
    
    the_response = make_response(jsonify({"favorites": favorites}))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# Follows/creates new users to following 

@sally.route('/users/<int:userId>/follows', methods=['POST'])
def follow_user(userId):
   
    
    data = request.get_json()
    follower_id = data.get('followerId')
    
    if not follower_id:
        response_data = {'error': 'followerId is required in request body'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 400
        return the_response
    
    # Can't follow yourself
    if follower_id == userId:
        response_data = {'error': 'Users cannot follow themselves'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 400
        return the_response
    
    cursor = db.get_db().cursor()
    
    try:
        # Check that both users exist
        cursor.execute('''SELECT userId FROM users WHERE userId = %s''', (follower_id,))
        if not cursor.fetchone():
            response_data = {'error': 'Follower user not found'}
            the_response = make_response(jsonify(response_data))
            the_response.status_code = 404
            return the_response
        
        cursor.execute('''SELECT userId FROM users WHERE userId = %s''', (userId,))
        if not cursor.fetchone():
            response_data = {'error': 'User to follow not found'}
            the_response = make_response(jsonify(response_data))
            the_response.status_code = 404
            return the_response
        
        # Check if already following
        cursor.execute('''
            SELECT * FROM follows 
            WHERE followerId = %s AND followeeId = %s
        ''', (follower_id, userId))
        
        if cursor.fetchone():
            response_data = {'error': 'User is already following this person'}
            the_response = make_response(jsonify(response_data))
            the_response.status_code = 409  # Conflict
            return the_response
        
        # Create the follow relationship
        cursor.execute('''
            INSERT INTO follows (followerId, followeeId) 
            VALUES (%s, %s)
        ''', (follower_id, userId))
        
        db.get_db().commit()
        
        response_data = {
            'message': 'Successfully followed user',
            'followerId': follower_id,
            'followeeId': userId
        }
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 201  # Created
        
    except Exception as e:
        db.get_db().rollback()
        response_data = {'error': f'Failed to follow user: {str(e)}'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 500
    
    return the_response

#------------------------------------------------------------
# Unfollows/deletes users from following 

@sally.route('/users/<int:userId>/follow', methods=['DELETE'])
def unfollow_user(userId):
    
    data = request.get_json()
    follower_id = data.get('followerId')
    
    if not follower_id:
        response_data = {'error': 'followerId is required in request body'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 400
        return the_response
    
    cursor = db.get_db().cursor()
    
    try:
        # Check that both users exist
        cursor.execute('''SELECT userId FROM users WHERE userId = %s''', (follower_id,))
        if not cursor.fetchone():
            response_data = {'error': 'Follower user not found'}
            the_response = make_response(jsonify(response_data))
            the_response.status_code = 404
            return the_response
        
        cursor.execute('''SELECT userId FROM users WHERE userId = %s''', (userId,))
        if not cursor.fetchone():
            response_data = {'error': 'User not found'}
            the_response = make_response(jsonify(response_data))
            the_response.status_code = 404
            return the_response
        
        # Check if the follow relationship exists
        cursor.execute('''
            SELECT * FROM follows 
            WHERE followerId = %s AND followeeId = %s
        ''', (follower_id, userId))
        
        if not cursor.fetchone():
            response_data = {'error': 'User is not following this person; follower cannot be deleted'}
            the_response = make_response(jsonify(response_data))
            the_response.status_code = 404
            return the_response
        
        # Delete the follow relationship
        cursor.execute('''
            DELETE FROM follows 
            WHERE followerId = %s AND followeeId = %s
        ''', (follower_id, userId))
        
        db.get_db().commit()
        
        response_data = {
            'message': 'Successfully unfollowed user',
            'followerId': follower_id,
            'followeeId': userId
        }
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 200
        
    except Exception as e:
        db.get_db().rollback()
        response_data = {'error': f'Failed to unfollow user: {str(e)}'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 500
    
    return the_response

#------------------------------------------------------------
# Creates a new review for a particular show

@sally.route('/shows/<int:showId>/reviews', methods=['POST'])
def create_review(showId):
    
    data = request.get_json()
    user_id = data.get('userId')
    rating = data.get('rating')
    content = data.get('content')
    
    # Make sure required fields are valid
    if not user_id:
        response_data = {'error': 'userId is required in request body'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 400
        return the_response
    
    if rating is None:
        response_data = {'error': 'rating is required in request body'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 400
        return the_response
    
    # Making sure rating range is correct
    if not (0.0 <= rating <= 5.0):
        response_data = {'error': 'rating must be between 0.0 and 5.0'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 400
        return the_response
    
    cursor = db.get_db().cursor()
    
    try:
        # Check that the show exists
        cursor.execute('''SELECT showID, title FROM shows WHERE showID = %s''', (showId,))
        show = cursor.fetchone()
        
        if not show:
            response_data = {'error': 'Show not found'}
            the_response = make_response(jsonify(response_data))
            the_response.status_code = 404
            return the_response
        
        show_id, show_title = show
        
        # Check that the user exists
        cursor.execute('''SELECT userId FROM users WHERE userId = %s''', (user_id,))
        if not cursor.fetchone():
            response_data = {'error': 'User not found'}
            the_response = make_response(jsonify(response_data))
            the_response.status_code = 404
            return the_response
        
        # Check if user already reviewed this show
        cursor.execute('''
            SELECT writtenrevID FROM reviews 
            WHERE userId = %s AND showID = %s
        ''', (user_id, showId))
        
        if cursor.fetchone():
            response_data = {'error': 'User has already reviewed this show'}
            the_response = make_response(jsonify(response_data))
            the_response.status_code = 409  # Conflict
            return the_response
        
        # Make new review ID 
        cursor.execute('''SELECT MAX(writtenrevID) FROM reviews''')
        max_id = cursor.fetchone()[0]
        new_review_id = (max_id + 1) if max_id else 1
        
        # Create the review
        cursor.execute('''
            INSERT INTO reviews (writtenrevID, userId, showID, rating, content)
            VALUES (%s, %s, %s, %s, %s)
        ''', (new_review_id, user_id, showId, rating, content))
        
        db.get_db().commit()
        
        response_data = {
            'message': f'Review created successfully for "{show_title}"',
            'reviewId': new_review_id,
            'userId': user_id,
            'showId': showId,
            'rating': rating,
            'content': content
        }
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 201  
        
    except Exception as e:
        db.get_db().rollback()
        response_data = {'error': f'Failed to create review: {str(e)}'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 500
    
    return the_response

#------------------------------------------------------------
# Update a review

@sally.route('/reviews/<int:reviewId>', methods=['PUT'])
def update_review(reviewId):
    
    data = request.get_json()
    user_id = data.get('userId')
    rating = data.get('rating')
    content = data.get('content')
    
    # Make sure required fields are valid
    if not user_id:
        response_data = {'error': 'userId is required'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 400
        return the_response
    
    if rating is not None and not (0.0 <= rating <= 5.0):
        response_data = {'error': 'rating must be between 0.0 and 5.0'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 400
        return the_response
    
    cursor = db.get_db().cursor()
    
    try:
        # Check that review exists and belongs to right user
        cursor.execute('''
            SELECT writtenrevID, userId, showID, rating, content 
            FROM reviews 
            WHERE writtenrevID = %s
        ''', (reviewId,))
        
        review = cursor.fetchone()
        
        if not review:
            response_data = {'error': 'Review not found'}
            the_response = make_response(jsonify(response_data))
            the_response.status_code = 404
            return the_response
        
        existing_review_id, existing_user_id, show_id, existing_rating, existing_content = review
        
        if existing_user_id != user_id:
            response_data = {'error': 'You can only update your own reviews'}
            the_response = make_response(jsonify(response_data))
            the_response.status_code = 403  # Forbidden
            return the_response
        
        # Use existing values if not provided in update
        new_rating = rating if rating is not None else existing_rating
        new_content = content if content is not None else existing_content
        
        # Update the review
        cursor.execute('''
            UPDATE reviews 
            SET rating = %s, content = %s
            WHERE writtenrevID = %s AND userId = %s
        ''', (new_rating, new_content, reviewId, user_id))
        
        db.get_db().commit()
        
        response_data = {
            'message': 'Review updated successfully',
            'reviewId': reviewId,
            'userId': user_id,
            'showId': show_id,
            'rating': float(new_rating),
            'content': new_content
        }
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 200
        
    except Exception as e:
        db.get_db().rollback()
        response_data = {'error': f'Failed to update review: {str(e)}'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 500
    
    return the_response


#------------------------------------------------------------
# Delete a review

@sally.route('/reviews/<int:reviewId>', methods=['DELETE'])
def delete_review(reviewId):
    
    data = request.get_json()
    user_id = data.get('userId')
    
    if not user_id:
        response_data = {'error': 'userId is required to verify ownership'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 400
        return the_response
    
    cursor = db.get_db().cursor()
    
    try:
        # Check that review exists and belongs to right user
        cursor.execute('''
            SELECT writtenrevID, userId, showID 
            FROM reviews 
            WHERE writtenrevID = %s
        ''', (reviewId,))
        
        review = cursor.fetchone()
        
        if not review:
            response_data = {'error': 'Review not found'}
            the_response = make_response(jsonify(response_data))
            the_response.status_code = 404
            return the_response
        
        existing_review_id, existing_user_id, show_id = review
        
        if existing_user_id != user_id:
            response_data = {'error': 'You can only delete your own reviews'}
            the_response = make_response(jsonify(response_data))
            the_response.status_code = 403  # Forbidden
            return the_response
        
        # Actually deleting
        cursor.execute('''
            DELETE FROM reviews 
            WHERE writtenrevID = %s AND userId = %s
        ''', (reviewId, user_id))
        
        db.get_db().commit()
        
        response_data = {
            'message': 'Review deleted successfully',
            'reviewId': reviewId,
            'userId': user_id,
            'showId': show_id
        }
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 200
        
    except Exception as e:
        db.get_db().rollback()
        response_data = {'error': f'Failed to delete review: {str(e)}'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 500
    
    return the_response

