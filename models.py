from enum import Enum
from pydantic import BaseModel
from passlib.hash import bcrypt
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields import ForeignKeyField
from tortoise.models import Model
from tortoise import fields, Tortoise
from typing import List, Annotated


class Category(Model):
    cat = fields.CharField(max_length=44)


class ContactModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=44)
    email = fields.CharField(max_length=44)
    message = fields.CharField(max_length=104)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class BlogModel(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=44)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    category = fields.CharField(max_length=44, null=True)
    owner = fields.ForeignKeyField("models.UserModel", related_name='owner')
    image = fields.CharField(max_length=404, null=True)


class UserModel(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=44)
    password = fields.CharField(max_length=404)
    avatar = fields.CharField(max_length=404, null=True)

    @classmethod
    async def get_user(cls, username):
        return cls.get(username=username)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)


class Comment(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.UserModel", related_name='user', null=True)
    content = fields.TextField()
    blog = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Size(str, Enum):
    xxl = 'xxl'
    xl = 'xl'
    l = 'l'
    s = 's'


class Color(str, Enum):
    black = 'black'
    blue = 'blue'
    yellow = 'yellow'
    green = 'green'
    red = 'red'
    white = 'white'


class ShopModel(BaseModel):
    id = fields.IntField(pk=True)
    image = fields.CharField(max_length=404)
    title = fields.CharField(max_length=44)
    rating = fields.IntField
    price = fields.IntField()
    content = fields.TextField(null=False)
    size = fields.CharField(max_length=404)
    color = fields.CharField(max_length=404)
    number = fields.IntField()
    category = fields.CharField(max_length=404)
    tags = fields.CharField(max_length=404)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


Comment_Pydantic = pydantic_model_creator(Comment, name='Comment', exclude=['id'])
CommentIn_Pydantic = pydantic_model_creator(Comment, name='CommentIN', exclude_readonly=True,
                                            exclude=['created_at', 'updated_at', 'id'])

Contact_Pydantic = pydantic_model_creator(ContactModel, name='Contact')
ContactIn_Pydantic = pydantic_model_creator(ContactModel, name='ContactIN')

Cat_Pydantic = pydantic_model_creator(Category, name='Category')
CatIN_Pydantic = pydantic_model_creator(Category, name='CategoryIn', exclude_readonly=True)

Blog_Pydantic = pydantic_model_creator(BlogModel, name='Blog')
BlogIn_Pydantic = pydantic_model_creator(BlogModel, name='BlogIn', exclude_readonly=True,
                                         exclude=('created_at', 'updated_at', 'image'))
User_Pydantic = pydantic_model_creator(UserModel, name='User')
UserIn_Pydantic = pydantic_model_creator(UserModel, name='UserIn', exclude_readonly=True,
                                         include=('username', 'password', 'role_id'),
                                         exclude=('created_at', 'updated_at', 'avatar'))
