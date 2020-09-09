# application.py for implementing a tree-buy webapp
#
# Maurice Kingma
#
#
# python program for page routes tree.mauricekingma.nl

from config import *

# decorators
def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            # check if user is logged in and has active roles
            if not current_user.is_authenticated:
               return login_manager.unauthorized()
            roles = current_user.get_user_roles()
            if role not in roles:
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    # message and route for unathorized users
    return redirect(url_for('login'))

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

# redirect routes
@app.route('/loguit')
def logout():
    # log out user
    logout_user()
    flash("Successvol uitgelogd", 'success')
    return redirect(url_for('index'))

# page routes
@app.route('/')
def index():
    post = Post.query.filter_by(title="Verhaal").first()
    lastupdate = Update.query.order_by(Update.date.desc()).first()


    # order = Order(firstname="Maurice", lastname="Kingma", email="mauricekingma@me.com")
    # db.session.add(order)
    # db.session.commit()
    #
    # product = Product.query.first()
    # order.add_product(product, 6)
    # db.session.commit()

    # msg = Message("Bevestig je e-mailadres om je account te activeren", recipients=['mauricekingma@me.com'])
    # msg.html = "Hallooooooooo"
    # mail.send(msg)




    return render_template('index.html', post=post, lastupdate=lastupdate)

@app.route('/onsverhaal')
def story():
    post = Post.query.filter_by(title="Verhaal").first()
    return render_template('story.html', post=post)

@app.route('/updates')
def updates():
    updates = Update.query.order_by(Update.date).all()
    return render_template('updates.html', updates=updates)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/koopnboom', methods=['GET', 'POST'])
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/dashboard/updates', methods=["GET", "POST"])
def dashupdates():
    if request.method == "GET":
        updates = Update.query.order_by(Update.date).all()
        return render_template('dashupdates.html', updates=updates)
    newupdate = Update()
    db.session.add(newupdate)
    db.session.commit()
    return redirect(url_for('createupdate', update_id=newupdate.id))

@app.route('/dashboard/updates/opstellen/<update_id>', methods=["GET", "POST"])
def createupdate(update_id):
    update = Update.query.filter_by(id=update_id).first()

    if request.method == "GET":
        return render_template('createupdate.html', update=update)

    files = request.files.getlist('file')
    update.title = request.form.get('title')
    update.date = datetime.datetime.strptime(request.form.get('date'), '%d-%m-%y')
    update.short = request.form.get('short')
    update.body = request.form.get('editor1')
    db.session.commit()

    for file in files:
        if file and allowed_file(file.filename):
            try:
                repo.create_file("static/img/uploads/updates/" + str(update.id) + '/' + file.filename, "file upload", file.read(), branch='master')
            except:
                flash(f"Fout bij uploaden {file.filename}, naam bestaat al in uploadmap bij deze update.", "danger")
                return render_template('createupdate.html', update=update)

    for image in request.form.get('images').split(','):
        if update.images == None:
            update.images = image
        elif image not in update.images.split(','):
            update.images = update.images + ',' + image


    db.session.commit()

    if request.form.get('action') == "save":
        flash("Wijzigingen opgeslagen", "success")
        return render_template('createupdate.html', update=update)

    if request.form.get('action') == "delete":
        if update.images:
            for image in update.images.split(','):
                contents = repo.get_contents("static/img/uploads/updates/" + str(update.id) + '/' + image)
                repo.delete_file("static/img/uploads/updates/" + str(update.id) + '/' + image, "delete uploaded file", contents.sha)
        db.session.delete(update)
        db.session.commit()
        flash("Update verwijderd", "success")
        return redirect(url_for('dashupdates'))


@app.route('/dashboard/posts', methods=["GET", "POST"])
def dashposts():
    if request.method == "GET":
        posts = Post.query.order_by(Post.id).all()
        return render_template('dashposts.html', posts=posts)
    newpost = Post()
    db.session.add(newpost)
    db.session.commit()
    return redirect(url_for('createpost', post_id=newpost.id))

@app.route('/dashboard/posts/opstellen/<post_id>', methods=["GET", "POST"])
def createpost(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if request.method == "GET":
        return render_template('createpost.html', post=post)

    files = request.files.getlist('file')
    post.title = request.form.get('title')
    post.short = request.form.get('short')
    post.body = request.form.get('editor1')
    db.session.commit()
    for file in files:
        if file and allowed_file(file.filename):
            try:
                repo.create_file("static/img/uploads/posts/" + str(post.id) + '/' + file.filename, "file upload", file.read(), branch='master')
            except:
                flash(f"Fout bij uploaden {file.filename}, naam bestaat al in uploadmap bij deze post.", "danger")
                return render_template('createpost.html', post=post)


    for image in request.form.get('images').split(','):
        if post.images == None:
            post.images = image
        elif image not in post.images.split(','):
            post.images = post.images + ',' + image

    db.session.commit()

    if request.form.get('action') == "save":
        flash("Wijzigingen opgeslagen", "success")
        return render_template('createpost.html', post=post)

    if request.form.get('action') == "delete":
        if post.images:
            for image in post.images.split(','):
                contents = repo.get_contents("static/img/uploads/posts/" + str(post.id) + '/' + image)
                repo.delete_file("static/img/uploads/posts/" + str(post.id) + '/' + image, "delete uploaded file", contents.sha)
        db.session.delete(post)
        db.session.commit()
        flash("Post verwijderd", "success")
        return redirect(url_for('posts'))

@app.route('/dashboard/winkel', methods=["GET", "POST"])
def dashshop():
    if request.method == "GET":
        products = Product.query.all()
        orders = Order.query.order_by(Order.date.desc()).all()
        return render_template('dashshop.html', products=products, orders=orders)

    if request.form.get('action') == "newproduct":
        return redirect(url_for('createproduct', product_id=0))

    if request.form.get('action') == "paycode":
        paycode = int(request.form.get('paycode'))
        if paycode <= 10000:
            flash(f"Foutieve Tikkie code: {paycode}", "warning")
            return redirect(url_for('dashshop'))
        paycode = paycode - 10000
        order = Order.query.get(paycode)
        if not order:
            flash(f"Bestelling niet gevonden", "warning")
            return redirect(url_for('dashshop'))
        if not order.sendpayment:
            flash("Van deze bestelling is nog geen betaallink verzonden, verstuur eerst de betaallink. Hierna kan je de betaling verwerken.", "warning")
            return redirect(url_for('dashshop'))

        order.paid = True
        db.session.commit()
        flash(f"Betaling van de bestelling van {order.firstname} is verwerkt", "success")
        return redirect(url_for('dashshop'))

@app.route('/dashboard/winkel/stuurtikkie', methods=["GET", "POST"])
def sendpayment():
    if request.method == "GET":
        orders = Order.query.filter_by(sendpayment=False).order_by(Order.date.desc()).all()
        return render_template('sendpayment.html', orders=orders)

    checked = request.form.getlist('checked')
    for check in checked:
        order = Order.query.get(check)
        order.sendpayment = True
        db.session.commit()
    flash("bestellingen verwerkt", "success")
    return redirect(url_for('sendpayment'))

@app.route('/dashboard/productwijzigen/<product_id>', methods=["GET", "POST"])
def createproduct(product_id):
    product = None
    if not product_id == 0:
        product = Product.query.get(product_id)

    if request.method == "GET":
        return render_template('createproduct.html', product=product)
    name = request.form.get('name')
    description = request.form.get('description')
    stock = request.form.get('stock')
    price = float(request.form.get('price'))
    if not product:
        product = Product(name=name, description=description, stock=stock, price=price)
        db.session.add(product)
        db.session.commit()
        flash(f"Product {product.name} toegevoegd", "success")
        return render_template('createproduct.html', product=product)
    else:
        product.name = name
        product.description = description
        product.stock = stock
        product.price = price
        db.session.commit()
        if request.form.get('action') == "save":
            flash("Wijzigingen opgeslagen", "succes")
            return render_template('createproduct.html', product=product)
        if request.form.get('action') == "delete":
            db.session.delete(product)
            db.session.commit()
            flash("Product verwijderd", "succes")
            return redirect(url_for('dashshop'))

@app.route('/dashboard/product/faq/<product_id>', methods=["GET", "POST"])
def dashfaqs(product_id):
    product = Product.query.get(product_id)
    if request.method == "GET":
        return render_template('dashfaqs.html', product=product)

    return redirect(url_for('createfaq', faq_id=0, product_id=product_id))

@app.route('/dashboard/product/faq/opstellen/<faq_id>/<product_id>', methods=["GET", "POST"])
def createfaq(faq_id, product_id):
    faq = None
    product = Product.query.get(product_id)
    if not faq_id == 0:
        faq = FAQ.query.get(faq_id)
    if request.method == "GET":
        return render_template('createfaq.html', faq=faq, product=product)

    question = request.form.get('question')
    answer = request.form.get('answer')

    if not faq:
        faq = FAQ(question=question, answer=answer, product_id=product.id)
        db.session.add(faq)
        db.session.commit()
        flash(f"FAQ toegevoegd", "success")
        return render_template('createfaq.html', faq=faq, product=product)
    else:
        faq.question = question
        faq.answer = answer
        db.session.commit()
        if request.form.get('action') == "save":
            flash("Wijzigingen opgeslagen", "succes")
            return render_template('createfaq.html', faq=faq, product=product)
        if request.form.get('action') == "delete":
            db.session.delete(faq)
            db.session.commit()
            flash("FAQ verwijderd", "success")
            return redirect(url_for('dashfaqs', product_id=product.id))


@app.route('/update/<update_id>')
def update(update_id):
    update = Update.query.get(update_id)
    return render_template('update.html', update=update)

@app.route('/blog/<post_id>')
def post(post_id):
    post = Post.query.get(post_id)
    otherposts = Post.query.filter(Post.id!=post_id).first()
    return render_template('post.html', post=post, otherposts=otherposts)

@app.route('/test')
def test():
    return redirect(url_for('index'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user:
        hpassword = blake2b(password.encode()).hexdigest()
        if user.password == hpassword:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Wachtwoord niet correct", "warning")
    else:
        flash(f"Geen gebruiker gevonden met gebruikersnaam {username}.", "warning")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
@role_required('Owner')
def dashboard():
    return render_template('dashboard.html')
