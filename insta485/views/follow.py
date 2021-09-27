"""
Insta485 like (main) view.

URLs include:

"""
import datetime
import flask
from werkzeug.utils import redirect
import insta485


@insta485.app.route('/following/', methods=["POST"])
def follow_redirect():
    """Redirect follow traffic."""
    if 'username' not in flask.session:
        return flask.redirect("show_login")
    curr_user = flask.session['username']
    target = flask.request.args.get('target')
    operation = flask.request.form['operation']
    follow_tar = flask.request.form['username']
    connection = insta485.model.get_db()
    # SELECT the person we are following called follow_tar=username1
    sql = """SELECT username2 FROM following WHERE username1='%s'
    AND username2='%s'""" % (curr_user, follow_tar)
    cur = connection.execute(sql)
    follow_data = cur.fetchall()

    if operation == 'follow':
        if follow_data:
            flask.abort(409, "User cannot follow someone they already follow")
        time_stamp = datetime.datetime.utcnow()
        time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        sql = """INSERT INTO following (username1, username2, created)
        VALUES ('%s', '%s', '%s')""" % (curr_user, follow_tar, time_stamp)
        cur = connection.execute(sql)
    else:
        if follow_data:
            sql = """DELETE FROM following WHERE username1='%s'
            AND username2='%s'""" % (curr_user, follow_tar)
            cur = connection.execute(sql)
        else:
            flask.abort(409, "User cannot unfollow someone they do not follow")
    return flask.redirect(target)


@insta485.app.route('/users/<user_url_slug>/following/', methods=["GET"])
def show_following(user_url_slug):
    """Render the following template."""
    if 'username' not in flask.session:
        return redirect('show_login')
    connection = insta485.model.get_db()
    # get list of followers
    curr_user = flask.session['username']  # session user
    # user_url_slug -> username2
    sql = """SELECT filename, username
    FROM users WHERE username in
    (SELECT username2 FROM following
    WHERE username1 = '%s')""" % user_url_slug
    cur = connection.execute(sql)
    following = cur.fetchall()
    # Get list of following of users the person is following
    sql = "SELECT username2 FROM following WHERE username1 = '%s'" % curr_user
    cur = connection.execute(sql)
    follow_list = cur.fetchall()
    # if entry is not empty
    follow_list = [follow['username2'] for follow in follow_list]
    for following_var in following:
        if following_var['username'] not in follow_list:
            following_var['following_back'] = False
        else:
            following_var['following_back'] = True
        following_var['user_slug'] = user_url_slug
    context = {"following": following}
    return flask.render_template("following.html", **context)


# DO NOT TOUCH
@insta485.app.route('/users/<user_url_slug>/followers/', methods=["GET"])
def show_followers(user_url_slug):
    """Render the followers template."""
    if 'username' not in flask.session:
        return redirect('show_login')
    connection = insta485.model.get_db()
    # get list of followers
    curr_user = flask.session['username']
    sql = """SELECT filename, username FROM users
    WHERE username in (SELECT username1 FROM following
    WHERE username2 = '%s')""" % user_url_slug
    cur = connection.execute(sql)
    followers = cur.fetchall()
    # Get list of following of users the person is following
    sql = "SELECT username2 FROM following WHERE username1 = '%s'" % curr_user
    cur = connection.execute(sql)
    follow_list = cur.fetchall()
    follow_list = [follow['username2'] for follow in follow_list]
    for follower in followers:
        if follower['username'] not in follow_list:
            follower['following_back'] = False
        else:
            follower['following_back'] = True
        follower['user_slug'] = user_url_slug
    context = {"followers": followers}
    # breakpoint()
    return flask.render_template("followers.html", **context)
