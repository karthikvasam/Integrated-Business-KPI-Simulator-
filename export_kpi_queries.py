# src/export_kpis.py
from src.kpi_queries import get_total_revenue, get_revenue_by_product_df, get_daily_sales_df
import pandas as pd
from datetime import datetime
from sqlalchemy import text
from db_connection import get_engine
import os

# Output directory
outdir = "exports"
os.makedirs(outdir, exist_ok=True)

def export_all():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # total revenue as small CSV
    total = get_total_revenue()
    pd.DataFrame([{"total_revenue": total}]).to_csv(f"{outdir}/total_revenue_{ts}.csv", index=False)

    # revenue by product
    get_revenue_by_product_df().to_csv(f"{outdir}/revenue_by_product_{ts}.csv", index=False)

    # daily sales
    get_daily_sales_df().to_csv(f"{outdir}/daily_sales_{ts}.csv", index=False)

    # ✅ NEW: export dim_date
    engine = get_engine()
    dim_query = text("""
        SELECT date_id, year, month, day, day_of_week, month_name, quarter
        FROM dim_date
        ORDER BY date_id
    """)
    with engine.connect() as conn:
        dim_df = pd.read_sql(dim_query, conn)
    dim_df.to_csv(f"{outdir}/dim_date_{ts}.csv", index=False)

    print("✅ Exported all CSVs (KPIs + DimDate) to", outdir)

if __name__ == "__main__":
    export_all()
