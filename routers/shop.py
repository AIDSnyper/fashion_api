from fastapi import APIRouter, Depends, HTTPException, status
import models

router = APIRouter(tags=['Shop'])
