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
    user = User.query.filter_by(firstname="Jozien").first()
    background = user.website_img
    videolink = user.youtube_link
    videolength = user.youtube_length
    lastposts = Post.query.filter(Post.title!="Verhaal").filter(Post.title!="Algemene voorwaarden").order_by(Post.date.desc()).limit(3).all()
    return render_template('index.html', post=post, background=background, lastposts=lastposts, videolink=videolink, videolength=videolength)

@app.route('/blog')
def updates():
    updates = Update.query.order_by(Update.date.desc()).all()
    return render_template('updates.html', updates=updates)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/winkel', methods=['GET', 'POST'])
def shop():
    if request.method == "GET":
        products = Product.query.all()
        return render_template('shop.html', products=products)

    orderstring = request.form.get('orderdict')

    return redirect(url_for('confirm', orderstring=orderstring))

@app.route('/winkel/bevestigen/<orderstring>', methods=['GET', 'POST'])
def confirm(orderstring):
    if request.method == "GET":
        orderdict = ast.literal_eval(orderstring)
        order = {}
        total = 0.00
        for key, value in orderdict.items():
            item = Product.query.get(key)
            order[str(value) + 'x ' + item.name] = "€ " + str("{:.2f}".format(int(value) * int(item.price)))
            total = "{:.2f}".format(total + (int(value) * int(item.price)))
        return render_template('confirm.html', orderstring=orderstring, order=order, total=total)

    orderdict = ast.literal_eval(orderstring)
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')

    neworder = Order(firstname=firstname, lastname=lastname, email=email)
    db.session.add(neworder)
    db.session.commit()
    for key, value in orderdict.items():
        product = Product.query.get(key)
        neworder.add_product(product, value)
    db.session.commit()
    message = f"Bedankt voor uw bestelling bij Studio 't Landje. In deze e-mail ontvangt u een overzicht van uw bestelling. Zodra deze is verwerkt ontvangt u een aparte e-mail met de betaalinstructies. Verwerken van de bestelling duurt doorgaans een dag."
    sender = "Studio 't Landje"
    name = neworder.firstname
    msg = Message("Bevestiging van uw bestelling bij Studio 't Landje", recipients=[neworder.email])
    msg.html = render_template('emailbase.html', name=name, message=message, sender=sender, order=neworder)
    job = queue.enqueue('task.send_mail_tree', msg)
    return render_template('confirmed.html', order=neworder)

@app.route('/faq/<product_id>/<product_name>')
def faq(product_id, product_name):
    product = Product.query.get(product_id)
    return render_template('faq.html', product=product)

@app.route('/dashboard/tijdlijn', methods=["GET", "POST"])
@login_required
@role_required('Owner')
def dashupdates():
    if request.method == "GET":
        updates = Update.query.order_by(Update.date).all()
        return render_template('dashupdates.html', updates=updates)
    newupdate = Update()
    db.session.add(newupdate)
    db.session.commit()
    return redirect(url_for('createupdate', update_id=newupdate.id))

@app.route('/dashboard/tijdlijn/opstellen/<update_id>', methods=["GET", "POST"])
@login_required
@role_required('Owner')
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
                try:
                    contents = repo.get_contents("static/img/uploads/updates/" + str(update.id) + '/' + image)
                    repo.delete_file("static/img/uploads/updates/" + str(update.id) + '/' + image, "delete uploaded file", contents.sha)
                except:
                    message = f"Er is een fout ontstaan bij het verwijderen van een geuploade afbeelding, namelijk {file.filename} van update {update.id}. Je kunt op onderstaande link klikken om naar de GitHub pagina te gaan en het bestand handmatig te verwijderen."
                    linktext = "Klik hier om naar de GitHub map te gaan"
                    sender = "Het brein van de website"
                    link = "https://github.com/MYKingma/tree/tree/master/static/img/uploads/updates/" + str(update.id)
                    msg = Message("Fout bij verwijderen afbeelding van GitHub", recipients=["mauricekingma@me.com"])
                    msg.html = render_template('emailbase.html', name="Maurice", link=link, message=message, linktext=linktext, sender=sender)
                    job = queue.enqueue('task.send_mail_tree', msg)

        db.session.delete(update)
        db.session.commit()
        flash("Update verwijderd", "success")
        return redirect(url_for('dashupdates'))

@app.route('/dashboard/blog', methods=["GET", "POST"])
@login_required
@role_required('Owner')
def dashposts():
    if request.method == "GET":
        posts = Post.query.order_by(Post.id).all()
        return render_template('dashposts.html', posts=posts)
    newpost = Post()
    db.session.add(newpost)
    db.session.commit()
    return redirect(url_for('createpost', post_id=newpost.id))

@app.route('/dashboard/blog/opstellen/<post_id>', methods=["GET", "POST"])
@login_required
@role_required('Owner')
def createpost(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if request.method == "GET":
        return render_template('createpost.html', post=post)

    files = request.files.getlist('file')
    post.title = request.form.get('title')
    post.short = request.form.get('short')
    post.body = request.form.get('editor1')
    if request.form.get('date'):
        post.date = datetime.datetime.strptime(request.form.get('date'), '%d-%m-%y %I:%M')
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
                try:
                    contents = repo.get_contents("static/img/uploads/posts/" + str(post.id) + '/' + image)
                    repo.delete_file("static/img/uploads/posts/" + str(post.id) + '/' + image, "delete uploaded file", contents.sha)
                except:
                    message = f"Er is een fout ontstaan bij het verwijderen van een geuploade afbeelding, namelijk {file.filename} van post {post.id}. Je kunt op onderstaande link klikken om naar de GitHub pagina te gaan en het bestand handmatig te verwijderen."
                    linktext = "Klik hier om naar de GitHub map te gaan"
                    sender = "Het brein van de website"
                    link = "https://github.com/MYKingma/tree/tree/master/static/img/uploads/posts/" + str(post.id)
                    msg = Message("Fout bij verwijderen afbeelding van GitHub", recipients=["mauricekingma@me.com"])
                    msg.html = render_template('emailbase.html', name="Maurice", link=link, message=message, linktext=linktext, sender=sender)
                    job = queue.enqueue('task.send_mail_tree', msg)

        db.session.delete(post)
        db.session.commit()
        flash("Post verwijderd", "success")
        return redirect(url_for('dashposts'))

@app.route('/dashboard/winkel', methods=["GET", "POST"])
@login_required
@role_required('Owner')
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
        message = "De betaling van uw bestelling bij Studio 't Landje is verwerkt, u hoeft verder niets meer te doen. Hieronder de details van uw afgeronde bestelling."
        sender = "Studio 't Landje"
        msg = Message("Betaling verwerkt van uw bestelling bij Studio 't Landje", recipients=[order.email])
        msg.html = render_template('emailbase.html', name=order.firstname, message=message, order=order, sender=sender)
        job = queue.enqueue('task.send_mail_tree', msg)
        flash(f"Betaling van de bestelling van {order.firstname} is verwerkt", "success")
        return redirect(url_for('dashshop'))

@app.route('/dashboard/winkel/stuurlink', methods=["GET", "POST"])
@login_required
@role_required('Owner')
def sendpayment():
    if request.method == "GET":
        orders = Order.query.filter_by(sendpayment=False).order_by(Order.date.desc()).all()
        return render_template('sendpayment.html', orders=orders)

    order_id = request.form.get('order')
    order = Order.query.get(order_id)
    link = str(request.form.get('link')).split(' ')
    for part in link:
        if part.startswith('https://'):
            link = str(part)
            break
    message = "Uw bestelling bij Studio 't Landje is verwerkt en er is een betaallink voor u aangemaakt. Klik op onderstaande link om uw bestelling af te ronden."
    footer = f"Werkt de link niet? Kopieer dan de volgende link en plak deze in uw browser: {link}"
    linktext = "Klik hier om via Tikkie te betalen"
    sender = "Studio 't Landje"
    msg = Message("Betaalverzoek voor uw bestelling bij Studio 't Landje", recipients=[order.email])
    msg.html = render_template('emailbase.html', name=order.firstname, link=link, message=message, order=order, linktext=linktext, sender=sender, footer=footer)
    job = queue.enqueue('task.send_mail_tree', msg)
    flash("Betaallink verstuurd", "success")
    order.sendpayment = True
    db.session.commit()
    return redirect(url_for('sendpayment'))

@app.route('/dashboard/productwijzigen/<product_id>', methods=["GET", "POST"])
@login_required
@role_required('Owner')
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
    file = request.files.get('file')
    image = file.filename if file else None

    if not product:
        product = Product(name=name, description=description, stock=stock, price=price, image=image)
        oldfile = None
        db.session.add(product)
        db.session.commit()
    else:
        product.name = name
        product.description = description
        product.stock = stock
        product.price = price
        if image:
            oldfile = product.image
            product.image = image
        db.session.commit()

    if file and allowed_file(file.filename):
        try:
            repo.create_file("static/img/uploads/products/" + str(product.id) + "/" + file.filename, "file upload", file.read(), branch='master')
        except:
            flash(f"Fout bij uploaden {file.filename}, naam bestaat al in uploadmap.", "danger")
            return redirect(url_for('createproduct', product_id=0))

        if oldfile:
            try:
                contents = repo.get_contents("static/img/uploads/products/" + str(product.id) + "/" + oldfile)
                repo.delete_file("static/img/uploads/products/" + str(product.id) + "/" + oldfile, "delete uploaded file", contents.sha)
            except:
                message = f"Er is een fout ontstaan bij het verwijderen van een geuploade afbeelding, namelijk {file.filename} als foto bij {product.name}. Je kunt op onderstaande link klikken om naar de GitHub pagina te gaan en het bestand handmatig te verwijderen."
                linktext = "Klik hier om naar de GitHub map te gaan"
                sender = "Het brein van de website"
                link = "https://github.com/MYKingma/tree/tree/master/static/img/uploads/products/" + str(product.id)
                msg = Message("Fout bij verwijderen afbeelding van GitHub", recipients=["mauricekingma@me.com"])
                msg.html = render_template('emailbase.html', name="Maurice", link=link, message=message, linktext=linktext, sender=sender)
                job = queue.enqueue('task.send_mail_tree', msg)

    if request.form.get('action') == "save":
        flash("Wijzigingen opgeslagen", "succes")
        return render_template('createproduct.html', product=product)
    if request.form.get('action') == "delete":
        if product.image:
            try:
                contents = repo.get_contents("static/img/uploads/products/" + str(product.id) + "/" + oldfile)
                repo.delete_file("static/img/uploads/products/" + str(product.id) + "/" + oldfile, "delete uploaded file", contents.sha)
            except:
                message = f"Er is een fout ontstaan bij het verwijderen van een geuploade afbeelding, namelijk {file.filename} als foto bij {product.name}. Je kunt op onderstaande link klikken om naar de GitHub pagina te gaan en het bestand handmatig te verwijderen."
                linktext = "Klik hier om naar de GitHub map te gaan"
                sender = "Het brein van de website"
                link = "https://github.com/MYKingma/tree/tree/master/static/img/uploads/products/" + str(product.id)
                msg = Message("Fout bij verwijderen afbeelding van GitHub", recipients=["mauricekingma@me.com"])
                msg.html = render_template('emailbase.html', name="Maurice", link=link, message=message, linktext=linktext, sender=sender)
                job = queue.enqueue('task.send_mail_tree', msg)
        db.session.delete(product)
        db.session.commit()
        flash("Product verwijderd", "succes")
        return redirect(url_for('dashshop'))

@app.route('/dashboard/product/faq/<product_id>', methods=["GET", "POST"])
@login_required
@role_required('Owner')
def dashfaqs(product_id):
    product = Product.query.get(product_id)
    if request.method == "GET":
        return render_template('dashfaqs.html', product=product)

    return redirect(url_for('createfaq', faq_id=0, product_id=product_id))

@app.route('/dashboard/product/faq/opstellen/<faq_id>/<product_id>', methods=["GET", "POST"])
@login_required
@role_required('Owner')
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
    if post_id == "0":
        post = Post.query.filter(Post.title!="Verhaal").filter(Post.title!="Algemene voorwaarden").order_by(Post.date.desc()).first()
    else:
        post = Post.query.get(post_id)
    otherposts = Post.query.filter(Post.id!=post_id).filter(Post.title!="Verhaal").filter(Post.title!="Algemene voorwaarden").filter(Post.id!=post.id).order_by(Post.date.desc()).all()
    return render_template('post.html', post=post, otherposts=otherposts)

@app.route('/algemenevoorwaarden')
def policy():
    post = Post.query.filter(Post.title=="Algemene voorwaarden").first()
    return render_template('post.html', post=post)

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

@app.route('/dashboard/website', methods=["GET", "POST"])
@login_required
@role_required('Owner')
def dashwebsite():
    if request.method == "GET":
        return render_template('dashwebsite.html')

    if request.form.get('action') == "password":
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash("Wachtwoorden komen niet overeen", "warning")
        else:
            # hash password
            password = blake2b(password1.encode()).hexdigest()
            user = User.query.get(current_user.id)
            user.password = password
            db.session.commit()
            flash("Wachtwoord gewijzigd", "success")

    if request.form.get('action') == "img":
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            try:
                repo.create_file("static/img/" + file.filename, "file upload", file.read(), branch='master')
            except:
                flash(f"Fout bij uploaden {file.filename}, naam bestaat al in uploadmap.", "danger")
                return render_template('dashwebsite.html')

            user = User.query.filter_by(firstname="Jozien").first()
            oldfile = user.website_img
            user.website_img = file.filename
            db.session.commit()
            try:
                contents = repo.get_contents("static/img/" + oldfile)
                repo.delete_file("static/img/" + oldfile, "delete uploaded file", contents.sha)
            except:
                message = f"Er is een fout ontstaan bij het verwijderen van een geuploade afbeelding, namelijk {file.filename} als oude achtergrond. Je kunt op onderstaande link klikken om naar de GitHub pagina te gaan en het bestand handmatig te verwijderen."
                linktext = "Klik hier om naar de GitHub map te gaan"
                sender = "Het brein van de website"
                link = "https://github.com/MYKingma/tree/tree/master/static/img"
                msg = Message("Fout bij verwijderen afbeelding van GitHub", recipients=["mauricekingma@me.com"])
                msg.html = render_template('emailbase.html', name="Maurice", link=link, message=message, linktext=linktext, sender=sender)
                job = queue.enqueue('task.send_mail_tree', msg)
            flash("Nieuwe homepagina afbeelding opgeslagen", "success")

    if request.form.get('action') == "video":
        user = User.query.filter_by(firstname="Jozien").first()
        videolink = request.form.get('videolink')
        if not videolink:
            user.youtube_link = None
            user.youtube_length = None
            db.session.commit()
            flash("Video verwijderd", "success")
            return(redirect(url_for('dashwebsite')))
        videolength = request.form.get('videolength')
        if videolink and not videolength:
            flash("Geen afspeelduur opgegeven", "warning")
            return(redirect(url_for('dashwebsite')))
        user.youtube_link = videolink.split('?v=')[1]
        user.youtube_length = int(videolength) + 5
        db.session.commit()
        flash("Youtube video toegevoegd", "success")

    return render_template('dashwebsite.html')

@app.route('/dashboard/wachtwoordvergeten')
def forgot():
    user = User.query.filter_by(username="Jozien").first()
    # generate token reset password email
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    token = serializer.dumps(user.firstname, salt=app.config['SECURITY_PASSWORD_SALT'])
    message = "Onderstaande link brengt je naar de pagina om je wachtwoord opnieuw in te stellen. Deze link is 1 uur geldig, zodra deze is verlopen moet je een nieuwe link aanvragen via de website."
    linktext = "Klik hier om je wachtwoord te resetten"
    sender = "Het brein van de website"
    link = request.url_root + "dashboard/wachtwoordherstellen/" + token
    msg = Message("Reset je wachtwoord", recipients=["mauricekingma@me.com"])
    msg.html = render_template('emailbase.html', name=user.firstname, link=link, message=message, linktext=linktext, sender=sender)

    job = queue.enqueue('task.send_mail_tree', msg)

    flash("Link verstuurd naar jozien@studio-t-landje.nl voor het resetten van het emailadres", "success")
    return redirect(url_for('login'))

@app.route('/dashboard/wachtwoordherstellen/<token>')
def resetpass(token):
    # configure serializer and check token (3600s is 1h)
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    expiration = 3600
    try:
        firstname = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except:
        flash("Link verlopen, vraag een nieuwe link aan", "warning")
        return redirect(url_for('login'))
    user = User.query.filter_by(firstname=firstname).first()
    login_user(user)
    flash("Maak via onderstaand formulier een nieuw wachtwoord aan", "info")
    return redirect(url_for('dashwebsite'))
