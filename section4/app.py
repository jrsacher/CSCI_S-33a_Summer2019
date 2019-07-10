from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
# DON'T DO THIS!!! USE ENVIRONMENT VARIABLES
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://xbadxprxmkrvbx:815c4c0eb89edf45b25763444505cc5bccf63c0248a730f325c290054c06af21@ec2-174-129-209-212.compute-1.amazonaws.com:5432/d2q23hivule7au'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    # add some dogs
    fido = Dog(name='fido', breed='golden', age=1)
    rover = Dog(name='rover', breed='lab', age=5)

    db.session.add(fido)
    db.session.add(rover)
    db.session.commit()

    # add owners
    fido.add_owner('Richard')
    rover.add_owner('Susan')
    
    # run some queries
    d = Dog.query.all()
    for dog in d:
        print(dog.name)

    r = Dog.query.filter_by(name='rover').first()
    print(r.name, r.age)

    # happy birthday rover!
    r.age += 1
    db.session.commit()     # didn't work live, but totally works now!

    r = Dog.query.filter_by(name='rover').first()
    print(r.name, r.age)

if __name__ == "__main__":
    with app.app_context():
        main()
