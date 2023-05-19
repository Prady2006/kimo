from pydantic import BaseSettings
import os 
class Settings(BaseSettings): 
    mongo_host = os.getenv("MONGODB_HOST") or "localhost"
    mongo_port = int(os.getenv("MONGODB_PORT") or 27017)
    app_port = os.getenv("APP_PORT") or 8000
    mongodb_name = os.getenv("MONGODB_NAME") or "kimo"


app_settings = Settings()