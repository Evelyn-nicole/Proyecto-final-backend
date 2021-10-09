from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Event, Favorite, Comment, Availability, Reservation
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:floki@localhost:5432/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)
Migrate(app, db) 
CORS(app)

@app.route('/')
def home():
    return jsonify('Hola Mundo')

    
@app.route('/user', methods=["GET"])
def user():
    user = User.query.get(1)
    return jsonify(user.serialize()),200


@app.route('/login', methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    user = User.query.filter_by(email= email).first()
    print(user.email)

    return jsonify("prueba")


if __name__ == "__main__":
    app.run(host='localhost', port=8080)