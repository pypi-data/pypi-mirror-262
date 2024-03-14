from repositories.base import BaseRepository
from models.post import Post


class PostRepository(BaseRepository):
    model = Post
