from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
  text: str
  id: int