#Test for endpoints
from flask import Flask, jsonify, request
from flask_restful import Api
from datetime import timedelta

from resources.education import Education
from resources.user import User
from resources.work import Work

app = Flask(__name__)
#change this to link with prostgress later
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

app.secret_key = 'linkiedinscraper'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(User, '/user/<string:name>')
api.add_resource(UserList, '/users')
api.add_resource(Work, '/work/<string:name>')
api.add_resource(Education, '/education/<string:name>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
