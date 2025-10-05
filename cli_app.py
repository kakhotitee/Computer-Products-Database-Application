from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import get_connection

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    conn = get_connection()
    cursor = conn.cursor()
    # Твой запрос с product_id
    cursor.execute("""
        SELECT product_id, brand, model, full_name, price, rating, stock_quantity, warranty_months, category_id
        FROM products ORDER BY product_id
    """)
    products = [
        {
            "product_id": row[0],
            "brand": row[1],
            "model": row[2],
            "full_name": row[3],
            "price": row[4],
            "rating": row[5],
            "stock_quantity": row[6],
            "warranty_months": row[7],
            "category_id": row[8]
        }
        for row in cursor.fetchall()
    ]
    cursor.close()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "products": products})


@app.post("/add")
def add_product(
    brand: str = Form(...),
    model: str = Form(...),
    full_name: str = Form(...),
    price: float = Form(...),
    rating: float = Form(...),
    stock_quantity: int = Form(...),
    warranty_months: int = Form(...),
    category_id: int = Form(...)
):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO products (brand, model, full_name, price, rating, stock_quantity, warranty_months, category_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (brand, model, full_name, price, rating, stock_quantity, warranty_months, category_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Товар добавлен успешно!"}
