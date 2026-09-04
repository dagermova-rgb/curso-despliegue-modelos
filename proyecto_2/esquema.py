
from pydantic import BaseModel, Field

from datetime import date

class RegistroHistorico(BaseModel):

    fecha: date = Field(..., description="Fecha del registro histórico")

    unidades: float = Field(ge=0, description="Número de unidades vendidas en la fecha especificada, no puede ser negativo")



class solicitudPronostico(BaseModel):
    store: int = Field(ge=1,le=10, description="El número de tiendas del 1 al 10")

    item: int = Field(ge=1,le=50, description="El numero de productos del 1 al 50")
    
    historial: list[RegistroHistorico] = Field(min_length=28,max_length=365,
                                                description="Historico reciente de la serie. Minimo 28 registros)")

    horizonte: int = Field(default=14, ge=1, le=28, description="Número de días a pronosticar, entre 1 y 28")