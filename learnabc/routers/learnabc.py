from typing import List
from fastapi import APIRouter, Depends, status, HTTPException


router = APIRouter(
    prefix='',
    tags=['Blogs']
)