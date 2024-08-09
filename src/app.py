"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
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
    
    usuarios = User()
    usuarios = usuarios.query.all()
    usuarios = list(map(lambda item: item.serializar(),usuarios))
    print(usuarios) 
    return jsonify(usuarios), 200

@app.route('/user/<int:id>', methods=['GET'])
def buscar_id(id = None):
    if id is not None:
        usuario = User()
        usuario = usuario.query.get(id)

        if usuario is not None:
            return jsonify(usuario.serializar()),200
        else:
            return  jsonify({"Mensaje": "usuario no encontrado"}),404
    # return jsonify([]),200


@app.route('/user', methods=['POST'])
def agregar_usuario():

    data = request.json
    if data.get("nombre") is None:
        return jsonify({"mensasje":"debes enviar un nombre"}),400
    elif data.get("apellido") is None:
        return jsonify({"Mensaje": "debes enviar un apellido"}),400
    elif data.get("correo") is None:
        return jsonify({"Mensaje": "Debes enviar un correon electronico"}),400
    else:

        # valida si alguiene esta registrado 
        usuario = User()
        correo_usuario = usuario.query.filter_by(correo = data['correo'])
        if correo_usuario is None:

            usuario = User(nombre_usuario = data["nombre"],apellido = data["apellido"],correo = data["correo"])
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


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
