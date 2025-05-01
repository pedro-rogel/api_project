from app import create_app, db

app = create_app()

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()

    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"]
    )
