from fastapi import APIRouter, Depends, HTTPException, status
from utils import get_current_user
import models

router = APIRouter(tags=['Comment'])


@router.get('/comments/')
async def get_comments():
    return await models.Comment_Pydantic.from_queryset(models.Comment.all())


@router.post('/create_comment/{id}')
async def create_comment(model: models.CommentIn_Pydantic = Depends(),
                         curr: models.User_Pydantic = Depends(get_current_user)):
    data = model.dict()
    await models.Comment.create(user_id=int(curr.id), content=data['content'], blog=data['blog'])
    raise HTTPException(status_code=status.HTTP_201_CREATED)
