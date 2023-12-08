# import sqlalchemy
# print(sqlalchemy.__version__)

from sqlalchemy import create_engine, text

# engine = create_engine("mysql+pymysql://rajatvegan:Rajat.vegan1@localhost/mydb?charset=utf8mb4")
engine = create_engine("mysql+pymysql://wta1zlv42ok0jt7ad7w7:pscale_pw_Hm28awu4bmXXOOdWuPa0rZg1fDPUNbrpFvk89HlmX9V@aws.connect.psdb.cloud/mydb?charset=utf8mb4",
                       connect_args={
                           "ssl":{"ssl_ca": "/etc/ssl/certs/ca-certificates.crt"}
                       })



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



