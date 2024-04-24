import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
import models
import main

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
JWT_SECRET = 'myjwtsecret'


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await models.UserModel.get(id=payload.get('id'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')
    return await models.User_Pydantic.from_tortoise_orm(user)
