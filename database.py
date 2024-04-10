from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://rajatvegan:Rajat.vegan1@database-1.c5iwck0oo59v.ap-south-1.rds.amazonaws.com/mydb")

def execute_query1(count_query,params=None):
    with engine.connect() as conn:
        if params:
            result = conn.execute(text(count_query), params)
        else:
            result = conn.execute(text(count_query))

        count_result = result.scalar()
        return count_result
    
def execute_query2(sql_query):
    with engine.connect() as conn:
        result = conn.execute(text(sql_query))

        column_names = result.keys()
        result_dic = [dict(zip(column_names, row)) for row in result.fetchall()]
        return result_dic
      
def add_data_to_db(data):
    with engine.connect() as conn:
        query=text("INSERT INTO form (name,email,mobile,city,country,profession,social_media,interests,comment,friend_ask,privacy_ask) VALUES(:name,:email,:mobile,:city,:country,:profession,:social_media,:interests,:comment,:friend_ask,:privacy_ask)")
        conn.execute(query,{'name':data['name'], 'email':data['email'], 'mobile':data['mobile'],  'city':data['city'], 'country':data['country'], 'profession':data['profession'], 'social_media':data['social_media'], 'interests':data['interests'], 'comment':data['comment'],'friend_ask':data['friend_ask'], 'privacy_ask':data['privacy_ask']})
        conn.commit()


# import the necessary modules
from flask_pymongo import PyMongo
from pymongo import MongoClient
import urllib.parse
from gridfs import GridFS

# Initialize Flask-PyMongo
mongo = PyMongo()

def configure_mongo(app):
    username = "rajatvegan"
    password = "Rajat@123"
    encoded_username = urllib.parse.quote_plus(username)
    encoded_password = urllib.parse.quote_plus(password)
    mongo_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster-mongodb.1kp9n43.mongodb.net/db1?retryWrites=true&w=majority"

    app.config["MONGO_URI"] = mongo_uri
    app.config["MONGO_DBNAME"] = "db1"

    client = MongoClient(mongo_uri)
    db = client['db1']
    fs = GridFS(db)
    
    # Initialize Flask app with MongoDB
    mongo.init_app(app)
    
    return fs  # Return the GridFS object

def get_mongo_collection():
    return mongo.db.collection1
