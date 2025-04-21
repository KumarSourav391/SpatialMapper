from geoalchemy2 import Geometry
from app import db

class PointData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(Geometry('POINT'))

class PolygonData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    boundary = db.Column(Geometry('POLYGON'))
