"""File for all post related functionaliity."""
import insta485
import arrow
import uuid
import pathlib
import datetime
import flask
# from insta485.views.users import show_user
from flask.helpers import url_for


def show_post_helper(
                    post_data, comment_data,
                    like_data, curr_user, user_photos):
    """Show posts helper (looping)."""
    for post in post_data:
        comment_tuple = []
        likes = 0
        liked = False
        for comment in comment_data:
            if post["postid"] == comment["postid"]:
                comment_tuple.append(comment)
        for like in like_data:
            if post["postid"] == like["postid"]:
                if curr_user == like["owner"]:
                    liked = True
                likes += 1
        for user in user_photos:
            if post["owner"] == user["username"]:
                user_photo = user["filename"]

        post["owner_img_url"] = user_photo
        post["comments"] = comment_tuple
        post["likes"] = likes
        post["liked"] = liked
    context = {"posts": post_data}
    return flask.render_template("post.html", **context)


@insta485.app.route("/posts/<postid_url_slug>/", methods=["GET"])
def show_post(postid_url_slug):
    """Render Post Template."""
    if 'username' not in flask.session:
        return flask.redirect(url_for('show_login'))
    curr_user = flask.session['username']
    connection = insta485.model.get_db()
    # sql = """SELECT postid, filename, owner, created
    # FROM posts WHERE postid='%s'""" % postid_url_slug
    cur = connection.execute(
                            """SELECT postid, filename, owner, created
                            FROM posts
                            WHERE postid='%s'""" % postid_url_slug)
    post_data = cur.fetchall()
    for post in post_data:
        temp_post = post['created']
        post['created'] = arrow.get(
                                    temp_post,
                                    'YYYY-MM-DD HH:mm:ss').humanize()
    # sql = """SELECT c.postid, c.commentid, c.owner,
    # c.text, c.created FROM comments
    # AS c INNER JOIN (SELECT * FROM posts WHERE postid='%s')
    # AS p ON (p.postid = c.postid)""" % postid_url_slug
    cur = connection.execute(
                            """SELECT c.postid, c.commentid, c.owner,
                            c.text, c.created FROM comments
                            AS c INNER JOIN (SELECT * FROM posts
                            WHERE postid='%s')
                            AS p ON (p.postid = c.postid)"""
                            % postid_url_slug)
    comment_data = cur.fetchall()
    sql = """SELECT l.postid, l.likeid, l.owner, l.created
     FROM likes AS l INNER JOIN (SELECT * FROM posts WHERE postid='%s')
      AS p ON (p.postid = l.postid)""" % postid_url_slug
    cur = connection.execute(sql)
    like_data = cur.fetchall()
    sql = """SELECT u.filename, u.username FROM users AS u INNER JOIN
     (SELECT * FROM posts WHERE postid='%s') AS p ON
      (p.owner = u.username)""" % postid_url_slug
    cur = connection.execute(sql)
    user_photos = cur.fetchall()
    return show_post_helper(
                            post_data, comment_data, like_data,
                            curr_user, user_photos)


@insta485.app.route('/posts/', methods=["POST"])
def post_redirect():
    """Redirects all post traffic."""
    operation = flask.request.form['operation']
    curr_user = flask.session['username']
    url_var = flask.request.args.get('target')
    if operation == 'delete':
        postid = flask.request.form['postid']
        connection = insta485.model.get_db()
        sql = "SELECT owner FROM posts WHERE postid='%s'" % (postid)
        cur = connection.execute(sql)
        post_owner = cur.fetchone()
        post_owner = post_owner['owner']
        if curr_user != post_owner:
            flask.abort(403, "Can't delete other user's post")
        cur = connection.execute("""SELECT filename FROM posts
        WHERE postid='%s' AND owner = '%s'""" % (postid, curr_user))
        target_post = cur.fetchall()
        folder = insta485.app.config['UPLOAD_FOLDER']
        file_path = folder/target_post[0]['filename']
        file_path.unlink()
        sql = """DELETE FROM posts WHERE postid='%s' AND
             owner='%s'""" % (postid, curr_user)
        cur = connection.execute(sql)
        return flask.redirect(url_for('show_user', user_slug=curr_user))
    elif operation == 'create':
        url_var = url_for('show_user', user_slug=curr_user)
        fileobj = flask.request.files["file"]
        if fileobj is None:
            flask.abort(400)
        # filename = fileobj.filename
        uuid_basename = "{stem}{suffix}".format(
            stem=uuid.uuid4().hex,
            suffix=pathlib.Path(fileobj.filename).suffix
            )
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        connection = insta485.model.get_db()
        time_stamp = datetime.datetime.utcnow()
        time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        # params = (uuid_basename, curr_user, time_stamp)
        cur = connection.execute("""INSERT INTO posts(filename,owner,created)
         VALUES('%s','%s','%s')""" % (uuid_basename, curr_user, time_stamp))
    return flask.redirect(url_var)
