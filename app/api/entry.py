import sys
import os
import logging
from typing import Annotated
from fastapi import Depends, FastAPI

sys.path.append(f'{os.getcwd()}')
from app.logs.log_setup import get_log_config,log
from app.api.service import get_current_user
from app.api.schemas import User


get_log_config()

app = FastAPI()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def health_check():
    """health check"""
    @log
    def message():
        print('message')

    message()
    return {'Hello': 'world'}

# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    func_logger = logging.getLogger(f'app.entry.{__name__}')
    try:
        return current_user
    except Exception as e:
        func_logger.exception(e)
