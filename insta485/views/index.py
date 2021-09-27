"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
from flask.wrappers import Response
import insta485
import arrow
import pdb


@insta485.app.route('/')
def show_index():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))  # 302
    # Connect to database
    currUser = flask.session['username']
    connection = insta485.model.get_db()  # username is a primary key.
    # Get post data from followers including yourself.
    # And build json object dictionary.
    # Might need datetime to order entries.
    sql = """SELECT postid, filename, owner, created
    FROM posts WHERE owner='%s' OR owner in
    (SELECT username2 FROM following WHERE username1='%s')
    ORDER BY postid DESC""" % (currUser, currUser)
    cur = connection.execute(sql)
    postData = cur.fetchall()
    for post in postData:
        post['created'] = arrow.get(
                                    post['created'],
                                    'YYYY-MM-DD HH:mm:ss').humanize()
    # sql comment
    sql = """SELECT c.postid, c.commentid, c.owner, c.text, c.created
    FROM comments AS c INNER JOIN (SELECT * FROM posts
    WHERE owner='%s' OR owner in (SELECT username2
    FROM following WHERE username1='%s')) AS p
    ON (p.postid = c.postid)""" % (currUser, currUser)
    cur = connection.execute(sql)
    commentData = cur.fetchall()
    # sql post
    sql = """SELECT l.postid, l.likeid, l.owner, l.created
    FROM likes AS l INNER JOIN (SELECT * FROM posts WHERE owner='%s'
    OR owner in (SELECT username2 FROM following
    WHERE username1='%s')) AS p
    ON (p.postid = l.postid)""" % (currUser, currUser)
    cur = connection.execute(sql)
    likeData = cur.fetchall()
    # sql users
    sql = """SELECT u.filename, u.username FROM users
    AS u INNER JOIN (SELECT * FROM posts WHERE owner='%s'
    OR owner in (SELECT username2 FROM following
    WHERE username1='%s')) AS p
    ON (p.owner = u.username)""" % (currUser, currUser)
    cur = connection.execute(sql)
    userPhotos = cur.fetchall()
    for p in postData:
        userPhoto = None
        commentTuple = []
        likes = 0
        liked = False
        for c in commentData:
            if p["postid"] == c["postid"]:
                commentTuple.append(c)
        for li in likeData:
            if p["postid"] == li["postid"]:
                if(currUser == li["owner"]):
                    liked = True
                likes += 1
        for u in userPhotos:
            if p["owner"] == u["username"]:
                userPhoto = u["filename"]

        p["comments"] = commentTuple
        p["likes"] = likes
        p["liked"] = liked
        p["owner_img_url"] = userPhoto
        # add a bool to tell if the user liked a post p.
    context = {"posts": postData}
    return flask.render_template("index.html", **context)


@insta485.app.route('/uploads/<path:filename>', methods=["GET"])
def serve_img(filename):
    """Dynamically Serve Images."""
    if 'username' not in flask.session:
        return flask.abort(403)
    return flask.send_from_directory(
                                    insta485.app.config['UPLOAD_FOLDER'],
                                    filename, as_attachment=True)
