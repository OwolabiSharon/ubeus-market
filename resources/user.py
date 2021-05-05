from db import db
import hashlib
from models.user import *
from flask import jsonify, send_file,Response
from flask_restful import Resource, reqparse,request
from flask_jwt_extended import create_access_token,jwt_required
import werkzeug
from werkzeug.utils import secure_filename
from io import BytesIO



class register(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def encrypt_string(hash_string):
        sha_signature = \
            hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature


    def post(self):

        data = register.parser.parse_args()
        if User.find_by_email(data['email']):
            return  {
            'status':False,
            'message':'user exists'
            },400

        user = User(data['username'],data['email'],data['password'])

        User.save_to_db(user)



        #notification.notify(title= "notification",message="you are succesfully registered",timeout=5)
        return {
        'status': True,
        #'data info': user.jsonyo(),
        'data':user.json(),
        'message':'user created succesfully'
        },201


class login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = login.parser.parse_args()
        user = User.find_by_email(data['email']) and User.find_by_password(data['password'])
        if user:
            access_token = create_access_token(identity=user.id,fresh =True)
            #refresh_token= create_refresh_token(user.id)
            try:
                return {
                      'status': True,
                      'data': access_token,
                      'message':'you are logged in'
                },200
            except:
                {'message':'a little error occuredwhen trying to access the database'}


        return {
        'status':True,
        'status':False,
        'message':'user not found'
        },404
class top_up(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('ammount',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = top_up.parser.parse_args()
        user = User.find_by_username(data['username']) and User.find_by_password(data['password'])
        if user:
            user.account_balance = Integer(user.account_balance)
            user.account_balance = user.account_balance + data['ammount']
            user.account_balance = string(user.account_balance)
            try:
                return {
                      'status': True,
                      'data': user.account_balance,
                      'message':'your account_balance'
                },200
            except:
                {'message':'a little error occured when trying to access the database'}


        return {
        'status':True,
        'status':False,
        'message':'either your username or password is incorrect'
        },404

class add_to_wishlist(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Product_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = add_to_wishlist.parser.parse_args()
        Product = Product.find_by_name(data['Product_name'])
        user = User.find_by_username(data['username'])
        if product:
            wishlist = Wishlist(data['Product_name'],product.price,user.id)
            Wishlist.save_to_db(wishlist)
            return{
                 "status": True,
                 'message':'product added to wishlist'
                 },201
        return {
              'status': False,
              'message':'product not found'
        },404


class delete_from_wishlist(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Product_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = delete_from_wishlist.parser.parse_args()
        Product = Wishlist.find_by_name(data['Product_name'])
        user = User.find_by_username(data['username'])
        if product:
            Wishlist.save_to_db(Product)
            return{
                 "status": True,
                 'message':'product removed from wishlist'
                 },201
        return {
              'status': False,
              'message':'product not in your wishlist'
        },404


class add_to_cart(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Product_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = add_to_cart.parser.parse_args()
        Product = Product.find_by_name(data['Product_name'])
        user = User.find_by_username(data['username'])
        if product:
            cart = Cart(data['Product_name'],product.price,user.id)
            Cart.save_to_db(cart)
            return{
                 "status": True,
                 'message':'product added to wishlist'
                 },201
        return {
              'status': False,
              'message':'product not found'
        },404

class delete_from_cart(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Product_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = delete_from_cart.parser.parse_args()
        Product = Cart.find_by_name(data['Product_name'])
        user = User.find_by_username(data['username'])
        if product:
            Cart.save_to_db(Product)
            return{
                 "status": True,
                 'message':'product removed from your cart'
                 },201
        return {
              'status': False,
              'message':'product not in your cart'
        },404

class buy_product(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Product_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = buy_product.parser.parse_args()
        Product = Product.find_by_name(data['Product_name'])
        user = User.find_by_username(data['username'])
        store = Store.find_by_name(data['store_name'])
        inventory = Inventory.find_by_name(data['store_name'])
        if product:
            user.account_balance = Integer(user.account_balance)
            user.account_balance = user.account_balance - Product.price
            store.account_balance = Integer(store.account_balance)
            store.account_balance = store.account_balance + Product.price

            inventory.NO_of_products = inventory.NO_of_products - 1

            store.account_balance = string(store.account_balance)
            user.account_balance = string(user.account_balance)

            return{
                 "status": True,
                 'message':'product will be shipped to you soon'
                 },201
        return {
              'status': False,
              'message':'product not found'
        },404


    
    
class Create_store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    @jwt_required()
    def post(self):
        data = Create_store.parser.parse_args()
        store = Store.find_by_name(data['store_name'])
        user = User.find_by_username(data['username'])
        if store:
            return {
                  'status': False,
                  'message':'Store exists already'
            },400
        new_store = Store(data['store_name'],data['description'],data['store_address'],user.id)
        Store.save_to_db(new_store)
        new_inventory = Inventory(data['store_name'],0,new_store.id)

        Inventory.save_to_db(new_inventory)
        ki = new_store.json2()
        try:
            return{
                 "status": True,
                 'data': ki,
                 'message':'store created succesfully'
                 },201
        except:
            return {"message":"little error occured when trying to access db"}

class update_products(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Product_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('price',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('Number_available',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    @jwt_required()
    def post(self):
        data = update_products.parser.parse_args()

        inventory = Inventory.find_by_name(data['store_name'])
        product = Product.find_by_name(data['Product_name'])
        if product.user_id == inventory.id:
            return{
                 "status": False,
                 'message':'product is already in your inventory'
                 },400

        else:
            #file = request.files['inputFile']
            new_product = Product(data['Product_name'],data['description'],data['price'],data['Number_available'],inventory.id)


            Product.save_to_db(new_product)
            inventory.NO_of_products = inventory.NO_of_products + 1

            try:
                return{
                     "status": True,
                     'data': new_product.json(),
                     'message':'store created succesfully'
                     },201
            except:
                return {"message":"little error occured when trying to access db"}
class upload_image(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Product_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def post(self):
        data = upload_image.parser.parse_args()

        product = Product.find_by_name(data['Product_name'])
        if product:
            pic = request.files['pic']
            if not pic:
                return 'No pic uploaded!', 400
            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype
            if not filename or not mimetype:
                return 'Bad upload!', 400


            img = Image(image=pic.read(), name=product.name, mimetype=mimetype,user_id=product.id)


            Image.save_to_db(img)
            return{
                 "status": True,
                 'message':'image uploaded to product info'
                 },200

        return{
             "status": False,
             'message':'product is not in your inventory'
             },404

class First_page(Resource):
    def get(self):
        try:
            return {'stores': list(map(lambda x: x.json(), Store.query.all()))}
        except:
            return {"message":"little error occured when trying to access db"}




class view_store(Resource):
    def get(self,name):


        store = Store.find_by_name(name)
        if store:
            try:
                return{
                     "status": True,
                     "data": store.json2(),
                     'message':'this is the store'
                     },201
            except:
                return {"message":"little error occured when trying to access db"}





        return{
             "status": False,
             'message':'store not found'
             },404


class view_productimage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Product_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )


    def post(self):
        data = view_productimage.parser.parse_args()

        product = Product.find_by_name(data['Product_name'])
        image = Image.find_by_name(data['Product_name'])
        if product:
            return Response(image.image,mimetype=image.mimetype)
        return{
             "status": False,
             'message':'product is not in your inventory'
             },404
