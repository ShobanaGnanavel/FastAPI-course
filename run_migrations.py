from alembic.config import Config
from alembic import command
import os

# Load environment variables (if using .env locally)
# from dotenv import load_dotenv
# load_dotenv()

alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")
print("Migration completed successfully!")
