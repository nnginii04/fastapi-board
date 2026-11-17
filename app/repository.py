from typing import Any


class PostNotFoundError(Exception):
    def __init__(self, post_id: int) -> None:
        super().__init__(f"Post {post_id} not found")
        self.post_id = post_id


class PostRepository:
    """In-memory post store backed by a dict keyed by post id."""

    def __init__(self) -> None:
        self._posts: dict[int, dict[str, Any]] = {}
        self._next_id = 1

    def _require(self, post_id: int) -> dict[str, Any]:
        post = self._posts.get(post_id)
        if post is None:
            raise PostNotFoundError(post_id)
        return post

    def create(self, fields: dict[str, Any]) -> dict[str, Any]:
        post_id = self._next_id
        self._next_id += 1
        self._posts[post_id] = {"id": post_id, **fields}
        return dict(self._posts[post_id])

    def get(self, post_id: int) -> dict[str, Any]:
        return dict(self._require(post_id))

    def replace(self, post_id: int, fields: dict[str, Any]) -> dict[str, Any]:
        self._require(post_id)
        self._posts[post_id] = {"id": post_id, **fields}
        return dict(self._posts[post_id])

    def patch(self, post_id: int, fields: dict[str, Any]) -> dict[str, Any]:
        post = self._require(post_id)
        post.update(fields)
        return dict(post)

    def delete(self, post_id: int) -> None:
        self._require(post_id)
        del self._posts[post_id]
