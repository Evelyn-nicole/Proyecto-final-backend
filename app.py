from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Event, Favorite, Comment, Availability, Reservation
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:floki@localhost:5432/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['JWT_SECRET_KEY'] = 'super-secreta'
app.config['SECRET_KEY'] =  'otra-super-secreta'

db.init_app(app)
Migrate(app, db) 
CORS(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return jsonify('Hola Mundo')

    
@app.route('/user', methods=["GET"])
def user():
    user = User.query.get(1)
    return jsonify(user.serialize()),200

@app.route('/newUser', methods=["POST", "GET"])
def newUser():
    if request.method =="POST":
        email = request.json.get("email")
        name = request.json.get("name")
        password = request.json.get("password")
        phone = request.json.get("phone")
      
    if name == "":
        return jsonify("Debe informar su nombre."), 401
    if email == "":
        return jsonify("Debe informar su email."), 401
    if password == "":
        return jsonify("Debe informar su Contraseña."), 401
    if phone == "":
        return jsonify("Debe informar su Telefono."), 401
        
    user_exist = User.query.filter_by(email = email).first()
    print(user_exist)

    if user_exist != None:            
        return jsonify("Usted ya existe como cliente."), 404
    else:
        user = User()
        user.email = email
        user.name = name
        user.phone = phone
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')

        db.session.add(user)
        db.session.commit()
    
    return jsonify("Usuario Creado"), 200


# @app.route('/login', methods=["POST"])
# def login():
#     email = request.json.get("email")
#     password = request.json.get("password")
#     user_name = User.query.filter_by(email=email).first()
#     if user_name is None:
#         return jsonify (
#             "usuario no existe"
#         ),401

#     user = User.query.filter_by(email=email, password = password).first()
#     if user is None:
#         return jsonify(
#             "contraseña incorrecta"
#         ),401

#     # Campos vacios
#     if email == "":
#         return jsonify(
#             "Debe ingresar email."
#         ),401

#     if password == "":
#         return jsonify(
#             "Debe ingresar contraseña."
#         ),401
  
#     # usuario registrado
#     if email == email and password == password:
#         return jsonify({
#             "user":user.serialize(),
#         }),200
 
#     # email y contraseña no corresponde 
#     if email != email:
#         return jsonify(
#             "Haz ingresado mal tu email"
#         ),401
        
#     if password != password:
#         return jsonify(
#             "Haz ingresado mal tu contraseña"
#         ),401

@app.route('/login', methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # campos vacios
    if password == "":
        return jsonify({
            "msg":"contraseña invalida"
        }),400
    if email == "":
        return jsonify({
            "msg":"email invalido"
        }),400
    
     # email y contraseña no corresponde 
    if email != email:
        return jsonify({
            "msg":"Haz ingresado mal tu email"
        }),400
        
    if password != password:
        return jsonify({
            "msg":"Haz ingresado mal tu contraseña"
        }),400

    # buscamos que el usuario exista
    user = User.query.filter_by(email=email).first()

    # debe retornarme un usuario registrado
    if user is None:
        return jsonify ({
            "msg":"usuario no existe, debes registrate"
        }),400
    
    elif bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.password)
        return jsonify({
            "msg":"user login 200",
            "access_token": access_token,
            "user":user.serialize(),
        }),200
    else: 
        return jsonify({
            "msg":"credenciales erroneas"
        }),400

   
   
    # print(user.name)    
    # return user.name

 
@app.route('/availability', methods=["POST", "GET"])
def availability():
    user = request.json.get("user")
    date = request.json.get("date")

    availability_date = Availability.query.filter_by(date=date).first()
    # print(availability_date.date)
    # print(date)            

    if availability_date is None:
        return jsonify({
            "msg":"fecha esta disponible"
        }),200
    else:
        return jsonify({
            "msg":"fecha no dispinible"
        }), 400






@app.route('/edituser/<int:id>', methods=["PUT"])
def edituser():
    if request.method =="PUT":
        email = request.json.get("email")
        name = request.json.get("name")
        password = request.json.get("password")
        phone = request.json.get("phone")

    user = User.query.filter_by(id=id).first()

    









if __name__ == "__main__":
    app.run(host='localhost', port=8080)


    # # elif bcrypt.check_password_hash(user.password, password):
    #     access_token = create_access_token(Identity=user.email)
    #     return jsonify({
    #         "msg":"user login 200",
    #         "access_token":access_token,
    #         "user": user.serialize(),
    #     }),200