from sqlalchemy import create_engine, text
import pymysql
import os
from dotenv import load_dotenv

from flask_pymongo import PyMongo
from pymongo import MongoClient
from urllib.parse import quote_plus
from gridfs import GridFS

env_paths = ['/etc/secrets/credentials.env', 'credentials.env']
    
# Load the first existing .env file
for env_path in env_paths:
    if os.path.exists(env_path):
        load_dotenv(env_path)
        break

# Access the environment variables
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_host = os.getenv('MYSQL_HOST')
mysql_database = os.getenv('MYSQL_DATABASE')
port = '23472'

engine = create_engine(f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{port}/{mysql_database}?charset=utf8mb4")

def execute_query1(count_query,params=None):
    try:
        with engine.connect() as conn:
            if params:
                result = conn.execute(text(count_query), params)
            else:
                result = conn.execute(text(count_query))
            
            count_result = result.scalar()
            return count_result
    except Exception as e:
        raise Exception(f"Error in execute_query1: {str(e)}")

def execute_query2(sql_query):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            
            column_names = result.keys()
            result_dic = [dict(zip(column_names, row)) for row in result.fetchall()]
            return result_dic
    except Exception as e:
        raise Exception(f"Error in execute_query2: {str(e)}")

def add_data_to_db(data):
    try:
        with engine.connect() as conn:
            query=text("INSERT INTO form (name,email,mobile,city,country,profession,social_media,interests,comment,friend_ask,privacy_ask) VALUES(:name,:email,:mobile,:city,:country,:profession,:social_media,:interests,:comment,:friend_ask,:privacy_ask)")
            conn.execute(query,{'name':data['name'], 'email':data['email'], 'mobile':data['mobile'],  'city':data['city'], 'country':data['country'], 'profession':data['profession'], 'social_media':data['social_media'], 'interests':data['interests'], 'comment':data['comment'],'friend_ask':data['friend_ask'], 'privacy_ask':data['privacy_ask']})
            conn.commit()
    except Exception as e:
        raise Exception(f"Error in add_data_to_db: {str(e)}")

# Initialize Flask-PyMongo
mongo = PyMongo()
def configure_mongo(app):
    
    mongo_user = os.getenv('MONGO_USER')
    mongo_password = os.getenv('MONGO_PASSWORD')
    mongo_host = os.getenv('MONGO_HOST')
    mongo_database = os.getenv('MONGO_DATABASE')

    # encode the credentials 
    mongo_user_encoded = quote_plus(mongo_user)
    mongo_password_encoded = quote_plus(mongo_password)

    mongo_uri = f"mongodb+srv://{mongo_user_encoded}:{mongo_password_encoded}@{mongo_host}/{mongo_database}?retryWrites=true&w=majority"

    app.config["MONGO_URI"] = mongo_uri
    app.config["MONGO_DBNAME"] = "db1"

    client = MongoClient(mongo_uri)
    db = client['db1']
    fs = GridFS(db)
    
    # Initialize Flask app with MongoDB
    mongo.init_app(app)
    
    return fs  # Return the GridFS object

def get_mongo_collection():
    try:
        return mongo.db.collection1
    except Exception as e:
        raise Exception(f"Error in get_mongo_collection: {str(e)}")

