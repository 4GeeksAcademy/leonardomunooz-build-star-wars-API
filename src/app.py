"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import re
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db,  Usuario
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    
    usuarios = Usuario()
    usuarios = usuarios.query.all()
    usuarios = list(map(lambda item: item.serializar(),usuarios))
    print(usuarios) 
    return jsonify(usuarios), 200

@app.route('/user/<int:id>', methods=['GET'])
def buscar_id(id = None):
    if id is not None:
        usuario = Usuario()
        usuario = usuario.query.get(id)

        if usuario is not None:
            return jsonify(usuario.serializar()),200
        else:
            return  jsonify({"Mensaje": "usuario no encontrado"}),404



@app.route('/user', methods=['POST'])
def agregar_usuario():

    data = request.json

    if data.get("nombre") is None:
        # print(f"DATA CAPTURADA:  {data.get('nombre')}")
        return jsonify({"Mensaje":"debes enviar un nombre"}),400
    if data.get("apellido") is None:
        # print(f"El apellido es  : {data.get('apellido')}")
        return jsonify({"Mensaje": "debes enviar un apellido"}),400
    if data.get("correo") is None:
        return jsonify({"Mensaje": "Debes enviar un correon electronico"}),400
    if not re.match(f"^[^@\s]+@[^@\s]+\.[^@\s]+$", data.get('correo').lower()):
        return jsonify({"Mensaje": "El formato de correo NO es permitido"}),400
  
    # valida si alguiene esta registrado 
    usuario = Usuario()
    correo_usuario = usuario.query.filter_by(correo = data['correo'])
        # print(usuario.serializar())
    if correo_usuario is not  None:
        usuario = Usuario(nombre_usuario = data["nombre"],apellido = data["apellido"],correo = data["correo"])
        db.session.add(usuario)
        try:
            db.session.commit()
            return jsonify({"mensaje": "usuario guardado con exito!"}),201
        except Exception as error:
            print(error)
            db.session.rollback()
            return jsonify({"mensaje": f"error {error.args} "}),500
    else:
        return jsonify({"Mensaje":"EL usuario existe"}),400  



@app.route("/user/<int:id>", methods = ['PUT'])
def actualizar_usuario(id = None):
    if id is None:
        return jsonify({'Mensaje':'Mensaje de error'}), 400

    data = request.json

    if data.get('nombre') is None:
        return jsonify({"Mensaje":"Hola, soy la respuesta, estoy esperando un Nombre"}),400
    elif data.get('apellido') is None:
        return jsonify({"Mensaje":"Hola, soy la respuesta, estoy esperando un APELIIDO"}),400
    
   
    # BUSCAR EN LA BASE DE DATOS

    usuario = Usuario()
    usuario_actualizado = usuario.query.get(id)

    if usuario_actualizado is None:
        return jsonify({'Mensaje': 'Usuario no existe!'},404)
    else:
        usuario_actualizado.nombre_usuario = data['nombre']
        usuario_actualizado.apellido = data['apellido']
        try:
            db.session.commit()
            return jsonify({"Mensaje": "El usuario fue actualizado correctamente"}),201
        except Exception as error:
            print(error.args)
            return jsonify({'Mensaje': "Si perciste el error, contacte a soporte tecnico"}),500

    # return jsonify([]),200
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
