from flask import Flask, request, abort
from config import * 

app = Flask(__name__)

@app.route('/')
def index():
    return "<p>Hello World!</p>"


if __name__ == '__main__':
    app.run()