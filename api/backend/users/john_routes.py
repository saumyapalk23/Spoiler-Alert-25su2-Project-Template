#------------------------------------------------------------
# Update a comment for a particular review
@john.route('/reviews/<int:reviewId>/comments', methods=['PUT'])
def update_comment(reviewId):
    request_data = request.json
    comment_id = request_data['writtencomID']
    new_content = request_data['content']
    user_id = request_data['userID']

    query = ''' 
        UPDATE comments
        SET content = %s, updatedAt = NOW()
        WHERE writtencomID = %s AND writtenrevID = %s AND userID = %s 
    '''
    data = (new_content, comment_id, reviewId, user_id)

    cursor = db.get_db().cursor()
    cursor.execute(query, data)

    if cursor.rowcount == 0:
        response_data = {'error': 'Comment not found or user not authorized to update this comment'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 404
        return the_response
    
    db.get_db().commit()
    
    response_data = {'message': 'Comment updated successfully'}
    the_response = make_response(jsonify(response_data))
    the_response.status_code = 200
    return the_response 

#------------------------------------------------------------
# Delete a comment for a particular review
@john.route('/reviews/<int:reviewId>/comments', methods=['DELETE'])
def delete_comment(reviewId):
    request_data = request.json
    comment_id = request_data.get('writtencomID')
    user_id = request_data.get('userID')
    
    cursor = db.get_db().cursor()
    cursor.execute('''DELETE FROM Comments 
WHERE writtencomID = %s AND writtenrevID = %s AND userID = %s;
    ''', (comment_id, reviewId, user_id))
    
    if cursor.rowcount == 0:
        response_data = {'error': 'Comment not found or user not authorized to delete this comment'}
        the_response = make_response(jsonify(response_data))
        the_response.status_code = 404
        return the_response

    db.get_db().commit()
    
    response_data = { 'message': 'Comment deleted successfully',
        'writtencomID': comment_id,
        'writtenrevID': reviewId
        }
    the_response = make_response(jsonify(response_data))
    the_response.status_code = 200
    
    return the_response

