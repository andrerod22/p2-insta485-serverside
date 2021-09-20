"""
Insta485 index (main) view.

URLs include:
/login/
/logout/
/create/
/edit/
/password/
/ immediate redirection to where the user originally wanted to go. 
"""
import flask
import insta485

@insta485.app.route('/accounts', methods=["POST"])
def account_redirect():
    target = flask.request.args.get('target')
    return flask.redirect(target)

@insta485.app.route('/accounts/login', methods=["GET"])
def show_login():
    return flask.render_template("login.html")
