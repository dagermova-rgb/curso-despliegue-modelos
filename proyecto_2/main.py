from contextlib import asynccontextmanager #sirve para crear un contexto asincrono para sabe si el bondle esta cargado o no
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException #sirve para crear la api y manejar errores
from pydantic import BaseModel, Field  #yield marca el punto en el que termina la lógica de inicio y FastAPI puede comenzar a atender solicitudes. Cuando la aplicación se vaya a cerrar, la ejecución continúa después del yield.

from proyecto_2.inferencia import pronosticar
from proyecto_2.esquema import solicitudPronostico

#Ruta del bundle que contiene el modelo entrenado
NOMBRE_BUNDLE = "proyecto_2\modelo_demanda.joblib"

estado_servicio = {"bundle": None}

#Cargar el bundle al iniciar la API
@asynccontextmanager
async def lifespan(app: FastAPI):

    estado_servicio["bundle"] = joblib.load(NOMBRE_BUNDLE)
    print("Bundle cargado correctamente")
    yield #yield sirve para indicar que el contexto ha terminado y se puede continuar con la ejecución del código
    estado_servicio["bundle"] = None

#Configuración de la API
app = FastAPI(
    title="API - Servicio de pronóstico de demanda", 
    description="Pronostico de demanda de productos por un forecast",  
    version="1.0.0",
    lifespan=lifespan
    )


@app.get("/")
def estado():
    """Estado del servicio"""
    return {
        "servicio":"API - Servicio de Predicción de demanda",
        "modelo_cargado": estado_servicio["bundle"] is not None
    }


@app.post("/predecir")
def predecir(datos: solicitudPronostico):

    store = datos.store
    item = datos.item
    horizonte = datos.horizonte
    registros = datos.historial

    historial = pd.DataFrame(
        {
            "date": pd.to_datetime([r.fecha for r in registros]),
            "store": store,
            "item": item,
            "sales": [r.unidades for r in registros]
        }
    )

    bundle = estado_servicio["bundle"]

    pronostico = pronosticar(bundle, historial, horizonte)

    return {
        "store": store, 
        "item": item,
        "pronostico": pronostico

    }
    