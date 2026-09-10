from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.auth import router as auth_router
from backend.routers.users import router as users_router
from backend.routers.devices import router as devices_router
from backend.routers.weather import router as weather_router
from backend.routers.irrigation import router as irrigation_router
from backend.routers.crops import router as crops_router
from backend.routers.areas import router as areas_router
from utils.init_db import init_db

init_db()
app=FastAPI(title='AgrIoT Backend API',version='1.0')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:8501','http://127.0.0.1:8501'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(auth_router,prefix='/api/auth',tags=['auth']); app.include_router(users_router,prefix='/api/users',tags=['users']); app.include_router(devices_router,prefix='/api/devices',tags=['devices']); app.include_router(weather_router,prefix='/api/weather',tags=['weather']); app.include_router(irrigation_router,prefix='/api/irrigation',tags=['irrigation']); app.include_router(crops_router,prefix='/api/crops',tags=['crops']); app.include_router(areas_router,prefix='/api/areas',tags=['areas'])
@app.get('/health')
def health(): return {'status':'ok'}
