"""
Insta485 index (main) view.

URLs include: 
"""
from os import abort
import flask
import insta485

@insta485.app.route('/likes/?target=URL', methods=["POST"])
def likes():
    target = flask.request.args.get('target')
    operation = flask.request.form['operation']

    connection = insta485.model.get_db()
    if operation == 'like':
        # Query database
        cur = connection.execute(
            "SELECT owner "
            "FROM likes"
        )

        users = cur.fetchall
        owners = {"likes": users}
        for owner_var in owners
            if TODO is owner_var
                flask.abort(403, "Trying to like a post that was already liked")
        return flask.render_template("likes.html")
    elif operation == 'unlike':
        # Query database
        cur = connection.execute(
            "SELECT owner "
            "FROM likes"
        )

        users = cur.fetchall
        owners = {"likes": users}
        for owner_var in owners
            if TODO is owner_var
                flask.abort(403, "Trying to like a post that was already liked")
        return flask.render_template("likes.html")
