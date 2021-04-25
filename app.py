import os
from flask import Flask,jsonify,request,render_template,redirect,Response
from flask_restful import Api,Resource, reqparse
from werkzeug.utils import secure_filename
from resources.user import *
from flask_mysqldb import MySQL
from db import db
from flask_jwt_extended import JWTManager



#app = Flask(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://b3c7f95f471470:6199d16a@us-cdbr-east-03.cleardb.com/heroku_d80b842f2e56fa1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '!@#$%^&*()_+=-0987654321'
app.config['PROPAGATE_EXCEPTIONS'] = True


api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_table():
    db.create_all()

api.add_resource(register, '/register')
api.add_resource(login, '/login')
api.add_resource(Create_store, '/Create_store')
api.add_resource(update_products, '/update_products')
api.add_resource(upload_image, '/upload_image')
api.add_resource(First_page, '/First_page')
api.add_resource(view_store, '/view_store/<string:name>')
api.add_resource(view_productimage,'/view_product_image')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port =5000 , debug =True)
