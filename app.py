from flask import Flask, render_template, jsonify, request
from database import  add_data_to_db,  execute_query1, execute_query2

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/form")
def form():
    return render_template('form.html')


@app.route('/view')
def view():
    
    q1 = "SELECT COUNT(*) FROM form"
    q2 = "SELECT COUNT(*) FROM form WHERE city='kanpur'"
    q = "SELECT * FROM form"


    total_count = execute_query1(q1)
    city_count = execute_query1(q2)
    data_result = execute_query2(q)

    return render_template('view.html', total_count=total_count, peoples=data_result, kanpur_count=city_count)




@app.route("/form", methods=['POST'])
def submit_form():
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




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)