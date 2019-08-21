from flask import Flask, jsonify, request, Response
import json
import datetime
from settings import *
from BookModel import *
from flask_jwt import jwt
from UserModel import User
from functools import wraps



booksapp.config['SECRET_KEY'] = 'NotSoSecretKey'

# LOGIN
@booksapp.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)

    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, booksapp.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, booksapp.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need a valid token to view this page'}, 401)
    return wrapper


# Get /books
@booksapp.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})


def validBooksObject(bookObject):
    if ("name" in bookObject
            and "price" in bookObject
                and "isbn" in bookObject):
        return True
    else:
        return False

#POST
@booksapp.route('/books', methods=['POST'])
@token_required
def add_book():
    request_data = request.get_json()
    if(validBooksObject(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'],)
        response = Response("", 201,mimetype='application/json')
        response.headers['Location'] = "books/" + str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error":"Invalid book oject passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': '7.99', 'isbn' : '534325125314'}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg),status=400,mimetype='application/json')
        return response



#GET
@booksapp.route('/books/<int:isbn>')
def get_books_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)

# TO FINISH
# @booksapp.route('/books/<string:name>', methods=['GET'])
# def get_books_by_name(name):
#     i = 0
#     found_books = []
#     for book in books:
#         if book["name"].find(name):
#             i += 1
#         else:
#             found_books.append(books[i])    
#     return jsonify(found_books)

def valid_put_request_data(request_data):
    if("name" in request_data and
            "price" in request_data):
        return True
    else:
        return False


#REPLACE
@booksapp.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if(not valid_put_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            "error":"Invalid book oject passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': '7.99', 'isbn' : '534325125314'}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg),status=400,mimetype='application/json')
        return response
    Book.replace_book(isbn, request_data['name', request_data['price']])
    response = Response("",status=204)
    return response


#PATCH
@booksapp.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json()

    if('name' in request_data):
        Book.update_book_name(isbn, request_data['name'])
    if('price' in request_data):
        Book.update_book_price(isbn, request_data['price'])
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response  

# DELETE
@booksapp.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    if (Book.delete_book(isbn)):
        response = Response("", status=204)
        return response
    else:    
        invalidBookObjectErrorMsg = {
        "error" : "No match"
    }     
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response

 
booksapp.run(port=5000)
