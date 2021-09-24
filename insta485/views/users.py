import flask
import insta485

@insta485.app.route('/users/<user_slug>/', methods=["GET"])
def show_user(user_slug):
    currUser = flask.session['username']
    connection = insta485.model.get_db()
    sql = "SELECT COUNT(postid) FROM posts"
    cur = connection.execute(sql)
    userData['numPosts'] = cur.fetchall()
    sql = "SELECT COUNT(username2) FROM following WHERE username1='%s'" % (currUser)
    cur = connection.execute(sql)
    userData['numFollowing'] = cur.fetchall()
    sql = "SELECT COUNT(username1) FROM following WHERE username2='%s'" % (currUser)
    cur = connection.execute(sql)
    userData['numFollowers'] = cur.fetchall()
    sql = "SELECT fullname FROM users WHERE username='%s'" % (currUser)
    cur = connection.execute(sql)
    userData['fullname'] = cur.fetchall()    
    #Connect to database and fully render this page.
    context = {"UserData": userData} 
    return flask.render_template("user.html", **context)