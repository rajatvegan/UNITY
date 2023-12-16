from app import app

if __name__ == "__main__":
    from waitress import serve
    serve(app, host='0.0.0.0', port=8000)


# python -m waitress --host=0.0.0.0 --port=8000 wsgi:app