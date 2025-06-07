
from backend.db import engine, Base
from backend import models

Base.metadata.create_all(bind=engine)

