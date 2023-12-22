#database models for my travel tracker app
import os
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_login import UserMixin


db = SQLAlchemy()

class User(db.Model, UserMixin):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"
    
    def get_id(self):
        return self.user_id
    
    #where we create and return a new user
    @classmethod
    def create(cls, email, password):

       return cls(email=email, password=password)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(User.email == email).first()

    @classmethod
    def all_users(cls):
        return cls.query.all()

    

class Destination(db.Model):

    __tablename__ = "destinations"

    destination_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city = db.Column(db.String)
    country = db.Column(db.String)
    image_path = db.Column(db.String)



    def __repr__(self):
        return f"<Destination destination_id={self.destination_id} city={self.city}, country={self.country}>"
    
    #to add a new destination
    @classmethod
    def create(cls, city, country, image_path):

        return cls(
            city=city,
            country=country,
            image_path=image_path,
            )
    
    @classmethod
    def all_destinations(cls):

        return cls.query.all()

    @classmethod
    def get_by_id(cls, destination_id):

        return cls.query.get(destination_id)
    

class Rating(db.Model):

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.destination_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    destination = db.relationship("Destination", backref="ratings")
    image_path = db.relationship("Destination", backref="ratings_image")
    user = db.relationship("User", backref="ratings")


    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"
    
    @classmethod
    def create(cls, user, destination, score):

        return cls(user=user, destination=destination, score=score)

    @classmethod
    def update(cls, rating_id, new_rating):
        new_score = cls.query.get(rating_id)
        new_score.score = new_rating




class Bucket(db.Model):

    __tablename__ = "bucket"

    bucket_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    bucketed = db.Column(db.Boolean)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.destination_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    destination = db.relationship("Destination", backref="bucket")
    image_path = db.relationship("Destination", backref="bucket_image")
    user = db.relationship("User", backref="bucket")


    def __repr__(self):
        return f"<Bucket bucket_id={self.bucket_id} bucketed={self.bucketed}>"
    
    @classmethod
    def create(cls, user, destination, bucketed):

        return cls(user=user, destination=destination, bucketed=bucketed)

    @classmethod
    def update(cls, bucket_id, new_add):
        added = cls.query.get(bucket_id)
        added.bucketed = new_add

    @classmethod
    def get_by_id(cls, bucket_id):

        return cls.query.get(bucket_id)



def connect_to_db(flask_app, db_uri=os.environ["DATABASE_URI"], echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")



if __name__ == "__main__":
    from server import app

    connect_to_db(app)