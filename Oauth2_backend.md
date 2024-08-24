# Introduction
This is a section where we implement a backend Oauth2 authentication with FastApi.
Implementing the security method base on fastapi documentation [security with Oauth2](https://fastapi.tiangolo.com/tutorial/security/first-steps/)

# Getting started

The `entry.py` has the following endpoints:

```python
...
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
...
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

The password "flow" is one of the ways ("flows") defined in OAuth2, to handle security and authentication.
OAuth2 was designed so that the backend or API could be independent of the server that authenticates the user.

But in this case, the same FastAPI application will handle the API and the authentication.
So, let's review it from that simplified point of view:

+ The user types the `username` and `password` in the frontend, and hits `Enter`.
+ The frontend (or client) sends that `username` and `password` to a **specific URL** in our API (declared with `tokenUrl="token"`). In many case this URL leads to an authenticat server.
+ The API checks that `username` and `password`, and responds with a "token" (we haven't implemented any of this yet).
    + A "token" is just a string with some content that we can use later to verify this user.
    + Normally, a token is set to expire after some time.
        + So, the user will have to log in again at some point later.
        + And if the token is stolen, the risk is less. It is not like a permanent key that will work forever (in most of the cases).

+ The frontend stores that token temporarily somewhere or during runtime.
+ The user clicks in the frontend to go to another section of the frontend web app or in client script, this could be a redirected url.
+ The frontend needs to fetch some more data from the API.
    + But it needs authentication for that specific endpoint.
    + So, to authenticate with our API, it sends a header Authorization with a value of Bearer plus the token.
    + If the token contains `foobar`, the content of the Authorization header would be: `Bearer foobar`.


# FastApi `OAuth2PasswordBearer`
When we create an instance of the `OAuth2PasswordBearer` class we pass in the `tokenUrl` parameter. This parameter contains the URL that the client will use to send the `username` and `password` in order to get a token.

## `oauth2_scheme` variable:
The `oauth2_scheme` variable is an instance of `OAuth2PasswordBearer`, but it is also a "callable". the syntax could be `oauth2_scheme(some, parameters)`.
So, it can be used with `Depends`

```python
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

This dependency will provide a str that is assigned to the parameter token of the path operation function.
FastAPI will know that it can use this dependency to define a "security scheme" in the OpenAPI schema (and the automatic API docs).

It will go and look in the request for that `Authorization` header, check if the value is Bearer plus some token, and will return the token as a `str`.
If it doesn't see an Authorization header, or the value doesn't have a Bearer token, it will respond with a 401 status code error (`UNAUTHORIZED`) directly.

# Get current User
In the previous section, the security system (which is based on the dependency injection system) was giving the *path operation function* a `token` as a `str`.
>[`Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated) Add metadata `x` to a given type `T` by using the annotation `Annotated[T, x]`. Metadata added using `Annotated` can be used by static analysis tools or at runtime. At runtime, the metadata is stored in a `__metadata__` attribute.
If a library or tool encounters an annotation `Annotated[T, x]` and has no special logic for the metadata, it should ignore the metadata and simply treat the annotation as `T`.

But that is still not that useful. Let's make it give us the current user.

## Create a user model
First, let's create a Pydantic user model. in `schemas.py`

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
```

## Create a Service
Then we create services to use in our application. Let's call it `service.py`

Let's create a dependency `get_current_user`.

Remember that dependencies can have sub-dependencies?

`get_current_user` will have a dependency with the same `oauth2_scheme` we created before.

The same as we were doing before in the path operation directly, our new dependency `get_current_user` will receive a token as a str from the sub-dependency `oauth2_scheme`:

```python
from schemas import User
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    '''getuser via decode token'''
    return user

```

`get_current_user` will use a (fake) utility function we created, that takes a token as a `str` and returns our Pydantic `User` model:

```python

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    '''getuser via decode token'''
    user = fake_decode_token(token)
    return user

```

So now we can use the same Depends with our `get_current_user` in the *path* operation in `entry.py`:

```python
import sys
import os
from typing import Annotated
from fastapi import Depends, FastAPI
from service import get_current_user
from schemas import User

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

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
```
Notice that we declare the type of current_user as the Pydantic model `User`.
This will help us inside of the function with all the completion and type checks.

We just need to add a path operation for the user/client to actually send the username and password.

