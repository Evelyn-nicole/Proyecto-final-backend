import re
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Event, Favorite, Comment, Availability, Reservation, Superadmin
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:floki@localhost:5432/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['JWT_SECRET_KEY'] = "super-secreta"
app.config['SECRET_KEY'] = "otra-super-secreta"
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
Migrate(app, db)
CORS(app)


@app.route('/')
def home():
    return jsonify('Hola Mundo')


@app.route('/user', methods=["GET"])
def user():
    user = User.query.get(1)
    return jsonify({
        "user": user.serialize()
    }), 200

# CREAR NUEVO USUARIO
@app.route('/newUser', methods=["POST", "GET"])
def newUser():
    if request.method == "POST":
        email = request.json.get("email")
        name = request.json.get("name")
        password = request.json.get("password")
        phone = request.json.get("phone")

    # campos vacios
    if name == "":
        return jsonify({
            "msg": "Debe informar su nombre"
        }), 400

    if email == "":
        return jsonify({
            "msg": "Debe informar su email"
        }), 400

    if password == "":
        return jsonify({
            "msg": "Debe informar su Contraseña"
        }), 400

    if phone == "":
        return jsonify({
            "msg": "Debe informar su Telefono"
        }), 400

    # verificar si el usuario existe
    user_exist = User.query.filter_by(email=email).first()
    if user_exist != None:
        return jsonify("Usted ya existe como cliente."), 404
    else:
        user = User()
        user.email = email
        user.name = name
        user.phone = phone
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        password_regex = '^.*(?=.{4,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'

        if re.search(password_regex, password):
            password_hash = bcrypt.generate_password_hash(
                password).decode("utf-8")
            user.password = password_hash

        db.session.add(user)
        db.session.commit()

    return jsonify({
        "msg": "Usuario Creado con Exito"
    }), 200

# LOGIN
@app.route('/login', methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if password == "":
        return jsonify({
            "msg": "contraseña invalida"
        }), 400
    if email == "":
        return jsonify({
            "msg": "email invalido"
        }), 400

     # email y contraseña no corresponde
    if email != email:
        return jsonify({
            "msg": "Haz ingresado mal tu email"
        }), 400

    if password != password:
        return jsonify({
            "msg": "Haz ingresado mal tu contraseña"
        }), 400

    # buscamos que el usuario exista
    user = User.query.filter_by(email=email).first()

    # debe retornarme un usuario registrado
    if user is None:
        return jsonify({
            "msg": "No existe, registrate aqui"
        }), 400

    elif bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.password)
        return jsonify({
            "success": "Bienvenido a tu perfil",
            "access_token": access_token,
            "user": user.serialize()
        }), 200
    else:
        return jsonify({
            "msg2": "credenciales erroneas"
        }), 400

# RUTA PRIVADA EDITAR PERFIL/DATOS DE USUARIO
@app.route('/edituser/<int:id>', methods=["PUT"])
@jwt_required()
def get_user_id(id):
    if request.method == "PUT":
        if id is not None:
            profile = User.query.filter_by(id=id).first()
            if profile is None:
                return jsonify({
                    "msg": "Usuario no existe"
                }), 400

            user = User.query.filter_by(id=profile.id).first()
            checkpassword = request.json.get('password')
            password_regex = '^.*(?=.{4,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
            phone_regex = '^(\+?56)?(\s?)(0?9)(\s?)[9876543]\d{7}$'
            email_regex = '^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$'
            print(re.search(password_regex, checkpassword))

          
            if re.search(password_regex, checkpassword):
                password_hash = bcrypt.generate_password_hash(
                    checkpassword).decode("utf-8")
                user.password = password_hash
            else:
                return jsonify({
                    "msg": "Formato de contraseña errónea"
                }), 400

            # verificacion telefono
            if (re.search(phone_regex, str(request.json.get('phone')))):
                user.phone = request.json.get("phone")
            else:
                return jsonify({
                    "msg": "Formato de teléfono erróneo"
                }), 400

            # verificacion email
            if (re.search(email_regex, request.json.get("email"))):
                user.email = request.json.get("email")
            else:
                return jsonify({
                    "msg": "Formato de email erróneo"
                }), 400

            user.name = request.json.get("name")
            user.phone = request.json.get("phone")

            if user.name == "":
                return jsonify({
                    "msg": "Debe ingresar un nombre valido"
                }), 400

        db.session.add(user)
        db.session.commit()

    return jsonify({
        "success": "Datos actualizados"
    }), 200

# RUTA PRIVADA PARA EL PROFILE
@app.route('/private', methods=["POST"])
@jwt_required()
def private():
    current_user = get_jwt_identity()
    current_user_token_expires = get_jwt()["exp"]

    return jsonify({
        "current_user": current_user,
        "current_user_token_expires": datetime.fromtimestamp(current_user_token_expires)
    }), 200


# RUTA AVAILABILITY DEL CALENDARIO
@app.route('/availability', methods=["POST", "GET"])
def availability():
    if request.method == "POST":
        date = request.json.get("date")
       
        # verificar que la fecha esta disponible
        availability_date = Availability.query.filter_by(date=date).first()
 
        if availability_date != None:
            return jsonify({
            "msg":"Fecha no encuentra disponible"
            }),400
        
        else:
            availability = Availability()
            availability.date = date
    
        db.session.add(availability)
        db.session.commit()
        
    return jsonify({
        "success": "Fecha reservada exitosamente"
        }),200
 


@app.route('/admin/new_event', methods=["POST", "GET"])
def admin_new_event():
    if request.method == "GET":
        event = Event.query.all()
        results = list(map(lambda event: event.serialize(), event))
        return jsonify(results)

    if request.method == "POST":
        name = request.json.get("name")
        description = request.json.get("description")
        thematic = request.json.get("thematic")
        price = request.json.get("price")
        availability = request.json.get("availability")
    
        # campos vacios
        if name == "":
            return jsonify({
                "msg": "Debe informar el nombre del evento"
            }), 400
        if description == "":
            return jsonify({
                "msg": "Debe indicar una descripción"
            }), 400
        if thematic == "":
            return jsonify({
                "msg": "Debe informar una temática"
            }), 400
        if price == "":
            return jsonify({
                "msg": "Debe colocar un precio"
            }), 400
        
        # verificar si el evento existe
        event_exist = Event.query.filter_by(name=name).first()
        if event_exist != None:
            return jsonify("Éste evento ya existe."), 404
        else:
            event = Event()
            event.description = description
            event.thematic = thematic
            event.price = price
            event.name = name

            db.session.add(event)
            db.session.commit()
            
            return jsonify({
                "msg": "Evento Creado con Exito"
            }), 200

@app.route('/admin/edit_event/<int:id>', methods=["PUT"])
def admin_edit_event(id):
    if request.method == "PUT":
        if id is not None:
            event_exist = Event.query.filter_by(id=id).first()
            if event_exist is None:
                return jsonify({
                    "msg": "El evento no existe"
                }), 400
           
            event = Event.query.filter_by(id=event_exist.id).first()
            event.description = request.json.get("description")
            event.thematic = request.json.get("thematic")
            event.price = request.json.get("price")
            event.name = request.json.get("name")
        
        db.session.add(event_exist)
        db.session.commit()
   
    return jsonify({
        "msg": "Evento modificado con Exito"
    }), 200


# RUTA NUEVO USUARIO ADMINISTRADOR
@app.route('/admin_new_user', methods=["POST", "GET"])
# @jwt_required()
def admin_new_user():
    if request.method == "POST":
        email = request.json.get("email")
        name = request.json.get("name")
        password = request.json.get("password")
        phone = request.json.get("phone")

    if name == "":
        return jsonify({
            "msg": "Debe informar su nombre"
        }), 400

    if email == "":
        return jsonify({
            "msg": "Debe informar su email"
        }), 400

    if password == "":
        return jsonify({
            "msg": "Debe informar su Contraseña"
        }), 400

    if phone == "":
        return jsonify({
            "msg": "Debe informar su Telefono"
        }), 400

    # verificar si el usuario existe
    password_regex = '^.*(?=.{4,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
    email_regex = '^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$'
    
    superadmin_exist = Superadmin.query.filter_by(email=email).first()
    
    if superadmin_exist != None:
        return jsonify({
            "msg":"Usted ya existe como Super Administrador"
            }), 404
    else:
        superadmin = Superadmin()
        superadmin.email = email
        superadmin.name = name
        superadmin.phone = phone
        superadmin.password = bcrypt.generate_password_hash(password).decode('utf-8')
        password_regex = '^.*(?=.{4,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'

        #verificando la contraseña
        if re.search(password_regex, password):
            password_hash = bcrypt.generate_password_hash(
                password).decode("utf-8")
            superadmin.password = password_hash
        
        else:
            return jsonify({
                "msg": "credenciales erroneas"
                }), 400

        if (re.search(email_regex, request.json.get("email"))):
                user.email = request.json.get("email")
        else:
            return jsonify({
                "msg": "Formato de email erróneo"
                }), 400

        db.session.add(superadmin)
        db.session.commit()

        return jsonify({
            "msg": "Super Administrador Creado con Exito"
            }), 200


@app.route('/admin_login', methods=["POST"])
def admin_login():
    email = request.json.get("email")
    password = request.json.get("password")
 
    if password == "":
        return jsonify({
            "msg": "contraseña invalida"
        }), 400
    if email == "":
        return jsonify({
            "msg": "email invalido"
        }), 400

    if email != email:
        return jsonify({
            "msg": "Haz ingresado mal tu email"
        }), 400
    if password != password:
        return jsonify({
            "msg": "Haz ingresado mal tu contraseña"
        }), 400
        
  
    superadmin = Superadmin.query.filter_by(email=email).first()
    if superadmin is None:
        return jsonify({
            "msg": "Administrador no existe, debes registrarte"
        }), 400
        
    elif bcrypt.check_password_hash(superadmin.password, password):
        access_token = create_access_token(identity=superadmin.password)
     
        return jsonify({
            "success": "Bienvenido a tu perfil",
            "access_token": access_token,
            "superadmin": superadmin.serialize()
        }), 200
    else:
        return jsonify({
            "msg2": "credenciales erroneas"
        }), 400
        
@app.route('/admin_edit_user/<int:id>', methods=["PUT"])
#@jwt_required()
def get_admin_id(id):
    if request.method == "PUT":
        if id is not None:
            admin = Superadmin.query.filter_by(id=id).first()
            if admin is None:
                return jsonify({
                    "msg": "Usuario no existe"
                }), 400
                
            checkpassword = request.json.get('password')
            password_regex = '^.*(?=.{4,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
            phone_regex = '^(\+?56)?(\s?)(0?9)(\s?)[9876543]\d{7}$'
            email_regex = '^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$'
                
            user_admin = Superadmin.query.filter_by(id=admin.id).first()
            if re.search(password_regex, checkpassword):
                password_hash = bcrypt.generate_password_hash(
                    checkpassword).decode("utf-8")
                user_admin.password = password_hash
            else:
                return jsonify({
                    "msg": "Formato de contraseña errónea"
                }), 400
                
            if (re.search(phone_regex, str(request.json.get('phone')))):
                user.phone = request.json.get("phone")
            else:
                return jsonify({
                    "msg": "Formato de teléfono erróneo"
                }), 400
                
            if (re.search(email_regex, request.json.get("email"))):
                user.email = request.json.get("email")
            else:
                return jsonify({
                    "msg": "Formato de email erróneo"
                }), 400
                
            user_admin.name = request.json.get("name")
            user_admin.phone = request.json.get("phone")
            
            if user_admin.name == "":
                return jsonify({
                    "msg": "Debe ingresar un nombre valido"
                }), 400
                
        db.session.add(user_admin)
        db.session.commit()
        
    return jsonify({
        "success": "Datos actualizados"
    }), 200


if __name__ == "__main__":
    app.run(host='localhost', port=8080)