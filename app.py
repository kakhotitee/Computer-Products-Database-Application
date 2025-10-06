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
    # Aggregates
    cursor.execute("""
        SELECT
            COUNT(*) AS total_count,
            COALESCE(SUM(price), 0) AS total_price,
            COALESCE(MAX(rating), 0) AS max_rating,
            COALESCE(AVG(price), 0) AS avg_price,
            COALESCE(SUM(stock_quantity), 0) AS total_stock,
            COALESCE(MIN(price), 0) AS min_price,
            COALESCE(MAX(price), 0) AS max_price
        FROM products
    """)
    row = cursor.fetchone()
    stats = {
        "total_count": row[0],
        "total_price": float(row[1]) if row[1] is not None else 0.0,
        "max_rating": float(row[2]) if row[2] is not None else 0.0,
        "avg_price": float(row[3]) if row[3] is not None else 0.0,
        "total_stock": int(row[4]) if row[4] is not None else 0,
        "min_price": float(row[5]) if row[5] is not None else 0.0,
        "max_price": float(row[6]) if row[6] is not None else 0.0,
    }
    cursor.close()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "products": products, "stats": stats})


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


@app.post("/delete")
def delete_product(product_id: int = Form(...)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM products WHERE product_id = %s
    """, (product_id,))
    deleted = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"Удалено записей: {deleted}"}
