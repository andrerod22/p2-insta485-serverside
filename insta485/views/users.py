import flask
import insta485

@insta485.app.route('/users/<user_slug>/', methods=["GET"])
def show_user(user_slug):

    
    #Connect to database and fully render this page. 
    return flask.render_template("user.html")