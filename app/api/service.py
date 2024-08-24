from os import stat
from app.api.schemas import User,UserInDB
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated
import logging
from app.api.fake_db import fake_users_db
from app.logs.log_setup import log

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@log
def fake_hash_password(password: str):
    '''fake hasshing'''
    return "fakehashed" + password

@log
def get_user(db, username: str):
    '''simulate get user in DB'''
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


@log
def fake_decode_token(token):
    '''fakedecode token'''
    user = get_user(fake_users_db, token)
    return user

@log
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    '''getuser via decode token'''

    #add logging
    func_logger = logging.getLogger(f'app.api.service.{__name__}')
    func_logger.info('Get current User')

    try:
        # call decode to return User
        user = fake_decode_token(token)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return user
    except Exception as e:
        func_logger.exception(e)
        return e

@log
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    # add logging
    func_logger = logging.getLogger(f'app.api.service.{__name__}')
    func_logger.info('Get active User')
    try:
        if current_user.disabled:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= "Inactive user"
            )
        return current_user
    except Exception as e:
        func_logger.exception(e)
        return e


