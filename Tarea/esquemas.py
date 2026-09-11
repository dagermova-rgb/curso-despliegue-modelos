from typing import Literal

from pydantic import BaseModel, Field


class Cliente(BaseModel):
    antiguedad_meses: int = Field(
        ge=1,
        le=60,
        description="Antigüedad del cliente en meses"
    )

    gasto_mensual: float = Field(
        ge=5.0,
        le=58.39,
        description="Gasto mensual del cliente"
    )

    visitas_ultimo_mes: int = Field(
        ge=0,
        le=29,
        description="Cantidad de visitas realizadas durante el último mes"
    )

    dias_desde_ultima_visita: int = Field(
        ge=0,
        le=90,
        description="Días transcurridos desde la última visita"
    )

    tickets_soporte: int = Field(
        ge=0,
        le=5,
        description="Cantidad de tickets de soporte"
    )

    plan: Literal["basico", "estandar", "premium"] = Field(
        description="Plan contratado por el cliente"
    )

    metodo_pago: Literal["efectivo", "tarjeta", "transferencia"] = Field(
        description="Método de pago utilizado por el cliente"
    )

    descuento_activo: int = Field(
        ge=0,
        le=1,
        description="Indica si el cliente tiene un descuento activo: 0 = No, 1 = Sí"
    )