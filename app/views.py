from pathlib import Path
from flask import render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename

from . import app, db
from .models import Review, Movie
from .forms import FilmForm, FilmForm, ReviewForm

BASEDIR = Path(__file__).parent
UPLOAD_FOLDER = BASEDIR / 'static' / 'images'

@app.route('/')
def index():
    movies = Movie.query.order_by(Movie.id.desc()).all()
    return render_template('index.html', movies=movies)


@app.route('/film_detail/<int:id>', methods=['GET', 'POST'])
def movie(id):
    movie = Movie.query.get(id)
    if movie.reviews:
        avg_score = round(sum(review.score for review in movie.reviews) / len(movie.reviews), 2)
    else:
        avg_score = 0
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review()
        review.name = form.name.data
        review.text = form.text.data
        review.score = form.score.data
        review.movie_id = movie.id
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('movie', id=movie.id))
    return render_template('movie.html', movie=movie, avg_score=avg_score, form=form)


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    form = FilmForm()
    if form.validate_on_submit():
        movie = Movie()
        movie.title = form.title.data
        movie.image = form.image.data
        movie.description = form.description.data
        image = form.image.data
        image_name = secure_filename(image.filename)
        image.save(UPLOAD_FOLDER / image_name)
        movie.image = image_name
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('movie', id=movie.id))
    return render_template('add_movie.html', form=form)


@app.route('/reviews')
def reviews():
    reviews = Review.query.order_by(Review.created_date.desc()).all()
    return render_template('reviews.html', reviews=reviews)

@app.route('/delete_review/<int:id>')
def delete_review(id):
    review = Review.query.get(id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('reviews'))