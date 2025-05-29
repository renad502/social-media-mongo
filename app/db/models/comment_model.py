from bson import ObjectId
from datetime import datetime

def comment_helper(comment) -> dict:
    return {
        "id": str(comment["_id"]),
        "post_id": str(comment["post_id"]),
        "author_id": str(comment["author_id"]),
        "content": comment["content"],
        "created_at": comment["created_at"]
    }
