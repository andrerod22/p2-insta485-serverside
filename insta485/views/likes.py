"""
Insta485 like (main) view.

URLs include:

"""
import datetime
import flask
import insta485


@insta485.app.route("/likes/", methods=["POST"])
def update_likes():
    """Update likes in DB."""
    # setup==========================================
    target = flask.request.args.get('target')
    operation = flask.request.form['operation']
    postid = flask.request.form['postid']
    curr_user = flask.session['username']  # owner
    connection = insta485.model.get_db()  # username is a primary key.
    # load from SQL database=========================
    # SQL data for likes
    sql = """SELECT owner FROM likes WHERE postid='%s'
    AND owner='%s'""" % (postid, curr_user)
    cur = connection.execute(sql)
    like_data = cur.fetchall()
    # process the operation from User================
    # if the operation is like
    if operation == 'like':
        if like_data:
            flask.abort(409, "User tried to like a post he has already liked")
        time_stamp = datetime.datetime.utcnow()
        time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        sql = """INSERT INTO likes (owner, postid, created)
        VALUES ('%s', '%s', '%s')""" % (curr_user, postid, time_stamp)
        cur = connection.execute(sql)
    # if the operation is unlike
    elif operation == 'unlike':
        if like_data:
            sql = """DELETE FROM likes WHERE owner='%s'
            AND postid='%s'""" % (curr_user, postid)
            cur = connection.execute(sql)
        else:
            flask.abort(
                        409,
                        "User tried to unlike a post he did not like prior")
        # if target != '/':
            # return flask.redirect(URL)
    return flask.redirect(target)
