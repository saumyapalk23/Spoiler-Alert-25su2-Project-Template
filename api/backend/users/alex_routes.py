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
# Get all customers from the system
@alex.route('/shows', methods=['GET'])
def get_szn():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT *
FROM shows
WHERE season <= 3
ORDER BY season ASC
LIMIT 5;
    ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
