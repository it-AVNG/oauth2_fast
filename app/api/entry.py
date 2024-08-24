import sys
import os
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

sys.path.append(f'{os.getcwd()}')
from app.logs.log_setup import get_log_config,log


get_log_config()

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def health_check():
    """health check"""
    @log
    def message():
        print('message')

    message()
    return {'Hello': 'world'}

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}