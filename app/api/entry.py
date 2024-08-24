import sys
import os
from typing import Union
from fastapi import FastAPI
sys.path.append(f'{os.getcwd()}')
from app.logs.log_setup import get_log_config,log

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