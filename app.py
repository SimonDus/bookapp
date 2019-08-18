from flask import Flask, jsonify, request, Response
import json

booksapp = Flask(__name__)
books = [
    {
        'name': 'Green eggs and Ham',
        'price': 7.99,
        'isbn': 36545334235,
    },
    {
        'name': 'The cat in the hat',
        'price': 6.99,
        'isbn': 35436488787,

    },
    {
        'name': 'F',
        'price': '8.89',
        'isbn': 35425454536,
    },
    {
        'name': 'G',
        'price': '8.89',
        'isbn': 45645161555,
    },
    {
        'name': 'QQQ',
        'price': '10.89',
        'isbn': 54925454345,
    },
    {
        "name": "Le Talmud, traité de Halaka et Guemarra",
        "price": 489.63,
        "isbn": 36545312345
    }
]

#Get /books
@booksapp.route('/books')
def det_books():
    return jsonify({'books': books})

# POST / books

def validBooksObject(bookObject):
    if ("name" in bookObject
            and "price" in bookObject
                and "isbn" in bookObject):
        return True
    else:
        return False

#/books/isbn_number 

@booksapp.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBooksObject(request_data)):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn" : request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201,mimetype='application/json')
        response.headers['Location'] = "books/" + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error":"Invalid book oject passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': '7.99', 'isbn' : '534325125314'}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg),status=400,mimetype='application/json')
        return response


@booksapp.route('/books/<int:isbn>')
def get_books_by_isbn(isbn):
    return_value ={}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)

#PUT /books/36545312345

@booksapp.route('/books/<int:isbn>', methods=['PUT'])
def update_book(isbn):
    request_data = request.get_json()
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn' : isbn
    }
    i = 0
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("",status=204)
    return response

  
booksapp.run(port=5000)
