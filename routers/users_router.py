from fastapi import APIRouter,status,Depends
from fastapi.exceptions import HTTPException
from db import Session,engine
from schemas import SignUpModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
# from fastapi.encoders import jsonable_encoder
from auth import AuthHandler, find_user, session


auth_handler = AuthHandler()


user_router=APIRouter(
    prefix='/user',
    tags=['users']
)


@user_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user:SignUpModel):
    """
        ## Create a user
        This requires the following
        ```
                username:int
                email:str
                password:str
                is_staff:bool
                is_active:bool
        ```
    
    """
    db_email=session.query(User).filter(User.email==user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the email already exists")

    db_username=session.query(User).filter(User.username==user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the username already exists")

    hashed_pwd = auth_handler.get_password_hash(user.password)
    new_user=User(
        username=user.username,
        email=user.email,
        password=hashed_pwd,
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)
    session.commit()

    return new_user



#login route
@user_router.post('/login',status_code=200)
async def login(user:LoginModel):
    """     
        ## Login a user
        This requires
            ```
                username:str
                password:str
            ```
        and returns an  `access token` 
    """
    user_found = find_user(user.username)
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user_found.username)
    return {'token': token}


