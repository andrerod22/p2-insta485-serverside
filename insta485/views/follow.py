"""
Insta485 logout
"""
from os import abort
import flask
import insta485
import datetime

@insta485.app.route('/following/', methods=["POST"])
def follow_redirect():
    currUser = flask.session['username']
    target = flask.request.args.get('target')
    operation = flask.request.form['operation']
    follow_tar = flask.request.form['username']
    connection = insta485.model.get_db()
    sql = "SELECT username2 FROM following WHERE username1='%s' AND username2='%s'" % (currUser, follow_tar)
    cur = connection.execute(sql)
    followData = cur.fetchall()

    if operation == 'follow':
        if followData:
            flask.abort(409, "User cannot follow someone they already follow")
        time_stamp = datetime.datetime.utcnow()
        time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO following (username1, username2, created) VALUES ('%s', '%s', '%s')" % (currUser, follow_tar, time_stamp)
        cur = connection.execute(sql)
    else:
        if followData:
            sql = "DELETE FROM following WHERE username1='%s' AND username2='%s'" % (currUser, follow_tar)
            cur = connection.execute(sql)
        else:
            flask.abort(409, "User cannot unfollow someone they do not follow")
    
    return flask.redirect(target)
        
@insta485.app.route('/users/<user_url_slug>/following/', methods=["GET"])
def show_following(user_url_slug):
    #TODO if followers is successful
    return flask.render_template("following.html", **context)

@insta485.app.route('/users/<user_url_slug>/followers/', methods=["GET"])
def show_followers(user_url_slug):
    #currUser = flask.session['username']
    connection = insta485.model.get_db()
    sql = "SELECT f.username1 f.username2 u.filename FROM following AS f INNER JOIN users AS u ON f.username1=u.username"
    cur = connection.execute(sql)
    followers = cur.fetchall()
    followers[0]["pageUser"] = user_url_slug
    sql = "SELECT * FROM following WHERE username1='%s'" % (user_url_slug)
    cur = connection.execute(sql)
    followers[1] = cur.fetchall()
    context = {"followers": followers}
    return flask.render_template("followers.html", **context)