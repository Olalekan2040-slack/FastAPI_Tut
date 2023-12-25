from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel
from typing import Optional
app = FastAPI()

class Item(BaseModel):
    name:str
    price :float
    brand :  Optional[str] = None

class Updated_item(BaseModel):
    name: Optional[str] = None
    price : Optional[float] = None
    brand :  Optional[str] = None

inventory = {}


@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(description = "The ID of the Item", gt=0 )):
    return inventory[item_id]
    


@app.get("/get-name")
def get_item( name: str):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
        
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/add-item/{item_id}")
def new_item(item_id : int, item : Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="ID already exist")
    inventory[item_id] = item
    return inventory[item_id]  



@app.put("/update/{item-id}")
def update_item(item_id: int, item : Updated_item):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item does not exisit")
    
    if item.name != None:
        inventory[item_id].name = item.name
    
    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand
    
    
    return inventory[item_id]


@app.delete("/delete")
def delete_item(item_id: int = Query(..., description = "Delete item")):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item does not exisit")
    
    del inventory[item_id]
    return {"Success": "Item successfully deleted"}