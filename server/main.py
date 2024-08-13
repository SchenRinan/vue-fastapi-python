from fastapi import FastAPI, Form
from list import Item

app = FastAPI()

items = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

#CRUD - Create
@app.post("/items/create")
async def createItem(text: str = Form(...)):
    new_id = len(items) + 1
    new_item = Item(id=new_id, text=text)
    items.append(new_item)
    return {"message":"Item created", "item":new_item}

#CRUD - Read
@app.get("/items/findbyid/{item_id}")
async def findbyId(item_id:int):
    if 0 < item_id <= len(items):
        return items[item_id - 1]
    else:
        return {"error": "Item not found"}

@app.get("/items/findall")
async def findAll():
    return items


#CRUD - Update
@app.put("/items/editbyid/{item_id}")
async def editbyId(item_id:int, text:str = Form(...)):
    if 0 < item_id <= len(items):
        items[item_id-1] = Item(id=item_id, text=text)
        return {"message":"Item updated!", "item":items[item_id-1]}
    else:
        return {"error": "Item not found"}

#CRUD - Delete
@app.delete("/items/deletebyid/{item_id}")
async def deletebyId(item_id:int):
    if 0 < item_id <= len(items):
        items.pop(item_id - 1)
        for index, item in enumerate(items, start=1):
            item.id = index
        
        return {"message": "Item deleted successfully"}
    else:
        return {"error": "Item not found"}