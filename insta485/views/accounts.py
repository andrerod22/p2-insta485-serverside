"""
Insta485 index (main) view.

URLs include:
/login/
/logout/
/create/
/edit/
/password/
/ (not allowed, should throw error 405, since only POST request is allowed)
"""
import flask
import insta485


@insta485.app.route('/login', methods=["GET","POST"])
def show_login():
    if flask.request.method == "POST":
        #after they hit submit on login form
        pass

    return flask.render_template("login.html")
