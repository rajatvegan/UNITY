from flask import Flask, render_template, jsonify, request, send_file
from database import  add_data_to_db,  execute_query1, execute_query2, configure_mongo, get_mongo_collection
import os

app = Flask(__name__,static_url_path='/static')

@app.route("/")
def home():
    try:
        iframe_api_key = os.getenv('IFRAME_API_KEY')
        notebook_api_key = os.getenv('NOTEBOOK_API_KEY')
        return render_template('home.html', iframe_api_key=iframe_api_key, notebook_api_key=notebook_api_key)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/signup")
def signup():
    try:
        return render_template('signup.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/form")
def form():
    try:
        return render_template('form.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/resume")
def resume():
    try:
        return render_template('resume.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/view')
def view():
    try:
        q1 = "SELECT COUNT(*) FROM form"
        q2 = "SELECT COUNT(*) FROM form WHERE city='kanpur'"
        q = "SELECT * FROM form"

        total_count = execute_query1(q1)
        city_count = execute_query1(q2)
        data_result = execute_query2(q)
    
        configure_mongo(app)
        collection = get_mongo_collection()
        results = collection.aggregate([{ '$project': { '_id': 0 } }])
        documents = [document for document in results]
        return render_template("view.html", documents=documents, total_count=total_count, peoples=data_result, kanpur_count=city_count)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/form", methods=['POST'])
def submit_form():
    try:
        data = request.form
        add_data_to_db(data)

        country=request.form.get('country')
        city=request.form.get('city')
        interests=request.form.get('interests')
        interests_conditions = " AND ".join([f"interests LIKE '%{interest}%'" for interest in interests])

        q = f"SELECT COUNT(*) FROM form"
        q1 = f"SELECT COUNT(*) FROM form WHERE country = '{country}'"
        q2 = f"SELECT COUNT(*) FROM form WHERE city = '{city}'"
        q3 = f"SELECT name, email, social_media, interests FROM form WHERE city = '{city}' AND privacy_ask = 'yes' AND friend_ask='yes' "
        q4 = f"SELECT name, email, social_media, interests FROM form WHERE country = '{country}' AND privacy_ask = 'yes' AND friend_ask='yes' "
        q5 = f"SELECT name, email, social_media, city, interests FROM form WHERE {interests_conditions} AND privacy_ask = 'yes' AND friend_ask='yes' "

        r = execute_query1(q)
        r1 = execute_query1(q1)
        r2 = execute_query1(q2)
        r3 = execute_query2(q3)
        r4 = execute_query2(q4)
        r5 = execute_query2(q5)

        return render_template('form_submitted.html', total_count=r, count_country=r1, count_city=r2, people_city=r3, people_country=r4,people_interests=r5, form=data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/files', methods=['POST'])
def upload_file():
    try:
        fs = configure_mongo(app)  # Configure MongoDB
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        file_id = fs.put(file)
        return jsonify({'message': 'File uploaded successfully', 'file_id': str(file_id)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/files', methods=['GET'])
def view_files():
    try:
        fs = configure_mongo(app)  # Configure MongoDB
        files = fs.find()

        # Construct a list of dictionaries containing file information
        file_data = []
        for file in files:
            file_info = {
                'file_id': str(file._id),
                'filename': file.filename,
                'upload_date': file.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
                'file_format': file.content_type,
                'file_size': file.length
            }
            file_data.append(file_info)

        return render_template('files.html', files=file_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    try:
        fs = configure_mongo(app)
        file = fs.get(file_id)
        if file:
            return send_file(file, attachment_filename=file.filename, as_attachment=True)
        else:
            return 'File not found', 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

