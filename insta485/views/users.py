import flask
import insta485

@insta485.app.route('/users/<user_slug>/', methods=["GET"])
def show_user(user_slug):
    currUser = flask.session['username']
    sql = "SELECT * From users WHERE username='%s'" % (currUser)
    connection = insta485.model.get_db()
    cur = connection.execute(sql)
    userData = cur.fetchall()
    sql = "SELECT COUNT(postid) FROM posts"
    cur = connection.execute(sql)
    userData['numPosts'] = cur.fetchall()
    sql = "SELECT COUNT(username2) FROM following WHERE username1='%s'" % (currUser)
    cur = connection.execute(sql)
    userData['numFollowing'] = cur.fetchall()
    sql = "SELECT COUNT(username1) FROM following WHERE username2='%s'" % (currUser)
    cur = connection.execute(sql)
    userData['numFollowers'] = cur.fetchall()
    #ssql = "SELECT fullname FROM users WHERE username='%s'" % (currUser)
    #cur = connection.execute(sql)
    #userData['fullname'] = cur.fetchall()
    context = {"UserData": userData} 
    return flask.render_template("user.html", **context)