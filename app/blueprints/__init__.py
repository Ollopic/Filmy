from .auth import auth_bp
from .collection import collection_bp
from .main import main_bp
from .movie import movie_bp
from .person import person_bp

__all__ = ["auth_bp", "main_bp", "movie_bp", "person_bp", "collection_bp"]
