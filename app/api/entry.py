import sys
import os
import logging
from typing import Annotated
from fastapi import Depends, FastAPI,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
sys.path.append(f'{os.getcwd()}')
from app.logs.log_setup import get_log_config,log
from app.api.service import( get_current_active_user,
                             fake_hash_password)
from app.api.schemas import User,UserInDB
from app.api.fake_db import fake_users_db


get_log_config()

app = FastAPI()

@app.get("/")
def health_check():
    """health check"""
    @log
    def message():
        print('message')

    message()
    return {'Hello': 'world'}

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):

    # logging functional
    func_logger = logging.getLogger(f'{__name__}')
    func_logger.info('logging in')

    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        func_logger.warning('Incorrect username')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        func_logger.warning('Incorrect password')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect username or password")

    func_logger.info('user authenticated')
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    func_logger = logging.getLogger(f'app.entry.{__name__}')
    try:
        return current_user
    except Exception as e:
        func_logger.exception(e)
