from app import create_app
from app.extensions import db
import app.models

app = create_app()


@app.cli.command("create-db")
def create_db():
    db.create_all()
    print("Database tables created.")
