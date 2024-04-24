from enum import Enum
from typing import Optional, Union, List, Annotated
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, HTTPException, status, Response, Depends, Query
import models
from utils import get_current_user
from fastapi import UploadFile, File
from PIL import Image
import secrets
import json

router = APIRouter(tags=["Blog"])


@router.get("/get_blog/")
async def get_blog():
    return await models.Blog_Pydantic.from_queryset(models.BlogModel.all())


@router.post("/create_blog/", status_code=status.HTTP_201_CREATED)
async def create_blog(blog: models.BlogIn_Pydantic = Depends(),
                      curr: models.User_Pydantic = Depends(get_current_user)):
    data = blog.dict()
    blog1 = await models.BlogModel.create(title=data["title"], content=data["content"], category=data["category"],
                                          owner_id=int(curr.id))
    return await models.BlogIn_Pydantic.from_tortoise_orm(blog1)


@router.post('/create_image/{pk}/')
async def create_image(pk: int, file: UploadFile = File(...)):
    FILEPATH = './static/blog/'
    filename = file.filename
    extension = filename.split(".")[-1]
    if extension not in ['png', 'jpg']:
        return {"error": 'File extension not allowed'}
    token_name = secrets.token_hex(10) + '.' + extension
    genereted_name: str = FILEPATH + token_name
    file_content = await file.read()
    with open(genereted_name, 'wb') as file:
        file.write(file_content)

    img = Image.open(genereted_name)
    img = img.resize(size=(200, 200))
    img.save(genereted_name)
    file.close()
    model = models.BlogModel.filter(id=pk).first()
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        await model.update(image=token_name)
    return {'message': 'Successfully uploaded image'}
