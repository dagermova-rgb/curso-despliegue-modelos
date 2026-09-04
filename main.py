from fastapi import FastAPI

app = FastAPI(title="My FastAPI Application")

@app.get("/")
def root():
    return {"message": "Welcome to My FastAPI Application!"}

#Parametros

@app.get("/saludo/{nombre}")
def saludo(nombre: str):
    return {"message": f"Hola, {nombre}, bienvenido a mi aplicación FastAPI!"}

