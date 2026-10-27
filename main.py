from fastapi import Depends, FastAPI,HTTPException, Request
from fastapi.responses import JSONResponse
from auth_dependencies import get_current_user, require_role, require_role
from auth_dependencies import get_current_user
from dependencies import get_employee_service
from enums.user_role import UserRole
from models.user import User
from services import employee_service
from schemas.employee import employeeCreate as e, employeeResponse
from logging_config import logger
from exception_handler import register_exception_handlers
app = FastAPI()
register_exception_handlers(app)
from api.auth import router as auth_router
from api.employee import router as employee_router
from api.department import router as department_router

app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(department_router)
