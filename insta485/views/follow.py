"""
Insta485 index (main) view.

URLs include: 
"""
from os import abort
import flask
import insta485

@insta485.app.route('/likes/?target=URL', methods=["POST"])
    
