"""
Insta485 logout
"""
from os import abort
import flask
import insta485

@insta485.app.route('/logout', methods=["POST"])
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('index'))
    #old code
    #session.pop('username', None)
    #flash('You were logged out')
    #return redirect('/accounts/login/')