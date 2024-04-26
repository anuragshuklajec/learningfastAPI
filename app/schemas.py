from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True #default value partially optional

class PostCreate(PostBase):
    pass

class Post(PostBase): # model for response notice it inherits from PostBase class hence it would have every field in that class in addition to mentioned explicitely
    id : int
    created_at : datetime
    
    class Config: # So that it reads the model object and converts it to dictionary otherwise it will lead to error
        from_attributes = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str
    
class UserResponse(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    
    class Config:
        from_attributes = True #orm_mode has been renamed to from_attribute