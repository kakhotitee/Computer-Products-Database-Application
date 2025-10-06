import argparse
from database import get_connection

def list_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT product_id, brand, model, full_name, price, rating, stock_quantity, warranty_months, category_id
        FROM products ORDER BY product_id
        """
    )
    rows = cur.fetchall()
    for r in rows:
        print(f"#{r[0]} | {r[1]} {r[2]} | {r[3]} | {r[4]} ₸ | ⭐ {r[5]} | stock={r[6]} | {r[7]}m | cat={r[8]}")
    cur.close()
    conn.close()

def add_product(args):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO products (brand, model, full_name, price, rating, stock_quantity, warranty_months, category_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (args.brand, args.model, args.full_name, args.price, args.rating, args.stock_quantity, args.warranty_months, args.category_id)
    )
    conn.commit()
    print("Товар добавлен:", args.full_name)
    cur.close()
    conn.close()

def delete_product(args):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE product_id = %s", (args.product_id,))
    deleted = cur.rowcount
    conn.commit()
    print(f"Удалено записей: {deleted}")
    cur.close()
    conn.close()

def show_stats():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            COUNT(*) AS total_count,
            COALESCE(SUM(price), 0) AS total_price,
            COALESCE(MAX(rating), 0) AS max_rating,
            COALESCE(AVG(price), 0) AS avg_price,
            COALESCE(SUM(stock_quantity), 0) AS total_stock,
            COALESCE(MIN(price), 0) AS min_price,
            COALESCE(MAX(price), 0) AS max_price
        FROM products
        """
    )
    r = cur.fetchone()
    cur.close()
    conn.close()
    print("Всего товаров:", r[0])
    print("Общая стоимость:", float(r[1]))
    print("Макс. рейтинг:", float(r[2]))
    print("Средняя цена:", float(r[3]))
    print("Всего на складе:", int(r[4]))
    print("Мин. цена:", float(r[5]))
    print("Макс. цена:", float(r[6]))

def main():
    parser = argparse.ArgumentParser(description="CLI для управления товарами")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sp_list = sub.add_parser("list", help="Показать список товаров")
    sp_list.set_defaults(func=lambda a: list_products())

    sp_add = sub.add_parser("add", help="Добавить товар")
    sp_add.add_argument("--brand", required=True)
    sp_add.add_argument("--model", required=True)
    sp_add.add_argument("--full_name", required=True)
    sp_add.add_argument("--price", type=float, required=True)
    sp_add.add_argument("--rating", type=float, required=True)
    sp_add.add_argument("--stock_quantity", type=int, required=True)
    sp_add.add_argument("--warranty_months", type=int, required=True)
    sp_add.add_argument("--category_id", type=int, required=True)
    sp_add.set_defaults(func=add_product)

    sp_del = sub.add_parser("delete", help="Удалить товар по ID")
    sp_del.add_argument("--product_id", type=int, required=True)
    sp_del.set_defaults(func=delete_product)

    sp_stats = sub.add_parser("stats", help="Показать агрегированную статистику")
    sp_stats.set_defaults(func=lambda a: show_stats())

    args = parser.parse_args()
    args.func(args) if hasattr(args, "func") else parser.print_help()

if __name__ == "__main__":
    main()
