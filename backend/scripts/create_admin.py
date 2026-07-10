from app import create_app


def main():
    app = create_app()
    with app.app_context():
        print("Admin creation script ready.")


if __name__ == "__main__":
    main()
