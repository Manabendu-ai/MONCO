from app.database.database import engine, Base

# Import models so SQLAlchemy knows about them
from app.database import models

Base.metadata.create_all(bind=engine)

print("✅ Tables Created Successfully!")