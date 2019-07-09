from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://xbadxprxmkrvbx:815c4c0eb89edf45b25763444505cc5bccf63c0248a730f325c290054c06af21@ec2-174-129-209-212.compute-1.amazonaws.com:5432/d2q23hivule7au'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    # add some dogs
   
    # add owners
        
    # run some queries

    # happy birthday rover!

if __name__ == "__main__":
    with app.app_context():
        main()
