import certifi
from flask import request,Flask,jsonify
from flask_basicauth import BasicAuth

from pymongo.mongo_client import MongoClient

client = MongoClient("mongodb+srv://sirilux:FZjpQCRkkWd6hntm@cluster0.6jtbi56.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())

app = Flask(__name__) 

app.config['BASIC_AUTH_USERNAME']='username'
app.config['BASIC_AUTH_PASSWORD']='password'
basic_auth = BasicAuth(app)

client.admin.command('ping')
db = client["students"]
collection = db["std_info"]

@app.route("/")
def Greet():
    return "<p>Welcome to Student Management API</p>"

@app.route("/students",methods=["GET"])
@basic_auth.required
def get_all_students():
    students = collection.find()
    return jsonify({"students":list(students)})

@app.route("/students/<int:student_id>",methods=["GET"])
@basic_auth.required
def get_student(student_id):
    student = collection.find_one({"_id":str(student_id)})
    if student:
        return jsonify(student)
    else:
        return jsonify({"error":"Students not found"}),404

@app.route("/students",methods=["POST"])
@basic_auth.required
def create_student():
    data = request.get_json()
    collection.insert_one(data)
    return jsonify(data),201

@app.route("/books/<int:book_id>",methods=["PUT"])
@basic_auth.required
def update_book(book_id):
    book = next((b for b in books if b["id"]==book_id),None)
    if book:
        data = request.get_json()
        book.update(data)
        return jsonify(book)
    else:
        return jsonify({"error":"Book not found"}),404

@app.route("/books/<int:book_id>",methods=["DELETE"])
@basic_auth.required
def delete_book(book_id):
    book = next((b for b in books if b["id"]==book_id),None)
    if book:
        books.remove(book)
        return jsonify({"message":"Book deleted successfully"}),200
    else:
        return jsonify({"error":"Book not found"}),404
    




if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)