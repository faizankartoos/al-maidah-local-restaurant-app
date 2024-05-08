from fastapi import APIRouter, Request, FastAPI
import uvicorn
from datetime import datetime, date
from database.connection import get_session, engine
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import Menu, OrderHistory
from database.models import Base
from database.myEnums import OrderHistoryStatus
from typing import Any
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi import (
    FastAPI, 
    Request, 
    Depends)

app = FastAPI()



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)



@app.get("/get-menu/")
def get_menu(session: Annotated[Any, Depends(get_session)]):    
    menu = session.query(Menu).all()
    return menu



@app.post("/add-menu/")
def add_menu(session: Annotated[Any, Depends(get_session)], data:dict):    
    new_menu = Menu()
    new_menu.name = data['name']
    new_menu.description = data['description']
    new_menu.price = data['price']
    session.add(new_menu)
    session.commit()
    return True


@app.get("/get-order-history/")
def get_order_history(session: Annotated[Any, Depends(get_session)]):    
    orders = []
    order_history = session.query(OrderHistory).all()
    for order in order_history:
        dt = datetime.utcnow() - order.updated_at
        if dt.total_seconds() > 40 and (order.status == OrderHistoryStatus.COMPLETED  or order.status == OrderHistoryStatus.CANCELLED):
            continue
        orders.append(order)
    return orders

@app.get("/get-all-orders/")
def get_all_orders(session: Annotated[Any, Depends(get_session)]):    
    order_history = session.query(OrderHistory).all()
    return order_history

@app.get("/filter-orders/")
def filter_orders(session: Annotated[Any, Depends(get_session)], filter_date: str):  
    orders = []  
    order_history = session.query(OrderHistory).all()
    if not filter_date:
        return order_history
    for order in order_history:
        if order.created_at.strftime('%Y-%m-%d') == filter_date:
            orders.append(order)
    return orders



@app.post("/update-order/")
def update_order(session: Annotated[Any, Depends(get_session)], data:dict):    
    order_history = session.query(OrderHistory).filter(OrderHistory.id == data['order_id']).one()
    if order_history.status == OrderHistoryStatus.CANCELLED:
        return False
    elif order_history.status == OrderHistoryStatus.COMPLETED:
        return False
    order_history.status = data['status']
    order_history.updated_at = datetime.utcnow()
    session.commit()
    return True

@app.post("/add-order/")
def add_order(session: Annotated[Any, Depends(get_session)], data:dict):    
    new_order = OrderHistory()
    new_order.order = json.dumps(data['data'])
    new_order.type = data['order_type']
    session.add(new_order)
    session.commit()
    
    return True




if __name__=="__main__":
    uvicorn.run(app=app, host='127.0.0.1', port=8004)