from flask import Flask

booksapp = Flask(__name__)

booksapp.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///E:\python\projects\booksapp\database.db'
booksapp.config['SQLACLHEMY_TRACK_MODIFICATIONS'] = False


