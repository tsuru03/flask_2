from flask import Flask

app = Flask(__name__)
import testapp.views

from testapp import app

if __name__ == '__main__':
    app.run(debug=True)