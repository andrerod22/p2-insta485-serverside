"""
Insta485 logout
"""
from os import abort
import flask
import insta485

@insta485.app.route('', methods=["POST"])
def follow_redirect():
    currUser = flask.session['username']
    target = flask.request.args.get('target')
    operation = flask.request.form['operation']
    follow_tar = flask.request.form['username']
    connection = insta485.model.get_db()
    sql = "SELECT username2 FROM following WHERE username1='%s' AND username='%s'" % (currUser, follow_tar)
    cur = connection.execute(sql)
    followData = cur.fetchall()

    if operation == 'follow':
        if followData:
            flask.abort(409, "User cannot follow someone they already follow")
        time_stamp = datetime.datetime.utcnow()
        time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO following (username1, username2, created) VALUES '%s', '%s', '%s'" % (currUser, follow_tar, time_stamp)
        cur = connection.execute(sql)
    else:
        if followData:
            sql = "DELETE FROM following WHERE username1='%s' AND username2='%s'" % (currUser, follow_tar)
            cur = connection.execute(sql)
        else:
            flask.abort(409, "User cannot unfollow someone they do not follow")
        

                    
