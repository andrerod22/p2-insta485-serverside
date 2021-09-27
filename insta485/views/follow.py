"""
Insta485 logout
"""
import flask
from werkzeug.utils import redirect
import insta485
import datetime


@insta485.app.route('/following/', methods=["POST"])
def follow_redirect():
    if 'username' not in flask.session:
        return flask.redirect("show_login")
    currUser = flask.session['username']
    target = flask.request.args.get('target')
    operation = flask.request.form['operation']
    follow_tar = flask.request.form['username']
    connection = insta485.model.get_db()
    # SELECT the person we are following called follow_tar=username1
    sql = """SELECT username2 FROM following WHERE username1='%s'
    AND username2='%s'""" % (currUser, follow_tar)
    cur = connection.execute(sql)
    followData = cur.fetchall()

    if operation == 'follow':
        if followData:
            flask.abort(409, "User cannot follow someone they already follow")
        time_stamp = datetime.datetime.utcnow()
        time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        sql = """INSERT INTO following (username1, username2, created)
        VALUES ('%s', '%s', '%s')""" % (currUser, follow_tar, time_stamp)
        cur = connection.execute(sql)
    else:
        if followData:
            sql = """DELETE FROM following WHERE username1='%s'
            AND username2='%s'""" % (currUser, follow_tar)
            cur = connection.execute(sql)
        else:
            flask.abort(409, "User cannot unfollow someone they do not follow")
    return flask.redirect(target)


@insta485.app.route('/users/<user_url_slug>/following/', methods=["GET"])
def show_following(user_url_slug):
    if 'username' not in flask.session:
        return redirect('show_login')
    connection = insta485.model.get_db()
    # get list of followers
    currUser = flask.session['username']  # session user
    # user_url_slug -> username2
    sql = """SELECT filename, username
    FROM users WHERE username in
    (SELECT username2 FROM following
    WHERE username1 = '%s')""" % user_url_slug
    cur = connection.execute(sql)
    following = cur.fetchall()
    # Get list of following of users the person is following
    sql = "SELECT username2 FROM following WHERE username1 = '%s'" % currUser
    cur = connection.execute(sql)
    followList = cur.fetchall()
    # if entry is not empty
    followList = [follow['username2'] for follow in followList]
    for following_var in following:
        if following_var['username'] not in followList:
            following_var['following_back'] = False
        else:
            following_var['following_back'] = True
        following_var['user_slug'] = user_url_slug
    context = {"following": following}
    return flask.render_template("following.html", **context)


# DO NOT TOUCH
@insta485.app.route('/users/<user_url_slug>/followers/', methods=["GET"])
def show_followers(user_url_slug):
    if 'username' not in flask.session:
        return redirect('show_login')
    connection = insta485.model.get_db()
    # get list of followers
    currUser = flask.session['username']
    sql = """SELECT filename, username FROM users
    WHERE username in (SELECT username1 FROM following
    WHERE username2 = '%s')""" % user_url_slug
    cur = connection.execute(sql)
    followers = cur.fetchall()
    # Get list of following of users the person is following
    sql = "SELECT username2 FROM following WHERE username1 = '%s'" % currUser
    cur = connection.execute(sql)
    followList = cur.fetchall()
    followList = [follow['username2'] for follow in followList]
    for follower in followers:
        if follower['username'] not in followList:
            follower['following_back'] = False
        else:
            follower['following_back'] = True
        follower['user_slug'] = user_url_slug
    context = {"followers": followers}
    # breakpoint()
    return flask.render_template("followers.html", **context)
