"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import arrow
import insta485


@insta485.app.route('/')
def show_index():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))  # 302
    # Connect to database
    curr_user = flask.session['username']
    connection = insta485.model.get_db()  # username is a primary key.
    # Get post data from followers including yourself.
    # And build json object dictionary.
    # Might need datetime to order entries.
    sql = """SELECT postid, filename, owner, created
    FROM posts WHERE owner='%s' OR owner in
    (SELECT username2 FROM following WHERE username1='%s')
    ORDER BY postid DESC""" % (curr_user, curr_user)
    cur = connection.execute(sql)
    post_data = cur.fetchall()
    for post in post_data:
        post['created'] = arrow.get(
                                    post['created'],
                                    'YYYY-MM-DD HH:mm:ss').humanize()
    # sql comment
    # add a bool to tell if the user liked a post p.
    generate_json_obj(post_data)
    context = {"posts": post_data}
    return flask.render_template("index.html", **context)


@insta485.app.route('/uploads/<path:filename>', methods=["GET"])
def serve_img(filename):
    """Dynamically Serve Images."""
    if 'username' not in flask.session:
        return flask.abort(403)
    return flask.send_from_directory(
                                    insta485.app.config['UPLOAD_FOLDER'],
                                    filename, as_attachment=True)


def generate_json_obj(post_data):
    """Generate Index Json Object."""
    connection = insta485.model.get_db()
    sql = """SELECT c.postid, c.commentid, c.owner, c.text, c.created
    FROM comments AS c INNER JOIN (SELECT * FROM posts
    WHERE owner='%s' OR owner in (SELECT username2
    FROM following WHERE username1='%s')) AS p
    ON (p.postid = c.postid)
    """ % (flask.session['username'], flask.session['username'])
    cur = connection.execute(sql)
    comment_data = cur.fetchall()
    # sql post
    sql = """SELECT l.postid, l.likeid, l.owner, l.created
    FROM likes AS l INNER JOIN (SELECT * FROM posts WHERE owner='%s'
    OR owner in (SELECT username2 FROM following
    WHERE username1='%s')) AS p
    ON (p.postid = l.postid)
    """ % (flask.session['username'], flask.session['username'])
    cur = connection.execute(sql)
    like_data = cur.fetchall()
    # sql users
    sql = """SELECT u.filename, u.username FROM users
    AS u INNER JOIN (SELECT * FROM posts WHERE owner='%s'
    OR owner in (SELECT username2 FROM following
    WHERE username1='%s')) AS p
    ON (p.owner = u.username)
    """ % (flask.session['username'], flask.session['username'])
    cur = connection.execute(sql)
    user_photos = cur.fetchall()
    for p_d in post_data:
        user_photo = None
        comment_tuple = []
        likes = 0
        liked = False
        for c_d in comment_data:
            if p_d["postid"] == c_d["postid"]:
                comment_tuple.append(c_d)
        for l_i in like_data:
            if p_d["postid"] == l_i["postid"]:
                if flask.session['username'] == l_i["owner"]:
                    liked = True
                likes += 1
        for u_p in user_photos:
            if p_d["owner"] == u_p["username"]:
                user_photo = u_p["filename"]
        p_d["comments"] = comment_tuple
        p_d["likes"] = likes
        p_d["liked"] = liked
        p_d["owner_img_url"] = user_photo
    return post_data
