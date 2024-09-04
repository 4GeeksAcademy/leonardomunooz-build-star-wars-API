from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# print(f"ESTA ES EL OBJETO SQLAlchemy, {db}")
# class GenderEnum(db.enum.Enum):
#     masculino = 'Masculino'
#     femenino  = 'Femenino'


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key = True)
    nombre_usuario = db.Column(db.String(50), nullable = False)
    apellido = db.Column(db.String(80), nullable = True)
    correo = db.Column(db.String(80), nullable = False , unique = True)

    def serializar(self):
        return {
            "id": self.id,
            "nombre_usuario": self.nombre_usuario,
            "apellido": self.apellido,
            "correo": self.correo 
        }

class Planeta(db.Model):
    __tablename__ = "planeta"
    id = db.Column(db.Integer, primary_key = True)
    nombre_planera = db.Column(db.String(20),nullable = False)
    clima = db.Column(db.String(20), nullable = True)
    creacion_planeta = db.Column(db.String(50), nullable = True)
    poblacion = db.Column(db.Integer, nullable = True)

class Personaje(db.Model):
    __tablename__ = 'personaje'
    id = db.Column(db.Integer, primary_key = True)
    nombre_personaje = db.Column(db.String(250), nullable = False)
    anio_nacimiento = db.Column(db.Integer, nullable = True)
    # gender = enum.Enum(GenderEnum)  
    estatura = db.Column (db.Float, nullable = True)
    color_piel = db.Column(db.String(250), nullable = True)
    color_cabello = db.Column(db.String(250), nullable = True)

class Usuario_Planeta(db.Model):
    __tablename__ = 'usuarios_planeta'
    id = db.Column(db.Integer, primary_key = True)
    usuario_id = db.Column(db.Integer,db.ForeignKey('usuario.id'))
    planeta_id = db.Column(db.Integer, db.ForeignKey('planeta.id'))

    # RELACIONES PARA LOS ENDPOINTS 
    usuario = db.relationship('Usuario')
    planeta = db.relationship('Planeta')
    
class Usuario_Personaje(db.Model):
    __tablename__ = 'usuario_personaje'
    id = db.Column(db.Integer, primary_key = True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    personaje_id = db.Column(db.Integer, db.ForeignKey('personaje.id'))

    # RELACIONES PARA LOS ENDPOINTS   
    usuario = db.relationship('Usuario')
    personaje = db.relationship('Personaje')