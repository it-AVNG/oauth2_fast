import logging
from typing import Union
from fastapi import FastAPI

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