from flask import render_template, redirect, flash
from werkzeug.security import check_password_hash

from forms import RegisterForm, ProductForm, LoginForm, DestinationForm, SearchForm
from models import Product, Comment, User, Destination
from ext import app, db
from flask_login import login_user, logout_user, login_required, current_user
import os





@app.route("/")
def home():

    products = Product.query.all()
    destinations = Destination.query.all()
    return render_template("index.html", products=products, destinations=destinations)



@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data, email=form.email.data)

        db.session.add(new_user)
        db.session.commit()

        flash("თქვენ წარმატებით დარეგისტრირდით,  გაიარეთ ავტორიზაცია", "success")
        return redirect("/login")

    return render_template("register.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = None
        email_input = form.email.data.strip()
        username_input = form.username.data.strip()

        if email_input:
            user = User.query.filter_by(email=email_input).first()
        elif username_input:
            user = User.query.filter_by(username=username_input).first()

        if not user:
            flash("მოხდა შეცდომა: მომხმარებელი ვერ მოიძებნა", "danger")
            return render_template("login.html", form=form)

        if user.check_password(form.password.data):
            login_user(user)
            flash("თქვენ წარმატებით გაიარეთ ავტორიზაცია", "success")
            return redirect("/")
        else:
            flash("მოხდა შეცდომა: პაროლი არასწორია", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()

    return redirect("/")


@app.route("/createproduct", methods=["GET", "POST"])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data)

        image = form.image.data
        img_location = os.path.join(app.root_path, "static", "images", image.filename)
        image.save(img_location)

        new_product.image = image.filename

        db.session.add(new_product)
        db.session.commit()

        flash("პროდუქტი წარმატებით დაემატა", "success")
        return redirect("/")

    return render_template("createproduct.html", form=form)




@app.route("/edit_product/<int:product_id>", methods=["POST", "GET"])
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name, price=product.price)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data

        db.session.commit()

        flash("პროდუქტი წარმატებით განახლდა!", "success")
        return redirect("/")

    return render_template("createproduct.html", form=form)


@app.route("/delete/<int:product_id>")
def delete_product(product_id):
    product = Product.query.get(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("პროდუქტი წარმატებით წაიშალა", "danger")
    return redirect("/")

@app.route("/detailed/<int:product_id>")
def detailed_product(product_id):
    product = Product.query.get(product_id)
    comments = Comment.query.filter(Comment.product_id == product_id)
    return render_template("detailed.html", product=product, comments=comments)


@app.route("/detailed-destination/<int:destination_id>")
def detailed_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if not destination:
        return "Destination not found", 404
    comments = Comment.query.filter_by(destinations_id=destination_id).all()
    return render_template( "detailed_destination.html", destination=destination, comments=comments )



import os
from werkzeug.utils import secure_filename
from flask import current_app, render_template, redirect, flash

@app.route("/edit_destination/<int:destination_id>", methods=["GET", "POST"])
@login_required
def edit_destination(destination_id):
    destination = Destination.query.get_or_404(destination_id)
    form = DestinationForm(obj=destination)

    if form.validate_on_submit():
        destination.name = form.name.data
        destination.price = form.price.data

        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)

            images_folder = os.path.join(current_app.root_path, "static", "images")
            os.makedirs(images_folder, exist_ok=True)
            file.save(os.path.join(images_folder, filename))


            destination.image = f"/static/images/{filename}"

        db.session.commit()
        flash("destination წარმატებით განახლდა!", "success")
        return redirect("/")

    return render_template("add_destination.html", form=form, destination=destination)




@app.route("/contact", methods=["POST", "GET"])
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/profiles/<int:profile_id>")
def profile(profile_id):
    return render_template("profile.html", user=profile[profile_id])

import os
from werkzeug.utils import secure_filename
from flask import current_app

@app.route("/adddestination", methods=["GET", "POST"])
@login_required
def add_destination():
    form = DestinationForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = secure_filename(image.filename)

        images_folder = os.path.join(current_app.root_path, "static", "images")
        os.makedirs(images_folder, exist_ok=True)
        image.save(os.path.join(images_folder, filename))

        new_destination = Destination(
            name=form.name.data,
            price=form.price.data,
            image=f"/static/images/{filename}"
        )

        db.session.add(new_destination)
        db.session.commit()

        flash("destination added", "success")
        return redirect("/")

    return render_template("add_destination.html", form=form)


@app.route("/delete_destination/<int:destination_id>")
@login_required
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)

    if not destination:
        flash("Destination not found.", "danger")
        return redirect("/")

    db.session.delete(destination)
    db.session.commit()

    flash("Destination წარმატებით წაიშალა", "success")
    return redirect("/")




@app.route("/products", methods=["GET", "POST"])
def products():
    products = Product.query.all()
    return render_template("product.html", products=products)



@app.route("/search", methods=["GET", "POST"])
def search():
    form = SearchForm()
    products = []
    destinations = []

    if form.validate_on_submit():
        q = form.query.data

        products = Product.query.filter(
            Product.name.ilike(f"%{q}%")
        ).all()

        destinations = Destination.query.filter(
            Destination.name.ilike(f"%{q}%")
        ).all()

    return render_template(
        "search.html", form=form, products=products, destinations=destinations )
