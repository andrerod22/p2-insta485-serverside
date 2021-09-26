from insta485.views.users import show_user
import flask
from flask.helpers import url_for
import insta485
import arrow
import uuid
import pathlib
import datetime

@insta485.app.route("/posts/<postid_url_slug>/", methods=["GET"])

def show_post(postid_url_slug):
    #breakpoint()
    if 'username' not in flask.session:
        return flask.redirect(url_for('show_login'))
    curr_user = flask.session['username']
    connection = insta485.model.get_db()
    sql = "SELECT postid, filename, owner, created FROM posts WHERE postid='%s'" % postid_url_slug
    cur = connection.execute(sql)
    postData = cur.fetchall()
    for post in postData:
        post['created'] = arrow.get(post['created'], 'YYYY-MM-DD HH:mm:ss').humanize()
    sql = "SELECT c.postid, c.commentid, c.owner, c.text, c.created FROM comments AS c INNER JOIN (SELECT * FROM posts WHERE postid='%s') AS p ON (p.postid = c.postid)" % postid_url_slug
    cur = connection.execute(sql)
    commentData = cur.fetchall()
    sql = "SELECT l.postid, l.likeid, l.owner, l.created FROM likes AS l INNER JOIN (SELECT * FROM posts WHERE postid='%s') AS p ON (p.postid = l.postid)" % postid_url_slug
    cur = connection.execute(sql)
    likeData = cur.fetchall()
    sql = "SELECT u.filename, u.username FROM users AS u INNER JOIN (SELECT * FROM posts WHERE postid='%s') AS p ON (p.owner = u.username)" % postid_url_slug
    cur = connection.execute(sql)
    userPhotos = cur.fetchall()
    for p in postData:
        commentTuple = []
        likes = 0
        liked = False
        for c in commentData:
            if p["postid"] == c["postid"]:
                commentTuple.append(c)
        for l in likeData:
            if p["postid"] == l["postid"]:
                if(curr_user == l["owner"]):
                    liked = True
                likes += 1
        for u in userPhotos:
            if p["owner"] == u["username"]:
                userPhoto = u["filename"]

        p["owner_img_url"] = userPhoto
        p["comments"] = commentTuple
        p["likes"] = likes
        p["liked"] = liked
    context = {"posts": postData}
    return flask.render_template("post.html", **context)

@insta485.app.route('/posts/', methods=["POST"])
def post_redirect():
    operation = flask.request.form['operation']
    curr_user = flask.session['username'] #owner
    URL = flask.request.args.get('target')
    if operation == 'delete':
        postid = flask.request.form['postid']
        connection = insta485.model.get_db() #username is a primary key. 
        sql = "SELECT owner FROM posts WHERE postid='%s'" % (postid)
        cur = connection.execute(sql)
        post_owner = cur.fetchone()
        post_owner = post_owner['owner']
        if curr_user != post_owner:
            flask.abort(403,"Can't delete other user's post")
        cur = connection.execute("SELECT filename FROM posts WHERE postid='%s' AND owner = '%s'" % (postid, curr_user))
        target_post = cur.fetchall()
        filePath = insta485.app.config['UPLOAD_FOLDER']/target_post[0]['filename']
        filePath.unlink()
        sql = "DELETE FROM posts WHERE postid='%s' AND owner='%s'" % (postid, curr_user)
        cur = connection.execute(sql)
        return flask.redirect(url_for('show_user', user_slug = curr_user))
    elif operation == 'create':
        URL =  url_for('show_user', user_slug =  curr_user)
        fileobj = flask.request.files["file"]
        filename = fileobj.filename
        uuid_basename = "{stem}{suffix}".format(
            stem=uuid.uuid4().hex,
            suffix=pathlib.Path(filename).suffix
            )
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        connection = insta485.model.get_db()
        time_stamp = datetime.datetime.utcnow()
        time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        params = (uuid_basename, curr_user, time_stamp)
        cur = connection.execute("INSERT INTO posts(filename,owner,created) VALUES('%s','%s','%s')" % params)
    return flask.redirect(URL)