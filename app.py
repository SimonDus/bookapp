from flask import Flask, jsonify

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
    return {'books': books}
    
booksapp.run(port=5000)
