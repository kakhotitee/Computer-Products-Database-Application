import psycopg2
import argparse
import os

# Подключение к базе
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME", "postgres"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "20060503"),
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432")
)
conn.autocommit = True

def list_products():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM products ORDER BY product_id")
        rows = cur.fetchall()
        for row in rows:
            print(row)

def create_product(brand, model, full_name, price, rating, stock_quantity, warranty_months, category_id):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO products (brand, model, full_name, price, rating, stock_quantity, warranty_months, category_id) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING product_id",
            (brand, model, full_name, price, rating, stock_quantity, warranty_months, category_id)
        )
        product_id = cur.fetchone()[0]
        print(f"Product created with ID: {product_id}")

def read_product(product_id=None):
    with conn.cursor() as cur:
        if product_id:
            cur.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
        else:
            cur.execute("SELECT * FROM products ORDER BY product_id")
        rows = cur.fetchall()
        for row in rows:
            print(row)

def update_product(product_id, field, value):
    with conn.cursor() as cur:
        cur.execute(f"UPDATE products SET {field}=%s WHERE product_id=%s", (value, product_id))
        print(f"Updated product {product_id}")

def delete_product(product_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
        print(f"Deleted product {product_id}")

def complex_select():
    with conn.cursor() as cur:
        # Пример: все продукты категории 1 с ценой > 50000 или рейтинг >= 4.8
        cur.execute(
            "SELECT * FROM products WHERE (category_id=1 AND price>50000) OR rating>=4.8 ORDER BY product_id"
        )
        rows = cur.fetchall()
        for row in rows:
            print(row)

def test_injection(input_value):
    with conn.cursor() as cur:
        # безопасный пример
        cur.execute("SELECT * FROM products WHERE full_name=%s", (input_value,))
        rows = cur.fetchall()
        for row in rows:
            print(row)

# CLI
parser = argparse.ArgumentParser()
parser.add_argument("cmd", choices=["list","create","read","update","delete","complex","test-injection"])
parser.add_argument("--id", type=int)
parser.add_argument("--brand")
parser.add_argument("--model")
parser.add_argument("--full_name")
parser.add_argument("--price", type=float)
parser.add_argument("--rating", type=float)
parser.add_argument("--stock_quantity", type=int)
parser.add_argument("--warranty_months", type=int)
parser.add_argument("--category_id", type=int)
parser.add_argument("--field")
parser.add_argument("--value")
parser.add_argument("--input_value")
args = parser.parse_args()

if args.cmd == "list":
    list_products()
elif args.cmd == "create":
    create_product(args.brand, args.model, args.full_name, args.price, args.rating, args.stock_quantity, args.warranty_months, args.category_id)
elif args.cmd == "read":
    read_product(args.id)
elif args.cmd == "update":
    update_product(args.id, args.field, args.value)
elif args.cmd == "delete":
    delete_product(args.id)
elif args.cmd == "complex":
    complex_select()
elif args.cmd == "test-injection":
    test_injection(args.input_value)
