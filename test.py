from flask import Flask, jsonify, request


bookObject = {
    "type" : "object",
    "properties" : {
        "name" : {"type" : "string"},
        "price" : {"type" : "float"},
        "isbn" : {"type" : "integer"},
    }
}

def validBooksObject(bookObject):
    if ("name" in bookObject
            and "price" in bookObject
                and "isbn" in bookObject):
        return True
    else:
        return False

valid_object = {
    'name': 'F',
    'price': '8.89',
    'isbn': 3542545434536
}

missing_name = {
    'price': '9.99',
    'isbn': 212053444145
}

missing_price = {
    'name': 'La Philosophie dans le boudoir',
    'isbn': 2313254534543
}

missing_isbn = {
    'name': 'La métaphysique des moeurs',
    'price': 12.99
}

