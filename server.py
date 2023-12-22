#server for my travel tracker app

from flask import (Flask, render_template, request, flash, session, redirect)
from flask_login import LoginManager, login_required, login_user, logout_user
from model import connect_to_db, db, User, Destination, Rating, Bucket
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)

#to view homepage
@app.route('/')
def homepage():

    return render_template('homepage.html')

#to view all destinations
@app.route("/destinations")
@login_required
def all_destinations():

    destinations = crud.get_destinations()

    return render_template("all_destinations.html", destinations=destinations)

# #to view destination details
# @app.route("/destinations/<destination_id>")
# def show_destination(destination_id):

#     destination = crud.get_destination_by_id(destination_id)

#     return render_template("destination_details.html", destination=destination)

#to create a new user
@app.route("/users", methods=["POST"])
def register_user():

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_by_email(email)
    if user:
        flash("This email already exists. Please try again.")
    else:
        user = User.create(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now logged in.")

    return redirect("/")


#how user logs in
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("email")
    password = request.form.get("password")
    user = User.get_by_email(email)

    
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")

        # if form.validate_on_submit():
        #     login_user(user)

        #     flash('Logged in successfully.')

    else:
        login_user(user)
        flash('Logged in successfully.')
        
    return redirect("/")

#update destination rating
@app.route("/update_rating", methods=["POST"])
@login_required
def update_rating():
    rating_id = request.json["rating_id"]
    updated_score = request.json["updated_score"]
    Rating.update(rating_id, updated_score)
    db.session.commit()

    return "Success"

#edit destination rating
@app.route("/destinations/<destination_id>/ratings_update", methods=["POST"])
@login_required
def edit_rating(destination_id):

    return redirect(f"/destinations")

#create destination rating
@app.route("/destinations/<destination_id>/ratings", methods=["POST"])
@login_required
def create_rating(destination_id):

    logged_in_email = session.get("user_email")
    rating_score = request.form.get("rating")

    if logged_in_email is None:
        flash("Please log in to rate a destination.")
    elif not rating_score:
        flash("Error: please select a rating score.")
    else:
        user = User.get_by_email(logged_in_email)
        destination = Destination.get_by_id(destination_id)
        rated_destination_city = destination.city
        rated_destination_country = destination.country

        rating = Rating.create(user, destination, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated {rated_destination_city}, {rated_destination_country} {rating_score} out of 5.")


    return redirect(f"/destinations")

#add to bucket list page
@app.route("/destinations/<destination_id>/bucket", methods=["POST"])
@login_required
def add_to_bucket(destination_id):

    logged_in_email = session.get("user_email")
    bucket_checkbox = request.form.get("bucket")

    if logged_in_email is None:
        flash("Please log in to rate a destination.")
    # elif bucket_checkbox is not None:
    else:

        user = User.get_by_email(logged_in_email)
        destination = Destination.get_by_id(destination_id)
        rated_destination_city = destination.city
        rated_destination_country = destination.country

        bucket = Bucket.create(user, destination, bool(bucket_checkbox))
        db.session.add(bucket)
        db.session.commit()

        flash(f"You added {rated_destination_city}, {rated_destination_country} to your bucket list.")

    return redirect(f"/destinations")

#to view been there page
@app.route("/been_there/<user_id>")
@login_required
def been_there_destinations(user_id):

    # logged_in_email = request.form.get("email")
    # user = User.get_by_email(logged_in_email)
    user = User.get_by_id(user_id)

    return render_template("been_there.html", user=user)

#to view bucket list page
@app.route("/bucket_list/<user_id>")
@login_required
def bucket_list_destinations(user_id):

    # logged_in_email = request.form.get("email")
    # user = User.get_by_email(logged_in_email)
    user = User.get_by_id(user_id)

    return render_template("bucket_list.html", user=user)

#to remove from bucket list
@app.route("/destinations/<bucket_id>/bucket_remove", methods=["POST"])
@login_required
def remove_from_bucket(bucket_id):

    logged_in_email = session.get("user_email")
    remove_bucket = request.form.get("remove")

    if logged_in_email is None:
        flash("Please log in to update bucket list.")
    # elif bucket_checkbox is not None:
    else:

        user = User.get_by_email(logged_in_email)
        bucket = Bucket.get_by_id(bucket_id)
        rated_destination_city = bucket.destination.city
        rated_destination_country = bucket.destination.country

        bucket_remove = Bucket.query.get(bucket_id)
        db.session.delete(bucket_remove)
        db.session.commit()

        flash(f"You removed {rated_destination_city}, {rated_destination_country} from your bucket list.")

    return render_template("bucket_list.html", user=user)

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect('/')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)