import os


class Config:
    # Database
    DATABASE_URL = "husma_foundation.db"

    # Security
    SECRET_KEY = "husma-foundation-secret-key-2024"
    PASSWORD_RESET_TIMEOUT = 3600

    # App Settings
    UPLOAD_FOLDER = "instance/uploads"
    RECEIPT_FOLDER = "temp/receipts"
    MAX_FILE_SIZE = 5 * 1024 * 1024

    # Inventory
    LOW_STOCK_THRESHOLD = 20
    CRITICAL_STOCK_THRESHOLD = 10


config = Config()