from .artist import artist_bp
from .auth import auth_bp
from .main import main_bp
from .movie import movie_bp

__all__ = ["auth_bp", "main_bp", "movie_bp", "artist_bp"]
