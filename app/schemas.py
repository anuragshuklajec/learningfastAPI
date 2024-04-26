from pydantic import BaseModel

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True #default value partially optional

class PostCreate(PostBase):
    pass

    
    
    
