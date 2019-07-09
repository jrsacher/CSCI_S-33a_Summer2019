# See Brian's example: https://cdn.cs50.net/web/2018/spring/lectures/4/src4/airline5/
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Dog(db.Model):
    __tablename__ = "dogs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    breed = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def add_owner(self, name):
        person = Owner(name=name, dog_id=dogs.id)
        db.session.add(person)
        db.session.commit()


class Owner(db.Model):
    __tablename__ = "owners"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    dog_id = db.Column(db.Integer, db.ForeignKey("dogs.id"), nullable=False)
    
