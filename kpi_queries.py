from src.db_connection import get_engine
from sqlalchemy import text
import pandas as pd
from src.db_connection import get_engine
from sqlalchemy import text
import pandas as pd


def get_revenue_by_product():
    engine = get_engine()
    q = """
    SELECT p.name AS product, SUM(s.qty * s.price_per_unit) AS revenue
    FROM sales s
    JOIN products p ON p.id = s.product_id
    GROUP BY p.id, p.name
    ORDER BY revenue DESC
    """
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(text(q), conn)
    return df




def get_total_revenue():
    engine = get_engine()
    with engine.connect() as conn:
        return float(conn.execute(text("SELECT total_revenue FROM v_total_revenue")).scalar() or 0.0)

def get_revenue_by_product_df():
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text("SELECT product, category, revenue, units_sold FROM v_revenue_by_product"), conn)

def get_revenue_by_store_df():
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text("SELECT store, city, revenue, units_sold FROM v_revenue_by_store"), conn)

def get_daily_sales_df(limit=None):
    engine = get_engine()
    q = "SELECT sale_date, units_sold, revenue FROM v_daily_sales ORDER BY sale_date"
    if limit:
        q += f" LIMIT {int(limit)}"
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(q), conn)


if __name__ == "__main__":
    print("Total revenue:", get_revenue_by_store_df)
    print("\nRevenue by store:")
    df = get_revenue_by_store_df()
    try:
        print(df.to_string(index=False))
    except Exception:
        print(df)