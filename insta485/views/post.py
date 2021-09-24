import flask
import insta485
import arrow
@insta485.app.route("/posts/<postid_url_slug>/", methods=["GET"])
def show_post(postid_url_slug):
    currUser = flask.session['username']
    connection = insta485.model.get_db() #username is a primary key. 
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
                if(currUser == l["owner"]):
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