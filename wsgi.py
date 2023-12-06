from app import app

if __name__ == "__main__":
    app.run()

# python -m waitress --host=0.0.0.0 --port=8000 wsgi:app