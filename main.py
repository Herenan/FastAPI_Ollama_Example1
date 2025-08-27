from logging import root
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import tkinter as tk
from tkinter import BOTH, Frame, ttk, messagebox

app = FastAPI()

class Item(BaseModel):
    id : int
    name : str
    description : str
    price : float
    
class CreateItem(BaseModel):
    name : str
    description : str
    price : float

db = [
    Item(id=1, name="MacBook", description="Air M1", price=50000.0),
    Item(id=2, name="MacBook", description="Pro M4", price=70000.0),
    Item(id=3, name="MacBook", description="Air M3", price=60000.0),
    Item(id=4, name="MacBook", description="Pro M1", price=65000.0),
    Item(id=5, name="MacBook", description="Pro M1", price=65000.0)
]
def read_item_data():
    for item in db:
        print(item)

@app.get("/items",response_model=List[Item])
def read_item():
    return db

@app.get("/item/{item_id}",response_model=Item)
def read_item_by_id(item_id : int):
    for item in db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/item",response_model=Item)
def create_item(item_data : CreateItem):
    new_id = max([item.id for item in db]) + 1 if db else 1
    new_item = Item(id=new_id, **item_data.dict())
    db.append(new_item)
    return new_item

@app.put("/item/{item_id}",response_model=Item)
def update_item(item_id : int, item_data : CreateItem):
    for index, item in enumerate(db):
        if item.id == item_id:
            update_items = Item(id=item_id, **item_data.dict())
            db[index] = update_items
            return update_items
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/item/{item_id}", status_code=200)
def delete_item(item_id : int):
    for item in db:
        if item.id == item_id:
            break
    if item:
        db.remove(item)
        return db
    raise HTTPException(status_code=404, detail="Item not found")

root = tk.Tk()

root.title("FastAPI + Ollama")
root.geometry("700x500")
        
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=BOTH, expand=True)
read_button = ttk.Button(main_frame, text="ดึงข้อมูล", command=read_item_data)
read_button.pack(pady=10)
text_display = ttk.Entry(main_frame, width=30, textvariable=db)
text_display.pack(pady=10)

root.mainloop()