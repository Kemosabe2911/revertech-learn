from flask import Flask
from mongoengine import *
import datetime

connect('company')
app= Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)