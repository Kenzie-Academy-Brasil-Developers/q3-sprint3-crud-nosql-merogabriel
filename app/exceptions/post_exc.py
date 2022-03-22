class PostNotFoundError(Exception):
    message = {"error": "Post doesn't exist"}
    status_code = 404

class InvalidRequestError(Exception):
    message = {"error": "Invalid request"}
    status_code = 400
