from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from geoalchemy2 import Geometry

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/spatial_db'

db = SQLAlchemy(app)
api = Api(app)  # API instance created directly in app.py

# Define Models
class PointData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(Geometry('POINT'))

class PolygonData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    boundary = db.Column(Geometry('POLYGON'))

# API Endpoints
class PointResource(Resource):
    def get(self):
        points = PointData.query.all()
        return jsonify([{'id': p.id, 'name': p.name, 'location': str(p.location)} for p in points])

    def post(self):
        data = request.json
        point = PointData(name=data['name'], location=f"SRID=4326;POINT({data['lng']} {data['lat']})")
        db.session.add(point)
        db.session.commit()
        return jsonify({"message": "Point added!"})

api.add_resource(PointResource, '/points')

class PolygonResource(Resource):
    def get(self):
        polygons = PolygonData.query.all()
        return jsonify([{'id': p.id, 'name': p.name, 'boundary': str(p.boundary)} for p in polygons])

    def post(self):
        data = request.json
        polygon = PolygonData(name=data['name'], boundary=f"SRID=4326;POLYGON(({data['coordinates']}))")
        db.session.add(polygon)
        db.session.commit()
        return jsonify({"message": "Polygon added!"})

api.add_resource(PolygonResource, '/polygons')

@app.route('/')
def home():
    return "Spatial Data API is running!"

# Initialize database on startup
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
