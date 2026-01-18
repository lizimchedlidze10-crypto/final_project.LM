from ext import app, db


if __name__ == "__main__":
    import routes
    app.run(debug=True , port =5005)


with app.app_context():
    db.create_all()
