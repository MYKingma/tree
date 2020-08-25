# application.py for implementing a tree-buy webapp
#
# Maurice Kingma
#
#
# python program for page routes tree.mauricekingma.nl

from config import *

@app.route('/')
def hello_world():
    return 'Hello, World!'
