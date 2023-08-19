import os

DATABASEURI_LOCAL = 'postgresql:///test_canna_kings'
DATABASEURI_ZENTRY = 'postgresql://svlgbagv:anTsf3qgxTij9GUqD81SptEmGeKg79uw@mahmud.db.elephantsql.com/svlgbagv'
#DATABASEURI_LOCAL = 'postgresql://svlgbagv:anTsf3qgxTij9GUqD81SptEmGeKg79uw@mahmud.db.elephantsql.com/svlgbagv'
SECRET_KEY_ZENTRY = "dc2bbf134adb448a72dcf54f5d5839e9"

#DEPRECIATED DATABASE: #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ehowumwg:1PrOXf9x36L-MgaeMjqoNVw5-Dw2bP_J@mahmud.db.elephantsql.com/ehowumwg'
if 'ZENTRY_APP_BASE_URL' in os.environ:
    BASE_URL = os.environ['ZENTRY_APP_BASE_URL']
else:
    BASE_URL = "http://localhost:8000"

#BASE_URL = "http://localhost:8000"