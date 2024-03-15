import os
from dotenv import load_dotenv

load_dotenv()


BRANCH = os.environ.get("BRANCH", "dev")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "prod")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
NOTIFIER_API_TOKEN = os.environ.get("NOTIFIER_API_TOKEN")
API_TOKEN = os.environ.get("API_TOKEN")
FASTMAIL_TOKEN = os.environ.get("FASTMAIL_TOKEN")
FALLBACK_URI = os.environ.get("FALLBACK_URI")
MONGO_URI = os.environ.get("MONGO_URI")
