# application.py for implementing a tree-buy webapp
#
# Maurice Kingma
#
#
# python program for page routes tree.mauricekingma.nl

from config import *

# error handlers
@app.errorhandler(400)
def bad_request(e):
    raise Exception("Bad request")
    message = "Probleem met verzoek."
    return render_template('error.html', status_code="400", message=message), 400

@app.errorhandler(404)
def page_not_found(e):
    message = "De pagina die je probeert te bezoeken bestaat niet."
    return render_template('error.html', status_code="404", message=message), 404

@app.errorhandler(403)
def forbidden(e):
    message = "De pagina die je probeert te bezoeken is niet voor jou toegankelijk."
    return render_template('error.html', status_code=403, message=message), 403

@app.errorhandler(410)
def gone(e):
    message = "De pagina die je probeert te bezoeken bestaat niet meer."
    return render_template('error.html', status_code=410, message=message), 410

@app.errorhandler(500)
def server_error(e):
    # note that we set the 404 status explicitly
    message = "Server-fout."
    return render_template('error.html', status_code=500, message=message), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/onsverhaal')
def story():
    return render_template('story.html')

@app.route('/nieuws')
def news():
    return render_template('news.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/koopnboom')
def shop():
    return render_template('shop.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')
