from fastapi import FastAPI
from fastapi.middleware.cors import  CORSMiddleware
from redis_om import get_redis_connection, HashModel
import redis

# app initialization
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"],
    allow_headers = ['*']
    )

# database connection
import redis
import ssl

# Create a Redis connection
try:
        # Initialize the Redis connection
        redis_conn = redis.from_url(
          "rediss://red-cpab15dds78s73cv10f0:UGgpYC3oQReuei4xWfXaFaKRBsQuvQjn@oregon-redis.render.com:6379"
        )

        # Test the connection
        redis_conn.ping()
        print("Connected successfully!")

        # Use the hset method to set a hash value
        redis_conn.hset('myhash', 'field1', 'value1')
        print("Hash set successfully!")

except redis.ConnectionError as e:
        print(f"Connection failed: {e}")
except AttributeError as e:
        print(f"AttributeError: {e}")
except Exception as e:
        print(f"An error occurred: {e}")

# model
class Product(HashModel):
    name : str
    price : float
    quantity : int
    
    class Meta:
        database = redis

# routes definition 
@app.get("/")
async def root():
    return {"message": "hello this is the product api"}

@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk:str):
    product = Product.get(pk=pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }

@app.post("/products")
def createProduct(product: Product):
    try:
        return product.save()
    except Exception as e:
        return {"error": f"an error occured: {e}"}
    
@app.put("/products/{pk}")
def UpdateProduct(pk:str, newProduct: Product): 
    try:
        products = Product.all_pks()
        if pk not in products:
            return{"message": "product not find"}
        product = Product.get(pk)
        product.name = newProduct.name
        product.price = newProduct.price
        product.quantity = newProduct.quantity
        
        return product.save()
    except Exception as e:
        return {"error": f"an error occured: {e}"}

@app.get("/products/{pk}")
async def getProduct(pk:str):
    try:
        products =  Product.all_pks()
        if pk not in products:
            return {"message": "product not found"}
        product = Product.get(pk=pk)
        return product
    except Exception as e:
        return{"error": "an error occured"}
    
    
    
@app.delete("/products/{pk}")
async def deleteProduct(pk:str):
    try:
        products = Product.all_pks()
        if pk not in products:
            return{"message": "product doesnt exist"}
        delete = Product.delete(pk=pk)   
        if delete == 1:
            return {"message": "product succesfully deleted"} 
        elif delete == 0:
            return {"message": "product does'nt exist"}  
    except Exception as e:
            return{"error": f"prouct with the Id not found: error: {e}"}
    
    
    
