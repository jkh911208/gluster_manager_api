from flask import Flask
import sys

app = Flask(__name__)

# register blueprint
from routes.credential import credential
app.register_blueprint(credential, url_prefix='/credential')

from routes.resource import resource
app.register_blueprint(resource, url_prefix='/resource')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        debug = bool(sys.argv[1])
    else:
        debug = False
    app.run(debug=debug, threaded=True)
