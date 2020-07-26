from flask import Flask
from db.Database import Database
import config

# connect to Mongo DB
db = Database(config.mongodb_uri, config.database_name)

app = Flask(__name__)

# register credentail routes
from routes.credential import credential
app.register_blueprint(credential, url_prefix='/credential')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
