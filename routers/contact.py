from fastapi import APIRouter, HTTPException, status, Response, Depends
import models
from utils import get_current_user

router = APIRouter(tags=['Contact'])


@router.get('/get_contacts/')
async def get_contacts():
    return await models.Contact_Pydantic.from_queryset(models.ContactModel.all())


@router.post('/create_contact/', status_code=status.HTTP_201_CREATED)
async def create_contact(contact: models.ContactIn_Pydantic = Depends(get_current_user)):
    contact = await models.ContactModel.create(**contact.model_dump(exclude_unset=True))
    return await models.ContactIn_Pydantic.from_tortoise_orm(contact)
