from flask import Flask

app = Flask(__name__)
app.secret_key = b'ha8w9fn98v2rna9rvna89r-aw-da-dwa-'

from controllers import *
from database import *

if __name__ == "__main__":
    app.run(debug=True)