import os

class Config:
    # Secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cafe-management-secret-key-2024'
    
    # MySQL config
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '5782'
    MYSQL_DB = 'cafe_management'
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # Upload folder
    UPLOAD_FOLDER = 'static/images'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # Tax
    TAX_RATE = 0.05
    
    # Pagination
    ITEMS_PER_PAGE = 12