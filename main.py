from fastapi import FastAPI, HTTPException
from routers.products import router as products_router
from routers.llm import router as llm_router


app = FastAPI() # Servidor de la app

app.include_router(products_router)
app.include_router(llm_router)


@app.get("/")
def home():
    return {'message': 'hello world'}


