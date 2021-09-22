"""
Insta485 logout
"""
from os import abort
import flask
import insta485

@insta485.app.route('/logout', methods=["POST"])
def following(followUser):
    currUser = flask.session['username']
    target = flask.request.args.get('target')
    operation = flask.request.form['operation']
    connection = insta485.model.get_db()
    sql = "SELECT f.username1 f.username2 f.created FROM following"
    cur = connection.execute(sql)
    followData = cur.fetchall()
    if operation == 'follow':
        for c_user in followData:
            if c_user['username1'] == currUser:
                for f_user in followData:
                    if followUser == f_user['username2']
                        flask.abort(409, "User cannot follow someone they already follow")
                    
