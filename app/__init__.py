from flask import Flask
from config import Config
from flask_mail import Mail
from flask_jwt_extended import JWTManager

from .models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # with app.app_context():
    #     db.create_all()  # This creates tables based on your models

    mail = Mail(app)
    jwt = JWTManager(app)

    from app.auth.views import auth_bp
    from app.post.views import post_bp
    from app.comment.views import comment_bp
    from app.save.views import save_bp
    from app.mood.views import mood_bp
    from app.opendata.views import opendata_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(post_bp, url_prefix='/posts')
    app.register_blueprint(comment_bp, url_prefix='/comments')
    app.register_blueprint(save_bp, url_prefix='/saves')
    app.register_blueprint(mood_bp, url_prefix='/moods')
    app.register_blueprint(opendata_bp, url_prefix='/opendatas')

    return app
