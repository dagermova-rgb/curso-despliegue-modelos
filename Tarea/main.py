from contextlib import asynccontextmanager

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from esquemas import Cliente


NOMBRE_BUNDLE = "modelo_churn.joblib"

estado_servicio = {"bundle": None}


@asynccontextmanager
async def lifespan(app: FastAPI):
    estado_servicio["bundle"] = joblib.load(NOMBRE_BUNDLE)
    print("Bundle cargado correctamente")
    yield
    estado_servicio["bundle"] = None


app = FastAPI(
    title="API de predicción de cancelación de clientes",
    description="Recibe los datos de un cliente y predice su probabilidad de cancelación.",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
def estado():
    return {
        "servicio": "API de predicción de cancelación de clientes",
        "modelo_cargado": estado_servicio["bundle"] is not None
    }


@app.post("/predecir")
def predecir(cliente: Cliente):
    bundle = estado_servicio["bundle"]

    if bundle is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo no cargado"
        )

    fila = cliente.model_dump()

    X_nuevo = pd.DataFrame([fila])[bundle["columnas"]]

    probabilidad = bundle["modelo"].predict_proba(X_nuevo)[0, 1]

    umbral = bundle["umbral"]

    prediccion = "cancela" if probabilidad >= umbral else "sigue"

    if probabilidad >= 0.7:
        riesgo = "alto"
    elif probabilidad >= umbral:
        riesgo = "medio"
    else:
        riesgo = "bajo"

    return {
        "probabilidad_cancelacion": round(float(probabilidad), 4),
        "prediccion": prediccion,
        "nivel_riesgo": riesgo,
        "umbral_usado": umbral
    }