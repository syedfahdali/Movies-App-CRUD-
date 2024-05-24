from flask import Blueprint, request, render_template, redirect, url_for, flash
import logging
from database.models import Movie, Category, db

API_bp = Blueprint('API_bp', __name__,template_folder='templates')

# Route to render the create movie form
@API_bp.route('/add_movie', methods=['GET'])
def add_movie_form():
    return render_template('create_movie.html')

# Route to create a new movie
@API_bp.route('/create_movie', methods=['POST'])
def create_movie():
    try:
        movie_status = request.form.get("movie_status")
        movie_name = request.form.get("movie_name")
        category_name = request.form.get("category_name")

        if not movie_status or not movie_name or not category_name:
            flash("All fields are required", "error")
            return redirect(url_for('API_bp.add_movie_form'))

        # Check if the category already exists
        category = db.session.query(Category).filter_by(name=category_name).first()

        # If category does not exist, create a new category
        if category is None:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()

        # Create a new movie with the category's ID
        movie = Movie(category_id=category.id, movie_status=movie_status, name=movie_name)
        db.session.add(movie)
        db.session.commit()

        flash(f"Movie added: {movie.name}", "success")
        return redirect(url_for('home_page_bp.home_page'))
    except Exception as e:
        logging.exception(e)
        flash("An error occurred while adding the movie", "error")
        return redirect(url_for('API_bp.add_movie_form'))


    
@API_bp.route('/get_all_movies', methods=['GET'])
def get_all_movies():
    try:
        # Query all movies from the database
        movies = db.session.query(Movie).all()

        # Extract the names of all movies
        movie_names = [movie.name for movie in movies]

        return {"movies": movie_names}
    except Exception as e:
        logging.exception(e)
        return {"error": "Internal Server Error"}, 500
