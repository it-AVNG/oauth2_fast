from app.api.schemas import User
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import logging
from app.logs.log_setup import log

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@log
def fake_decode_token(token):
    '''decode faketoken'''
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

@log
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    '''getuser via decode token'''
    func_logger = logging.getLogger(f'app.api.service.{__name__}')
    func_logger.info('Get User')
    try:
        user = fake_decode_token(token)
        return user
    except Exception as e:
        func_logger.exception(e)
        return {"Error": "System Error - check logs"}

