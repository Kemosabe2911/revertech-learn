from flask import Flask, Response, request
import pymongo
import json
app= Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port= 27017,
        serverSelectionTimeoutMS = 1000
    )
    db =  mongo.company

    #trigger exception
    mongo.server_info()
except:
    print("ERROR - Cannot connect to db")



##################################
@app.route('/users', methods =['POST'])
def create_user():
    try:
        user = {
            "name": request.form['name'], 
            "lastName": request.form['lastName']
        }
        print("$$$$$$$$$$$$$$$$$$$$")
        print(user)
        dbResponse =  db.users.insert_one(user)
        print(dbResponse.inserted_id)
        return Response(
            response= json.dumps(
                {
                    "message":"user created", 
                    "id": f"{dbResponse.inserted_id}"
                }
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)




if __name__ == '__main__':
    app.run(port=80, debug=True)