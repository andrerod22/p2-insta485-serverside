"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import insta485
import datetime

@insta485.app.route("/likes/", methods=["POST"])
def update_likes():
    #setup==========================================
    target = flask.request.args.get('target')
    #URL = '/posts/' + target + '/'
    #breakpoint()
    operation = flask.request.form['operation']
    postid = flask.request.form['postid']
    currUser = flask.session['username'] #owner
    connection = insta485.model.get_db() #username is a primary key.
    #load from SQL database=========================
    #SQL data for likes
    sql = "SELECT owner FROM likes WHERE postid='%s' AND owner='%s'" % (postid, currUser)
    cur = connection.execute(sql)
    likeData = cur.fetchall()
    #process the operation from User================
    #if the operation is like
    if operation == 'like':
        if likeData:
            flask.abort(409, "User tried to like a post he has already liked")
        time_stamp = datetime.datetime.utcnow()
        time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO likes (owner, postid, created) VALUES ('%s', '%s', '%s')" % (currUser, postid, time_stamp)
        cur = connection.execute(sql)
    #if the operation is unlike
    elif operation == 'unlike':
        if likeData:
            sql = "DELETE FROM likes WHERE owner='%s' AND postid='%s'" % (currUser, postid)
            cur = connection.execute(sql)
        else:
            flask.abort(409, "User tried to unlike a post he did not like prior")
        #if target != '/':
            #return flask.redirect(URL)
    return flask.redirect(target)