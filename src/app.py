from enum import unique
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/pokedex"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    tipo = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.String(120), nullable=True)
    fechaNacimiento = db.Column(db.String(100), nullable=False)
    ataquePrincipal = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.String(2000), nullable=False)

    def __repr__(self):
        return "<Anime %r>" % self.username


# *Controllers
class IndexRoute(Resource):
    def get(self):
        return {"response": "Hola, este es el index route :)"}


class IndexAnime(Resource):
    def get(self):
        pokemon = User.query.all()
        response = []
        if pokemon:
            for anime in pokemon:
                response.append(
                    {
                        "id": anime.id,
                        "username": anime.username,
                        "tipo": anime.tipo,
                        "edad": anime.edad,
                        "fechaNacimiento": anime.fechaNacimiento,
                        "ataquePrincipal": anime.ataquePrincipal,
                        "foto": anime.foto,
                    }
                )

        return {"response": response}, 200

    def post(self):
        animeACrear = request.get_json()
        if (animeACrear['username'] == "" or animeACrear['edad'] == "" or animeACrear['fechaNacimiento'] == "" or animeACrear['ataquePrincipal'] == ""):
            return { "response": "Error al ingregar los datos, revise que todos los campos requeridos tengan informacion"}, 400
        anime = User(username=animeACrear['username'], tipo=animeACrear['tipo'], edad=animeACrear['edad'], fechaNacimiento=animeACrear['fechaNacimiento'], ataquePrincipal=animeACrear['ataquePrincipal'], foto=animeACrear['foto'])
        db.session.add(anime)
        db.session.commit()
        return { "response": " Anime creado exitosamente!"}, 201

class UserById(Resource):
    def get(self, id):
        anime = User.query.filter_by(id=id).first()

        if (anime is None):
            return { "response": "Error al obtener los datos, el pokemon no existe."}, 400
 
        return {'response': {
            "id": anime.id,
            "username": anime.username,
            "tipo": anime.tipo,
            "edad": anime.edad,
            "fechaNacimiento": anime.fechaNacimiento,
            "ataquePrincipal" : anime.ataquePrincipal,
            "foto": anime.foto
        }}, 200

    def put(self, id):
        anime = User.query.filter_by(id=id).first()
        datos = request.get_json()
        # TODO: LOOKUP 'ARGUMENT PARSING for Flask-RESTful'
        if (datos['username'] == "" or datos['username'] is None or datos['edad'] == "" or datos['edad'] is None or datos['fechaNacimiento'] == "" or datos['fechaNacimiento'] is None or datos['ataquePrincipal'] == "" or datos['ataquePrincipal'] is None ):
            return { "response": "Error al actualizar los datos, pokemon no existe."}, 400

        anime.username = datos['username']
        anime.tipo = datos['tipo']
        anime.edad = datos['edad']
        anime.fechaNacimiento = datos['fechaNacimiento']
        anime.ataquePrincipal = datos['ataquePrincipal']
        anime.foto = datos['foto']
        db.session.commit()
 
        return {"response": "Anime actualizado con exito!"}

    def delete(self, id):
        anime = User.query.filter_by(id=id).first()

        if (anime is None):
            return { "response": "Error al borrar los datos, el pokemon no existe."}, 400

        db.session.delete(anime)
        db.session.commit()
        return { "response": "Anime con id: {anime}. Borrado exitosamente. ".format(anime=id)}, 203

db.create_all()

# *Routes
# GET
api.add_resource(IndexRoute, '/')
# GET, POST
api.add_resource(IndexAnime, '/pokemon')
# GET, PUT, DELETE
api.add_resource(UserById, '/pokemon/<int:id>')