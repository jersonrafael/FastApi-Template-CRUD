from pydantic import BaseModel


class postBase(BaseModel):
    title:str
    descript:str | None


class createPost(postBase):
    pass

class getPost(postBase):
    id: int
    class Config:
        orm_mode = True