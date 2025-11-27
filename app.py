from flask import Flask, render_template, request, redirect, url_for, flash, session
from data_manager import DataManager
from models import db, User, Movie
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database with app
db.init_app(app)

# Create data manager instance
data_manager = DataManager()

# Create all database tables on startup
with app.app_context():
	db.create_all()


@app.route('/')
def index():
	"""Display all users and allow user selection or creation."""
	users = data_manager.get_users()
	return render_template('index.html', users=users)


@app.route('/users', methods=['GET', 'POST'])
def manage_users():
	"""GET: List all users (test route). POST: Create a new user."""
	if request.method == 'POST':
		# Handle user creation
		name = request.form.get('name', '').strip()
		
		if not name:
			flash('Please enter a user name.', 'error')
			return redirect(url_for('index'))
		
		try:
			data_manager.create_user(name)
			flash(f'User "{name}" created successfully!', 'success')
		except Exception as e:
			flash(f'Error creating user: {str(e)}', 'error')
		
		return redirect(url_for('index'))
	
	# GET: Return list of users as string (for testing)
	users = data_manager.get_users()
	return str(users)


@app.route('/add_user', methods=['POST'])
def create_user():
	"""Create a new user (POST only)."""
	name = request.form.get('name', '').strip()
	
	if not name:
		flash('Please enter a user name.', 'error')
		return redirect(url_for('index'))
	
	try:
		data_manager.create_user(name)
		flash(f'User "{name}" created successfully!', 'success')
	except Exception as e:
		flash(f'Error creating user: {str(e)}', 'error')
	
	return redirect(url_for('index'))

@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def manage_movies(user_id):
	"""GET: Display movies for a user. POST: Add a new movie."""
	user = data_manager.get_user_by_id(user_id)
	
	if not user:
		flash('User not found.', 'error')
		return redirect(url_for('index'))
	
	if request.method == 'POST':
		# Handle adding a new movie
		name = request.form.get('name', '').strip()
		director = request.form.get('director', '').strip()
		year = request.form.get('year', '')
		poster_url = request.form.get('poster_url', '').strip()
		
		# If name is provided but director/year are empty, try to fetch from OMDb
		if name and (not director or not year):
			omdb_data = data_manager.fetch_movie_from_omdb(name)
			
			if omdb_data:
				# Use OMDb data if available
				if not director and omdb_data.get('director'):
					director = omdb_data['director']
				if not year and omdb_data.get('year'):
					year = str(omdb_data['year'])
				if not poster_url and omdb_data.get('poster_url'):
					poster_url = omdb_data['poster_url']
		
		# Validate input
		if not name or not director or not year:
			flash('Please fill in all required fields (or provide a movie title for OMDb lookup).', 'error')
			return render_template('add_movie.html', user_id=user_id)
		
		try:
			year = int(year)
			if year < 1800 or year > 2099:
				raise ValueError('Year must be between 1800 and 2099')
		except ValueError:
			flash('Please enter a valid year.', 'error')
			return render_template('add_movie.html', user_id=user_id)
		
		# Create and add movie
		try:
			new_movie = Movie(name=name, director=director, year=year, poster_url=poster_url or None)
			data_manager.add_movie(user_id, new_movie)
			flash(f'Movie "{name}" added successfully!', 'success')
			return redirect(url_for('manage_movies', user_id=user_id))
		except Exception as e:
			flash(f'Error adding movie: {str(e)}', 'error')
			return render_template('add_movie.html', user_id=user_id)
	
	# GET: Display all movies for the user
	session['user_id'] = user_id
	session['user_name'] = user.name
	
	# Get search query if provided
	query = request.args.get('q', '').strip()
	
	if query:
		movies = data_manager.search_movies(user_id, query)
	else:
		movies = data_manager.get_movies(user_id)
	
	return render_template('movies.html', user=user, movies=movies, query=query, current_user_id=user_id, current_user_name=user.name)


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
	"""GET: Display add movie form. POST: Add a new movie with OMDb integration."""
	user = data_manager.get_user_by_id(user_id)
	
	if not user:
		flash('User not found.', 'error')
		return redirect(url_for('index'))
	
	if request.method == 'POST':
		# Handle adding a new movie
		name = request.form.get('name', '').strip()
		director = request.form.get('director', '').strip()
		year = request.form.get('year', '').strip()
		poster_url = request.form.get('poster_url', '').strip()
		
		# If name is provided but director/year are empty, try to fetch from OMDb
		if name and (not director or not year):
			omdb_data = data_manager.fetch_movie_from_omdb(name)
			
			if omdb_data:
				# Use OMDb data if available
				if not director and omdb_data.get('director'):
					director = omdb_data['director']
				if not year and omdb_data.get('year'):
					year = str(omdb_data['year'])
				if not poster_url and omdb_data.get('poster_url'):
					poster_url = omdb_data['poster_url']
				flash(f'✨ Movie details fetched from OMDb!', 'success')
		
		# Validate input
		if not name or not director or not year:
			flash('Please fill in all required fields (or provide a movie title for OMDb lookup).', 'error')
			return render_template('add_movie.html', user_id=user_id, user=user)
		
		try:
			year = int(year)
			if year < 1800 or year > 2099:
				raise ValueError('Year must be between 1800 and 2099')
		except ValueError:
			flash('Please enter a valid year.', 'error')
			return render_template('add_movie.html', user_id=user_id, user=user)
		
		# Create and add movie
		try:
			new_movie = Movie(name=name, director=director, year=year, poster_url=poster_url or None)
			data_manager.add_movie(user_id, new_movie)
			flash(f'Movie "{name}" added successfully!', 'success')
			return redirect(url_for('manage_movies', user_id=user_id))
		except Exception as e:
			flash(f'Error adding movie: {str(e)}', 'error')
			return render_template('add_movie.html', user_id=user_id, user=user)
	
	# GET: Display the add movie form
	return render_template('add_movie.html', user_id=user_id, user=user)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
	"""GET: Display edit form. POST: Update movie details."""
	movie = Movie.query.get(movie_id)
	
	if not movie or movie.user_id != user_id:
		flash('Movie not found.', 'error')
		return redirect(url_for('manage_movies', user_id=user_id))
	
	if request.method == 'POST':
		# Get form data
		name = request.form.get('name', '').strip()
		director = request.form.get('director', '').strip()
		year = request.form.get('year', '')
		poster_url = request.form.get('poster_url', '').strip()
		
		# Validate input
		if not name or not director or not year:
			flash('Please fill in all required fields.', 'error')
			return render_template('edit_movie.html', movie=movie)
		
		try:
			year = int(year)
			if year < 1800 or year > 2099:
				raise ValueError('Year must be between 1800 and 2099')
		except ValueError:
			flash('Please enter a valid year.', 'error')
			return render_template('edit_movie.html', movie=movie)
		
		# Update movie
		try:
			data_manager.update_movie(movie_id, name=name, director=director, year=year, poster_url=poster_url or None)
			flash(f'Movie "{name}" updated successfully!', 'success')
			return redirect(url_for('manage_movies', user_id=user_id))
		except Exception as e:
			flash(f'Error updating movie: {str(e)}', 'error')
			return render_template('edit_movie.html', movie=movie)
	
	return render_template('edit_movie.html', movie=movie)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie_route(user_id, movie_id):
	"""Delete a movie from a user's list."""
	movie = Movie.query.get(movie_id)
	
	if not movie or movie.user_id != user_id:
		flash('Movie not found.', 'error')
		return redirect(url_for('manage_movies', user_id=user_id))
	
	movie_name = movie.name
	
	try:
		data_manager.delete_movie(movie_id)
		flash(f'Movie "{movie_name}" deleted successfully!', 'success')
	except Exception as e:
		flash(f'Error deleting movie: {str(e)}', 'error')
	
	return redirect(url_for('manage_movies', user_id=user_id))


@app.route('/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
	"""Delete a user and all their movies."""
	user = data_manager.get_user_by_id(user_id)
	
	if not user:
		flash('User not found.', 'error')
		return redirect(url_for('index'))
	
	user_name = user.name
	
	try:
		data_manager.delete_user(user_id)
		# Clear session if deleting current user
		if session.get('user_id') == user_id:
			session.clear()
		flash(f'User "{user_name}" and all their movies deleted successfully!', 'success')
	except Exception as e:
		flash(f'Error deleting user: {str(e)}', 'error')
	
	return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
	"""Handle 404 errors."""
	return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
	"""Handle 500 errors."""
	return render_template('500.html'), 500


if __name__ == '__main__':
	# Only run debug mode locally, not in production
	debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
	app.run(port=5005, debug=debug_mode)
