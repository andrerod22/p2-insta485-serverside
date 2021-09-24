import flask
import insta485


@insta485.app.route("/posts/<postid_url_slug>", methods=["GET"])
def show_post(postid_url_slug):
    currUser = flask.session['username']
    connection = insta485.model.get_db() #username is a primary key. 
    return flask.render_template("post.html", **context)