"""
Insta485 comments (main) view.
"""
import flask
from flask import request
import insta485
import datetime

@insta485.app.route('/comments/', methods=['POST', 'DELETE'])
def update_user_comment():
    #comments: count comments in post associated w/ postid
    operation = flask.request.form['operation']
    currUser = flask.session['username'] #owner
    URL = flask.request.args.get('target')
    connection = insta485.model.get_db() #username is a primary key. 
    #Save the URL from the page we are on, so we can redirect later:
    #Insert Comment
    if operation == 'create':
        postid = flask.request.form['postid']
        text = flask.request.form['text']
        time_stamp = datetime.datetime.utcnow()
        time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO comments (owner, postid, text, created) VALUES ('%s', '%s', '%s', '%s')" % (currUser, postid, text, time_stamp)
        cur = connection.execute(sql)

    #Delete Comment
    elif operation == 'delete':
        commentid = flask.request.form['commentid']
        sql = "SELECT owner FROM comments WHERE commentid='%s'" % (commentid)
        cur = connection.execute(sql)
        commentOwner = cur.fetchone()['owner']
        if currUser != commentOwner:
            flask.abort(403,"Can't delete other user's comment")
        sql = "DELETE FROM comments WHERE commentid='%s' AND owner='%s'" % (commentid, currUser)
        cur = connection.execute(sql)
        #make sure user doesn't delete someone else's comment
        #flask.abort(403,"Can't delete other user's comment")
        #sql = "DELETE "
        #print("deleting...")


    #return updated json object to the page comment was inserted on!
    return flask.redirect(URL)