from sqlalchemy import create_engine,text
import os



try:
    engine = create_engine("DATABASE_URL")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW();"))
        print("✅ Connected! Current time:", result.fetchone())
except Exception as e:
    print("❌ Connection failed:", e)
