#this page is for the CRUD operations for existing data that we imported used in seed database file

from model import db, User, Destination, Rating, connect_to_db

def create_user(email, password):

    user = User(email=email, password=password)

    return user



def create_destination(city, country, image_path):

    destination = Destination(
        city=city,
        country=country,
        image_path=image_path,
    )

    return destination

def get_destinations():

    return Destination.query.all()

def create_rating(user, destination, score):

    rating = Rating(user=user, destination=destination, score=score)

    return rating

def get_destination_by_id(destination_id):

    return Destination.query.get(destination_id)

def get_user_by_email(email):

    return User.query.filter(User.email == email).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
