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
from os import abort
import flask
import insta485

@insta485.app.route('/accounts', methods=["POST"])
def account_redirect():
    #Gets form data from login.html
    operation = flask.request.form['operation']
    username = flask.request.form['username']
    password = flask.request.form['password']
    target = flask.request.args.get('target')

    if not username or not password:
        abort(400, "Username or Password field was empty")
    if operation == 'login': 
        connection = insta485.model.get_db()
        params = (username, password)
        cur = connection.execute("SELECT * FROM users WHERE username = '%s' AND password = '%s'" % params)
        user = cur.fetchone()
        if user is None:
            flask.abort(403, "Invalid Username and Password Combination")
        flask.session['username'] = username
        if target == '': #Depending on the target, we want to redirect them to different places. 
            return flask.redirect("/", code=302)

    #TODO Other operations like account create, edit, etc. Refer to spec. 

@insta485.app.route('/accounts/login', methods=["GET"])
def show_login():
    return flask.render_template("login.html")
