from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
	"""User model for storing user information."""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	
	# Relationship to movies (one user can have many movies)
	movies = db.relationship('Movie', backref='user', lazy=True, cascade='all, delete-orphan')
	
	def __repr__(self):
		return f'<User {self.name}>'


class Movie(db.Model):
	"""Movie model for storing movie information."""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	director = db.Column(db.String(100), nullable=False)
	year = db.Column(db.Integer, nullable=False)
	poster_url = db.Column(db.String(500), nullable=True)
	
	# Link Movie to User (foreign key)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	def __repr__(self):
		return f'<Movie {self.name} ({self.year})>'
