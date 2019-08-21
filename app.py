from flask import Flask, jsonify, request, Response
import json
import datetime
from settings import *
from BookModel import *
from flask_jwt import jwt



booksapp.config['SECRET_KEY'] = 'NotSoSecretKey'

@booksapp.route('/login')
def get_token():
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
    token = jwt.encode({'exp': expiration_date}, booksapp.config['SECRET_KEY'], algorithm='HS256')
    return token

#Get /books
@booksapp.route('/books')
def get_books():
    token = request.args.get('token')
    try:
        jwt.decode(token, booksapp.config['SECRET_KEY'])
    except:
        return jsonify({'error': 'Need a valid token to view this page'}, 401)
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
