from sys import prefix

from fastapi import FastAPI, Depends, status, Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles



from app import exceptions
from app.auth.routes import router as auth_router

from app.routes import  pages_router, api_router
from app.fastapi_instance import app


app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # любой домен
    allow_credentials=False,  # без cookies
    allow_methods=["*"],      # все методы (GET, POST и т.д.)
    allow_headers=["*"],      # все заголовки
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(api_router, prefix= "/api")
app.include_router(pages_router)



# custom exception handlers
@app.exception_handler(exceptions.NotFoundError)
async def not_found_handler(request, exc: exceptions.NotFoundError):
    return JSONResponse({"detail": str(exc)}, status_code=status.HTTP_404_NOT_FOUND)

@app.exception_handler(exceptions.AlreadyExistsError)
async def conflict_handler(request, exc: exceptions.AlreadyExistsError):
    return JSONResponse({"detail": str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)

@app.exception_handler(exceptions.BusinessError)
async def business_handler(request, exc: exceptions.BusinessError):
    return JSONResponse({"detail": str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)


