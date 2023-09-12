from flask import Flask, request, make_response
from flask_pymongo import PyMongo, ObjectId
from Schema.models import UserSchema, UpdateSchema


app = Flask(__name__)

# Enter your Mongodb URI here (ex:-mongodb://localhost:27017/users)
app.config["MONGO_URI"] = "[MongoDb URI/databasename]"

mongo = PyMongo(app)
mongo.db.users.create_index('email', unique=True)
user_schema = UserSchema()
update_schema = UpdateSchema()

#Convert ObjectId into normal Id's
def object_id_conversion(object):
    ids = []
    for document in object:
        document['_id'] = str(document['_id'])
        del document['password']
        ids.append(document)
    return ids

#Show all users
@app.route("/users", methods=["GET"])
def get_users():
    users = object_id_conversion(mongo.db.users.find({}))
    if users == []:
        response = make_response({"message": "Your database is empty"}, 200)
    else:
        response = make_response({"message": "Users successfully fetched", "users": users}, 200)
    return response

#Show user with the given id
@app.route("/users/<id>", methods=["GET"])
def get_user_by_id(id):
    try:
        user = object_id_conversion([mongo.db.users.find_one({'_id': ObjectId(id)})])
        response = make_response({"message": "User found", "user": user}, 200)
    except Exception:
        response = make_response({"message": "User not found"}, 400)
    return response

#Create user
@app.route("/users", methods=["POST"])
def create_users():
    user = request.get_json()
    try:
        user_schema.load(user)
        mongo.db.users.insert_one(user.copy())
        del user['password']
        response = make_response({"message": "User created successfully", "user": user}, 201)
        
    except Exception as error:
        try:
            e = eval(str(error))
            response = make_response(e, 401)
        except:
            response = make_response({"message": "Email already exists"}, 400)
    return response
    
    
#Update user
@app.route("/users/<id>", methods=["PUT"])
def update_users(id):
    update = request.get_json()

    try:
        update_schema.load(update)
        setValues = { "$set": update }
        user = object_id_conversion([mongo.db.users.find_one({'_id': ObjectId(id)})])
        mongo.db.users.update_one({'_id': ObjectId(id)}, setValues)
        response = make_response({"message": "User updated successfully", "user": user}, 201)
    except Exception as error:
        try:
            e = eval(str(error))
            response = make_response(e, 401)
        except:
            if "duplicate" in str(error):
                response = make_response({"message": "Email already exists"}, 400)
            else:
                response = make_response({"message": "User not found"}, 400)

    return response

#Delete user
@app.route("/users/<id>", methods=["DELETE"])
def delete_users(id):
    try:
        user = object_id_conversion([mongo.db.users.find_one({'_id': ObjectId(id)})])
        mongo.db.users.delete_one({'_id': ObjectId(id)})
        response = make_response({"message": "User deleted successfully", "user": user}, 200)
    except Exception as error:
        print(error)
        response = make_response({"message": "User not found"}, 400)
    return response

app.run(debug=True)