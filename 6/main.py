from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

# Создаем подключение к базе данных SQLite
conn = sqlite3.connect('store.db')
cursor = conn.cursor()

# Создаем таблицы
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT,
                    password TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    price REAL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    product_id INTEGER,
                    order_date TEXT,
                    status TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (product_id) REFERENCES products (id))''')

# Классы Pydantic моделей
class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class Product(BaseModel):
    name: str
    description: str
    price: float

class Order(BaseModel):
    user_id: int
    product_id: int
    order_date: str
    status: str

app = FastAPI()

# CRUD операции для таблицы пользователей
@app.post("/users/")
async def create_user(user: User):
    cursor.execute('''INSERT INTO users (first_name, last_name, email, password) 
                      VALUES (?, ?, ?, ?)''', (user.first_name, user.last_name, user.email, user.password))
    conn.commit()
    return {"message": "User created successfully"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    if user:
        return {"id": user[0], "first_name": user[1], "last_name": user[2], "email": user[3]}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/products/")
async def create_product(product: Product):
    cursor.execute('''INSERT INTO products (name, description, price) 
                      VALUES (?, ?, ?)''', (product.name, product.description, product.price))
    conn.commit()
    return {"message": "Product created successfully"}

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()
    if product:
        return {"id": product[0], "name": product[1], "description": product[2], "price": product[3]}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.post("/orders/")
async def create_order(order: Order):
    cursor.execute('''INSERT INTO orders (user_id, product_id, order_date, status) 
                      VALUES (?, ?, ?, ?)''', (order.user_id, order.product_id, order.order_date, order.status))
    conn.commit()
    return {"message": "Order created successfully"}

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    order = cursor.fetchone()
    if order:
        return {"id": order[0], "user_id": order[1], "product_id": order[2], "order_date": order[3], "status": order[4]}
    else:
        raise HTTPException(status_code=404, detail="Order not found")

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    cursor.execute('''UPDATE products SET name=?, description=?, price=? WHERE id=?''',
                   (product.name, product.description, product.price, product_id))
    conn.commit()
    return {"message": "Product updated successfully"}

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    return {"message": "Product deleted successfully"}

@app.put("/orders/{order_id}")
async def update_order(order_id: int, order: Order):
    cursor.execute('''UPDATE orders SET user_id=?, product_id=?, order_date=?, status=? WHERE id=?''',
                   (order.user_id, order.product_id, order.order_date, order.status, order_id))
    conn.commit()
    return {"message": "Order updated successfully"}

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
    conn.commit()
    return {"message": "Order deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
