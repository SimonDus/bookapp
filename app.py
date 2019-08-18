from flask import Flask, jsonify, request

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

 
@booksapp.route('/books', methods=['POST'])
def add_book():
    return jsonify(request.get_json())


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
    
booksapp.run(port=5000)
