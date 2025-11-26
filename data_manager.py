from models import db, User, Movie
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DataManager:
	"""Manages database operations for users and movies."""

	def __init__(self):
		"""Initialize DataManager with OMDb API configuration."""
		self.omdb_api_key = os.environ.get('OMDB_API_KEY')
		self.omdb_api_url = os.environ.get('OMDB_API_URL', 'http://www.omdbapi.com')
		self.api_timeout = 10  # seconds

	def fetch_movie_from_omdb(self, title):
		"""Fetch movie information from OMDb API.
		
		Args:
			title (str): The title of the movie to search for
			
		Returns:
			dict: Dictionary with keys 'name', 'director', 'year', 'poster_url'
				  Returns empty dict if API fails or movie not found
		"""
		if not self.omdb_api_key:
			return {}
		
		try:
			params = {
				'apikey': self.omdb_api_key,
				't': title,
				'type': 'movie'
			}
			
			response = requests.get(
				self.omdb_api_url,
				params=params,
				timeout=self.api_timeout
			)
			response.raise_for_status()
			
			data = response.json()
			
			# Check if movie was found
			if data.get('Response') == 'False':
				return {}
			
			# Extract relevant fields
			result = {
				'name': data.get('Title', ''),
				'director': data.get('Director', ''),
				'year': int(data.get('Year', 0)) if data.get('Year', '').isdigit() else 0,
				'poster_url': data.get('Poster') if data.get('Poster') != 'N/A' else None
			}
			
			return result
			
		except requests.exceptions.Timeout:
			# API request timed out
			return {}
		except requests.exceptions.ConnectionError:
			# Connection failed
			return {}
		except Exception as e:
			# Other errors
			return {}

	def create_user(self, name):
		"""Add a new user to the database.
		
		Args:
			name (str): The name of the user
			
		Returns:
			User: The created user object
		"""
		new_user = User(name=name)
		db.session.add(new_user)
		db.session.commit()
		return new_user

	def get_users(self):
		"""Return a list of all users in the database.
		
		Returns:
			list: List of User objects
		"""
		return User.query.all()

	def get_user_by_id(self, user_id):
		"""Get a specific user by ID.
		
		Args:
			user_id (int): The user's ID
			
		Returns:
			User: The user object or None if not found
		"""
		return User.query.get(user_id)

	def get_movies(self, user_id):
		"""Return a list of all movies of a specific user.
		
		Args:
			user_id (int): The user's ID
			
		Returns:
			list: List of Movie objects for the user
		"""
		user = User.query.get(user_id)
		if user:
			return user.movies
		return []

	def add_movie(self, user_id, movie):
		"""Add a new movie to a user's favorites.
		
		Args:
			user_id (int): The user's ID
			movie (Movie): A Movie object with name, director, year, poster_url
			
		Returns:
			Movie: The created movie object or None if user not found
		"""
		user = User.query.get(user_id)
		if not user:
			return None
		
		movie.user_id = user_id
		db.session.add(movie)
		db.session.commit()
		return movie

	def update_movie(self, movie_id, **kwargs):
		"""Update the details of a specific movie in the database.
		
		Args:
			movie_id (int): The movie's ID
			**kwargs: Fields to update (name, director, year, poster_url)
			
		Returns:
			Movie: The updated movie object or None if not found
		"""
		movie = Movie.query.get(movie_id)
		if not movie:
			return None
		
		# Update fields if provided
		if 'name' in kwargs:
			movie.name = kwargs['name']
		if 'director' in kwargs:
			movie.director = kwargs['director']
		if 'year' in kwargs:
			movie.year = kwargs['year']
		if 'poster_url' in kwargs:
			movie.poster_url = kwargs['poster_url']
		
		db.session.commit()
		return movie

	def delete_movie(self, movie_id):
		"""Delete a movie from the database.
		
		Args:
			movie_id (int): The movie's ID
			
		Returns:
			bool: True if deleted, False if movie not found
		"""
		movie = Movie.query.get(movie_id)
		if not movie:
			return False
		
		db.session.delete(movie)
		db.session.commit()
		return True

	def delete_user(self, user_id):
		"""Delete a user and all their movies from the database.
		
		Args:
			user_id (int): The user's ID
			
		Returns:
			bool: True if deleted, False if user not found
		"""
		user = User.query.get(user_id)
		if not user:
			return False
		
		db.session.delete(user)
		db.session.commit()
		return True
