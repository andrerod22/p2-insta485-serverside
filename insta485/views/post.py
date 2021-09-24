import flask
import insta485
import arrow
import pdb
@insta485.app.route("/posts/<postid_url_slug>/", methods=["GET"])
def show_post(postid_url_slug):
    currUser = flask.session['username']
    connection = insta485.model.get_db() #username is a primary key. 
    sql = "SELECT postid, filename, owner, created FROM posts (WHERE owner='%s' OR owner in (SELECT username2 FROM following WHERE username1='%s') AND postid = postid_url_slug) ORDER BY postid DESC" % (currUser, currUser)
    cur = connection.execute(sql)
    postData = cur.fetchall()
    for post in postData:
        post['created'] = arrow.get(post['created'], 'YYYY-MM-DD HH:mm:ss').humanize()
    context = {"posts": postData}
    return flask.render_template("post.html", **context)