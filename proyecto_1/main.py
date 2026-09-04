from contextlib import asynccontextmanager #sirve para crear un contexto asincrono para sabe si el bondle esta cargado o no
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException #sirve para crear la api y manejar errores
from pydantic import BaseModel, Field  #yield marca el punto en el que termina la lógica de inicio y FastAPI puede comenzar a atender solicitudes. Cuando la aplicación se vaya a cerrar, la ejecución continúa después del yield.
NOMBRE_BUNDLE = "modelo_entrenado_e_cardiaca.pkl"

estado_servicio = {"bundle": None}

@asynccontextmanager
async def lifespan(app: FastAPI):

    estado_servicio["bundle"] = joblib.load(NOMBRE_BUNDLE)
    print("Bundle cargado correctamente")
    yield #yield sirve para indicar que el contexto ha terminado y se puede continuar con la ejecución del código
    estado_servicio["bundle"] = None

app = FastAPI(
    title="API de predicción de enfermedad cardiaca", 
    description="Recibe datos clinicos de un paciente y predice riesgo cardipatia coronaria (chd).",  
    version="1.0.0",
    lifespan=lifespan
    )

#Clase para la entrada
#Las llaves deben coincidir con los nombres de las columnas del dataset original, y los tipos de datos deben ser los mismos que los del dataset original.
class PacienteInput(BaseModel):
    sbp: int = Field(..., description="Presión sistólica (mmHg)")
    Tabaco: float = Field(..., description="Consumo de tabaco (kg)"),
    ldl: float = Field(..., description="Colesterol LDL (mg/dL)"),
    Adiposidad: float = Field(..., description="Adiposidad (kg/m²)"),
    Familia: Literal["Presente", "Ausente"] = Field(..., description="Antecedentes familiares de enfermedad cardiaca (Presente/Ausente)"),
    Tipo: int = Field(..., description="Comportamiento tipo-A)"),
    Obesidad: float = Field(..., description="Obesidad (kg/m²)"),
    Alcohol: float = Field(..., description="Consumo de alcohol (g/día)"),
    Edad: int = Field(..., description="Edad del paciente")

#Clase para la salida
class PacienteOutput (BaseModel):
    chd_predicho: int
    probabilidad: float
    riesgo: str

#Construir el endpoint de verificación del estado del servicio. Este endpoint devuelve un diccionario con el estado del servicio y si el modelo está cargado o no.
@app.get("/")
def estado():
    return {
            "servicio":"API de prediccion de enfermedad cardiaca",
            "modelo_cargado": estado_servicio["bundle"] is not None
    }

#Construir el endpoint de predicción. Este endpoint recibe un diccionario con los datos del paciente y devuelve un diccionario con la predicción del modelo.
#Predecir 
@app.post("/predecir", response_model=PacienteOutput)
def predecir(paciente: PacienteInput):

    #validar modelo
    bundle = estado_servicio["bundle"]

    if bundle is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")

    #Convertir a diccionario y mapear la variable Familia
    fila= paciente.model_dump() #model_dump() convierte el objeto en un diccionario

    #Aplicar transformación de la variable Familia usando el mapeo del bundle
    fila["Familia"] = bundle["mapeo_familia"][fila["Familia"]] # 

    #convertir a dataframe y seleccionar las columnas correctas
    X_nuevo = pd.DataFrame([fila])[bundle["columnas"]] # x_nuevo = pd.DataFrame([fila])[bundle["columnas"]] # Crear un DataFrame con las columnas correctas

    #Predicción
    prediccion = bundle["pipeline"].predict(X_nuevo)[0] 
    probabilidad = bundle["pipeline"].predict_proba(X_nuevo)[0,1]

    #Devolver resultado
    return PacienteOutput(
        chd_predicho=int(prediccion),
        probabilidad= round(probabilidad, 4),
        riesgo="Alto" if prediccion == 1 else "Bajo"
    )