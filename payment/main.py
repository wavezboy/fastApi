from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"],
    allow_headers = ['*']
    )

# database connection
redis = get_redis_connection(
    host= "red-cpab15dds78s73cv10f0@oregon-redis.render.com",
    port = 6379,
    password = "UGgpYC3oQReuei4xWfXaFaKRBsQuvQjn",
    decode_responses =  True   
) 



class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  
    
    class Meta:
        database = redis
        



@app.post("/orders")
async def createOrder(request:Request):
    body = await request.json()
    response = requests.get(f"http://127.0.0.1:8000/products/{body["id"]}")
    
    if response.status_code == 200:
        product = response.json()
        order = Order(
        product_id = body["id"],
        price = product["price"],
        fee = 0.2 * product["price"],
        total = 1.2* product["price"],
        quantity = body["quantity"],
        status = "pending"
    )
        order.save()
        order_completed(order)
        return order
    else:
        return {"error": f"Error: {response.status_code} - {response.reason}" }
    
    
def order_completed(order: Order):
    order.status = "completed"
    order.save()