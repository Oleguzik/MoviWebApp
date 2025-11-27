# 🎬 MoviWebApp

A modern, full-stack Flask web application for managing personal movie collections with external API integration, responsive design, and deployment-ready architecture.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📸 Screenshots

<details>
<summary>Click to view screenshots</summary>

### Home Page - User Management
Beautiful gradient design with user cards and movie counts.

### Movie Collection
Grid layout with movie posters, director info, and action buttons.

### Add Movie with OMDb Integration
Auto-fetch movie details including poster from OMDb API.

</details>

---

## ✨ Features

### Core Functionality
- **👤 Multi-User Support** - Create and manage multiple user profiles
- **🎥 Movie Collections** - Each user maintains their own favorite movies list
- **🔍 Smart Search** - Search movies by title or director
- **✏️ Full CRUD Operations** - Create, Read, Update, Delete for users and movies

### External API Integration
- **🎬 OMDb API Integration** - Auto-fetch movie details (director, year, poster)
- **🖼️ Movie Posters** - Automatic poster images from OMDb database
- **⚡ Smart Auto-Fill** - Just enter movie title, we fetch the rest!

### Modern UI/UX
- **🎨 Beautiful Design** - Modern gradient backgrounds and card layouts
- **📱 Fully Responsive** - Mobile-first design, works on all devices
- **🔔 Flash Messages** - User-friendly feedback for all actions
- **✨ Smooth Animations** - CSS transitions and hover effects
- **🎯 Font Awesome Icons** - Professional iconography throughout
- **🍞 Breadcrumb Navigation** - Easy navigation across pages

### Technical Excellence
- **🏗️ MVC Architecture** - Clean separation of concerns
- **🗃️ SQLAlchemy ORM** - Robust database management
- **🔒 Secure Configuration** - Environment variables for secrets
- **🚀 Production Ready** - WSGI configured for deployment

---

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| **Backend** | Python 3.9+, Flask 3.1 |
| **Database** | SQLite, SQLAlchemy 2.0 |
| **Frontend** | Jinja2, HTML5, CSS3 |
| **Styling** | Custom CSS, Font Awesome 6, Google Fonts |
| **API** | OMDb API (movie data) |
| **Deployment** | PythonAnywhere, WSGI |

---

## 📁 Project Structure

```
MoviWebApp/
├── app.py                 # Main Flask application & routes
├── models.py              # SQLAlchemy database models
├── data_manager.py        # Data access layer & OMDb integration
├── wsgi.py                # WSGI entry point for deployment
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in repo)
│
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Base layout with navigation
│   ├── index.html         # Home page - user list
│   ├── movies.html        # User's movie collection
│   ├── add_movie.html     # Add movie form
│   ├── edit_movie.html    # Edit movie form
│   ├── 404.html           # Custom error page
│   └── 500.html           # Custom error page
│
├── static/
│   └── styles.css         # Modern CSS with animations
│
├── data/
│   └── movies.db          # SQLite database
│
└── docs/                  # Documentation
    ├── PROJECT_OVERVIEW.md
    ├── API_REFERENCE.md
    ├── DATABASE_SCHEMA.md
    ├── DEVELOPMENT_GUIDE.md
    ├── DEPLOYMENT_GUIDE.md
    └── AGENT_SESSION_GUIDE.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- OMDb API key (free at [omdbapi.com](http://www.omdbapi.com/apikey.aspx))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Oleguzik/MoviWebApp.git
   cd MoviWebApp
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env file
   echo "SECRET_KEY=your-secret-key-here" > .env
   echo "OMDB_API_KEY=your-omdb-api-key" >> .env
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://127.0.0.1:5005
   ```

---

## 🌐 API Routes

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/` | Home page - list all users |
| `POST` | `/add_user` | Create a new user |
| `GET` | `/users/<id>/movies` | View user's movie collection |
| `GET/POST` | `/users/<id>/add_movie` | Add movie form / submit |
| `GET/POST` | `/users/<id>/movies/<mid>/update` | Edit movie |
| `POST` | `/users/<id>/movies/<mid>/delete` | Delete movie |
| `POST` | `/user/<id>/delete` | Delete user |

---

## 🗃️ Database Schema

```
┌─────────────────┐       ┌─────────────────────┐
│      User       │       │       Movie         │
├─────────────────┤       ├─────────────────────┤
│ id (PK)         │───┐   │ id (PK)             │
│ name            │   │   │ name                │
└─────────────────┘   │   │ director            │
                      │   │ year                │
                      │   │ poster_url          │
                      └──▶│ user_id (FK)        │
                          └─────────────────────┘
                          
Relationship: One User → Many Movies
Cascade: Delete user removes all their movies
```

---

## 🎯 Key Implementation Highlights

### 1. OMDb API Integration
```python
def fetch_movie_from_omdb(self, title):
    """Auto-fetch movie details from OMDb API."""
    response = requests.get(self.omdb_api_url, params={
        'apikey': self.omdb_api_key,
        't': title,
        'type': 'movie'
    })
    # Returns: name, director, year, poster_url
```

### 2. SQLAlchemy Relationships
```python
class User(db.Model):
    movies = db.relationship('Movie', backref='user', 
                            cascade='all, delete-orphan')

class Movie(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
```

### 3. Error Handling
- Custom 404 and 500 error pages
- Try-except blocks for database operations
- API timeout handling
- User-friendly flash messages

---

## 🚀 Deployment

The application is deployment-ready for PythonAnywhere:

1. **WSGI Configuration** - `wsgi.py` included
2. **Environment Variables** - Secure configuration
3. **Production Mode** - Debug disabled in production
4. **Static Files** - Properly organized

See [`docs/DEPLOYMENT_GUIDE.md`](docs/DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## 📚 Documentation

Comprehensive documentation available in `/docs`:

- **[PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md)** - Architecture & quick start
- **[API_REFERENCE.md](docs/API_REFERENCE.md)** - Route & method documentation
- **[DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md)** - ERD & table definitions
- **[DEVELOPMENT_GUIDE.md](docs/DEVELOPMENT_GUIDE.md)** - Setup & debugging
- **[DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** - PythonAnywhere deployment

---

## 🧪 Code Quality

- ✅ **PEP8 Compliant** - Follows Python style guidelines
- ✅ **Type Hints Ready** - Clean function signatures
- ✅ **Documented** - Docstrings for all functions
- ✅ **Error Handling** - Comprehensive exception handling
- ✅ **Security** - Environment variables for secrets

---

## 🔮 Future Enhancements

- [ ] User authentication (login/register)
- [ ] Movie ratings and reviews
- [ ] Watch history tracking
- [ ] Movie recommendations
- [ ] Export/import collections
- [ ] Social sharing features

---

## 👨‍💻 Author

**Oleg Uzik**

- GitHub: [@Oleguzik](https://github.com/Oleguzik)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [OMDb API](http://www.omdbapi.com/) - Movie data provider
- [Font Awesome](https://fontawesome.com/) - Icons
- [Google Fonts](https://fonts.google.com/) - Poppins font
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM

---

<p align="center">
  Made with ❤️ and Python
</p>