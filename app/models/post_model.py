from typing import Union
import pymongo

from bson.objectid import ObjectId
import datetime as dt
from pymongo import ReturnDocument

client = pymongo.MongoClient("mongodb://localhost:27017/")

kenzie = client['kenzie']


class Post:
    def __init__(self, title: str, author: str, tags: list, content: str):
        if not len(list(kenzie.posts.find())):
            self.id = 1
        else:
            self.id = list(kenzie.posts.find())[-1]['id']+1
            
        self.created_at = dt.datetime.now()
        self.updated_at = dt.datetime.now()
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content

    @staticmethod
    def serialize_post(post: Union["Post", dict]):
        if type(post) is dict:
            post.update({'_id': str(post['_id'])})
        elif type(post) is Post:
            post._id = str(post._id)
        return post

    @staticmethod
    def get_all():
        posts_list = kenzie.posts.find()

        return posts_list

    def create_post(self):
        kenzie.posts.insert_one(self.__dict__)

    @staticmethod
    def get_by_id(id):
        post = kenzie.posts.find_one({"id": id})

        return post

    @staticmethod
    def update_post(post_id: str, payload:dict):
        updated_post = kenzie.posts.find_one_and_update(
            {"id": post_id},
            {"$set": payload},
            return_document=ReturnDocument.AFTER,
        )
        if updated_post:
            updated_post = kenzie.posts.find_one_and_update(
            {"id": post_id},
            {"$set": {"updated_at": dt.datetime.now()}},
            return_document=ReturnDocument.AFTER,
        )

        return updated_post

    @staticmethod
    def delete_post(id: str):
        deleted_post = kenzie.posts.find_one_and_delete({"id": id})
        return deleted_post