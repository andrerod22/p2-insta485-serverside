"""
Insta485 index (main) view.

URLs include: 
"""
from os import abort
import flask
import insta485

@insta485.app.route('/logout', methods=["POST"])
def logout():
    session.pop('user', None)
    #flash('You were logged out')
    return redirect('/accounts/login/')
