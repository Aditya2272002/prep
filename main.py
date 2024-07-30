from flask import Flask
from test import test




app = Flask(__name__)
app.register_blueprint(test)





if __name__== "__main__":
   app.run(debug=False)