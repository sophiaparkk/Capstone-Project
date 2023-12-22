#seeding database means to populate databased with existing data. This uses crud file to input.

import os
import json
from random import choice, randint

import crud
import model
import server
# from server import app

os.system('dropdb -U postgres ratings')
os.system('createdb -U postgres ratings')
os.system('dropdb -U postgres bucket')
os.system('createdb -U postgres bucket')


model.connect_to_db(server.app)
model.db.create_all()

with open("data/destinations.json") as f:
    destination_data = json.loads(f.read())

#we are storing movies from file above into list below
destinations_in_db = []
for destination in destination_data:
    city, country, image_path = (
        destination["city"],
        destination["country"],
        destination["image_path"],
    )

    db_destination = crud.create_destination(city, country, image_path)
    destinations_in_db.append(db_destination)

model.db.session.add_all(destinations_in_db)
model.db.session.commit()

for n in range(10):
    email = f"user{n}@test.com"
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

    for _ in range(10):
        random_destination = choice(destinations_in_db)
        score = randint(1, 5)

        rating = crud.create_rating(user, random_destination, score)
        model.db.session.add(rating)

model.db.session.commit()