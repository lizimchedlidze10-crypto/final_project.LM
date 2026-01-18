from ext import db, app
from models import  Product, Comment, User, Destination

with app.app_context():

    db.drop_all()
    db.create_all()
    print("ბაზა წარმატებით შეიქმნა!")

    admin = User(username="adminlizi",email="lizazu10@gmail.com", password="Admin_pass", role="Admin")

    db.session.add(admin)
    db.session.commit()