from flask import Flask
from db.Database import Database
import config
import sys

# connect to Mongo DB
config.db = Database(config.mongodb_uri, config.database_name)

app = Flask(__name__)

# register blueprint
from routes.credential import credential
app.register_blueprint(credential, url_prefix='/credential')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        debug = bool(sys.argv[1])
    else:
        debug = False
    app.run(debug=debug, threaded=True)
