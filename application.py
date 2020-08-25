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

@app.route('/test')
def test():
    msg = Message(f"Ontvangstbevestiging informatieaanvraag voor {name}", recipients=['mauricekingma@me.com'])
    msg.html = 'Hello, World!'
    job = queue.enqueue('task.send_mail', msg)
    return 'Hello, World!'
