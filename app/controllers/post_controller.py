from flask import jsonify, request

from app.exceptions import PostNotFoundError, InvalidRequestError

from app.models.post_model import Post

from app.services.post_model_services import verify_types,verify_patch_request


def get_posts():
    posts_list = Post.get_all()

    posts_list = list(posts_list)

    for post in posts_list:
        Post.serialize_post(post)

    return jsonify(posts_list), 200


def create_post():
    data = request.get_json()

    try:
        if not verify_types(data):
            raise InvalidRequestError  

        post = Post(**data)

        post.create_post()

        serialized_post = Post.serialize_post(post)

        return serialized_post.__dict__, 201 

    except InvalidRequestError:

        return InvalidRequestError.message, InvalidRequestError.status_code



def get_post_by_id(id):
    try:
        post = Post.get_by_id(id)

        if not post: 
            raise PostNotFoundError

        serialized_post = Post.serialize_post(post)

        return serialized_post, 200
        
    except PostNotFoundError:
        return PostNotFoundError.message, PostNotFoundError.status_code


def update_post(id):
    data = request.get_json()

    try:
        if not verify_patch_request(data):
            raise InvalidRequestError

        updated_post = Post.update_post(id, verify_patch_request(data))

        if not updated_post: 
            raise PostNotFoundError

        serialized_post = Post.serialize_post(updated_post)

        return serialized_post, 200

    except InvalidRequestError:
        return InvalidRequestError.message, InvalidRequestError.status_code

    except PostNotFoundError:
        return PostNotFoundError.message, PostNotFoundError.status_code


def delete_post(id):
    try:
        deleted_post = Post.delete_post(id)

        if not deleted_post: 
            raise PostNotFoundError

        Post.serialize_post(deleted_post)

        return deleted_post, 200

    except PostNotFoundError:
        return PostNotFoundError.message, PostNotFoundError.status_code
