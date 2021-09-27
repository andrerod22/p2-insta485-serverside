"""
Insta485 comment (main) view.

URLs include:
N/a
"""
import flask
from flask import request
import insta485
import datetime


@insta485.app.route('/comments/', methods=['POST'])
def update_user_comment():
    """Increment Comment Table with New Like."""
    operation = flask.request.form['operation']
    currUser = flask.session['username']
    target = flask.request.args.get('target')
    if target is None:
        URL = '/'
    elif '/posts/' in target:
        URL = target
    elif '/posts/' not in target:
        URL = '/posts/' + str(target) + '/'
    else:
        URL = '/'
    connection = insta485.model.get_db()
    if operation == 'create':
        postid = flask.request.form['postid']
        text = flask.request.form['text']
        time_stamp = datetime.datetime.utcnow()
        time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        sql = """INSERT INTO comments
         (owner, postid, text, created) VALUES ('%s', '%s', '%s', '%s')
         """ % (currUser, postid, text, time_stamp)
        cur = connection.execute(sql)

    elif operation == 'delete':
        commentid = flask.request.form['commentid']
        sql = "SELECT owner FROM comments WHERE commentid='%s'" % (commentid)
        cur = connection.execute(sql)
        commentOwner = cur.fetchone()
        commentOwner = commentOwner['owner']

        if currUser != commentOwner:
            flask.abort(403, "Can't delete other user's comment")
        sql = """DELETE FROM comments WHERE commentid='%s'
         AND owner='%s'""" % (commentid, currUser)
        cur = connection.execute(sql)

    if target == '/':
        return flask.redirect('/')
    return flask.redirect(URL)
