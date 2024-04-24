import secrets

from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from routers import contact, blog, comment
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
import models
import jwt
from utils import get_current_user, JWT_SECRET
from PIL import Image

app = FastAPI(title='Male Fashion', tags=['Male Fashion'], )
app.mount('/static', StaticFiles(directory='static'), name='static')


async def authenticate_user(username: str, password: str):
    user = await models.UserModel.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


@app.post('/token/', tags=['User'])
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        return {'error': 'Incorrect username or password'}
    obj = await models.User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(obj.dict(), JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer'}


@app.post('/users/', response_model=models.User_Pydantic, tags=['User'])
async def create_user(user: models.UserIn_Pydantic = Depends()):
    obj = models.UserModel(username=user.username, password=bcrypt.hash(user.password))
    await obj.save()
    return await models.User_Pydantic.from_tortoise_orm(obj)


@app.get('/users/me/', tags=['User'])
async def get_user_curr(user: models.UserIn_Pydantic = Depends(get_current_user)):
    return user


@app.delete('/delete_user/', tags=['User'])
async def delete_user(curr: models.UserIn_Pydantic = Depends(get_user_curr)):
    await models.UserModel().filter(id=curr.id).delete()
    return {'message': 'User deleted'}

@app.post('/uploadfile/profile', tags=['User'])
async def create_upload_file(file: UploadFile = File(...), user: models.User_Pydantic = Depends(get_current_user)):
    FILEPATH = './static/images/'
    filename = file.filename
    extension = filename.split(".")[-1]
    if extension not in ['png', 'jpg']:
        return {"error": 'File extension not allowed'}
    token_name = secrets.token_hex(10) + '.' + extension
    genereted_name = FILEPATH + token_name
    file_content = await file.read()
    with open(genereted_name, 'wb') as file:
        file.write(file_content)

    img = Image.open(genereted_name)
    img = img.resize(size=(200, 200))
    img.save(genereted_name)
    file.close()

    u = await models.UserModel.filter(id=user.id).update(avatar=token_name)
    return {'message': 'Successfully uploaded'}


app.include_router(contact.router)
app.include_router(blog.router)
app.include_router(comment.router)

TORTOISE_ORM = {
    "connections": {
        "default": 'postgres://fashion_api:fashion_api@localhost/fashion_api'
    },
    "apps": {
        "models": {
            "models": ['aerich.models', 'models'],
            "default_connection": "default",
        },
    },
}
register_tortoise(
    app,
    modules={"models": ["models"]},
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True
)
