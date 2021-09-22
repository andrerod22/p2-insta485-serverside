"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import insta485
import arrow

@insta485.app.route('/')
def show_index():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login')) #302

    # Connect to database
    currUser = flask.session['username']
    connection = insta485.model.get_db() #username is a primary key. 

    #Get post data from followers including yourself. And build json object dictionary.
    #Might need datetime to order entries.
    sql = "SELECT postid, filename, owner, created FROM posts WHERE owner='%s' OR owner in (SELECT username2 FROM following WHERE username1='%s') ORDER BY postid DESC" % (currUser, currUser)
    cur = connection.execute(sql)
    postData = cur.fetchall()
    sql = "SELECT c.postid, c.commentid, c.owner, c.text, c.created FROM comments AS c INNER JOIN (SELECT * FROM posts WHERE owner='%s' OR owner in (SELECT username2 FROM following WHERE username1='%s')) AS p ON (p.postid = c.postid)" % (currUser, currUser)
    cur = connection.execute(sql)
    commentData = cur.fetchall()
    sql = "SELECT l.postid, l.likeid, l.owner, l.created FROM likes AS l INNER JOIN (SELECT * FROM posts WHERE owner='%s' OR owner in (SELECT username2 FROM following WHERE username1='%s')) AS p ON (p.postid = l.postid)" % (currUser,currUser)
    cur = connection.execute(sql)
    likeData = cur.fetchall()
    for p in postData:
        commentTuple = []
        likes = 0
        for c in commentData:
            if p["postid"] == c["postid"]:
                commentTuple.append(c)
        for l in likeData:
            if p["postid"] == l["postid"]:
                likes += 1
        p["comments"] = commentTuple
        p["likes"] = likes
    #check if user is trying to add empty comment
    if p["comments"] == False:
        flask.abort(400, "Tried to add empty comment")
    #render template
    context = {"posts": postData}
    return flask.render_template("index.html", **context)

@insta485.app.route('/uploads/<path:filename>', methods=["GET"])
def serve_img(filename):
    return flask.send_from_directory(insta485.app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@insta485.app.route(url_for('likes', target='likes'), methods=["GET"])
def update_likes():
    #setup==========================================
    target = flask.request.args.get('target')
    operation = flask.request.form['operation']
    connection = insta485.model.get_db()
    #load from SQL database=========================
    #SQL data for post
    sql = "SELECT postid, filename, owner, created FROM posts WHERE owner='%s' OR owner in (SELECT username2 FROM following WHERE username1='%s') ORDER BY postid DESC" % (currUser, currUser)
    cur = connection.execute(sql)
    postData = cur.fetchall()
    #SQL data for likes
    sql = "SELECT l.postid, l.likeid, l.owner, l.created FROM likes AS l INNER JOIN (SELECT * FROM posts WHERE owner='%s' OR owner in (SELECT username2 FROM following WHERE username1='%s')) AS p ON (p.postid = l.postid)" % (currUser,currUser)
    cur = connection.execute(sql)
    likeData = cur.fetchall()
    #process the operation from User================
    #if the operation is like
    if operation == 'like':
        if p["postid"] == l["postid"]:
            for l in likeData:
                if l["owner"] == flask.session['username']:
                    flask.abort(409, "User tried to like a post that he already liked")
            p["likes"] += 1
            context = {"posts": postData}
            return flask.render_template("index.html", **context) #render page with unlike button
    #if the operation is unlike
    elif operation == 'unlike':
        if p["postid"] == l["postid"]:
            if l["owner"] == flask.session['username']:
                p["likes"] -= 1
                context = {"posts": postData}
                return flask.render_template("index.html", **context) #render page with like button
            else:
                flask.abort(409, "User tried to unlike a post he did not like prior")

