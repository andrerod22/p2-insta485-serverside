"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import insta485
import arrow
import pdb

@insta485.app.route('/')
def show_index():
    #flask.session.clear()
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login')) #302

    # Connect to database
    currUser = flask.session['username']
    connection = insta485.model.get_db() #username is a primary key. 

    #Get post data from followers including yourself. And build json object dictionary.
    #Might need datetime to order entries.
    # sql = "SELECT DISTINCT p.postid, p.filename, p.owner, p.created FROM posts AS p, following as f WHERE p.owner = '%s' OR (p.owner = f.username2 AND f.username1 = '%s')" % (currUser, currUser)
    sql = "SELECT postid, filename, owner, created FROM posts WHERE owner='%s' OR owner in (SELECT username2 FROM following WHERE username1='%s') ORDER BY postid DESC" % (currUser, currUser)
    cur = connection.execute(sql)
    postData = cur.fetchall()
    for post in postData:
        post['created'] = arrow.get(post['created'], 'YYYY-MM-DD HH:mm:ss').humanize()
    
    sql = "SELECT c.postid, c.commentid, c.owner, c.text, c.created FROM comments AS c INNER JOIN (SELECT * FROM posts WHERE owner='%s' OR owner in (SELECT username2 FROM following WHERE username1='%s')) AS p ON (p.postid = c.postid)" % (currUser, currUser)
    cur = connection.execute(sql)
    commentData = cur.fetchall()
    sql = "SELECT l.postid, l.likeid, l.owner, l.created FROM likes AS l INNER JOIN (SELECT * FROM posts WHERE owner='%s' OR owner in (SELECT username2 FROM following WHERE username1='%s')) AS p ON (p.postid = l.postid)" % (currUser,currUser)
    cur = connection.execute(sql)
    likeData = cur.fetchall()
    for p in postData:
        commentTuple = []
        likes = 0
        liked = False
        for c in commentData:
            if p["postid"] == c["postid"]:
                commentTuple.append(c)
        for l in likeData:
            if p["postid"] == l["postid"]:
                if(currUser == l["owner"]):
                    liked = True
                likes += 1
        p["comments"] = commentTuple
        p["likes"] = likes
        p["liked"] = liked

        #add a bool to tell if the user liked a post p. 
    # breakpoint()    
        
    context = {"posts": postData}
    
    return flask.render_template("index.html", **context)

@insta485.app.route('/uploads/<path:filename>', methods=["GET"])
def serve_img(filename):
    return flask.send_from_directory(insta485.app.config['UPLOAD_FOLDER'], filename, as_attachment=True)