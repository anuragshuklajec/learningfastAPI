from fastapi  import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database,schemas,models,utils,oauth2

router = APIRouter(
    tags = ["Authentication"]
)


@router.post('/login')
# def login(user_credentials : schemas.UserLogin ,db:Session = Depends(database.get_db)): # This expectes something in body and we are using inbuilt password request form which takes input from form data
def login(user_credentials : OAuth2PasswordRequestForm = Depends() ,db:Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if user:
        if not utils.verify(user_credentials.password,user.password):
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "user is not valid, please check credentials")
        access_token = oauth2.create_access_token(data = {"user_id" : user.id})
        
        return {"access_token" : access_token, "token_type" : "bearer"}
            
        
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "user is not valid, please check credentials")