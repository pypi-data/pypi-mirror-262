from repositories.post import PostRepository
from utils.formatters import object_as_dict


class PostService:
    def __init__(self):
        self.repository = PostRepository()

    def get_posts(self, **filters):
        return [object_as_dict(i) for i in self.repository.get_list_items_by_filter(**filters)]

    def get_post(self, **filters):
        return object_as_dict(self.repository.get_item_by_filter(**filters))

    def create_post(self, data):
        return object_as_dict(self.repository.create(**data))

    def update_post(self, _id: int, data):
        return object_as_dict(self.repository.update_by_id(_id, **data))

    def delete_post(self, _id: int):
        self.repository.delete_by_id(_id)


post_service = PostService()
