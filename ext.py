from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from forms import SearchForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "lizazusuyvarsprogramirebadamadlobeliagvancisromelmaccmasyvelaferiaswavla"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
login_manager = LoginManager(app)

@app.context_processor
def inject_search_form():
    return dict(search_form=SearchForm())   # 👈 renamed from 'form'

