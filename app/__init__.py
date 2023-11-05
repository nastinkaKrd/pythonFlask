from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "app/static/images/"
configure_uploads(app, photos)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views
