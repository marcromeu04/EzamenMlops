from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Entrada(BaseModel):
   
    id_paquete: str= Field(min_length=1)
    peso_kg: float=Field(gt=0, le=30)
    distancia_km: float=Field(ge=0, le=200 )
    
    @field_validator('id_paquete', mode='before')
    @classmethod
    def limpiar_espacios(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

class Salida(BaseModel):
    
    id_paquete: str= Field(min_length=1)
    categoria: Literal["normal", "urgente"]
    confianza: float=Field(ge=0, le=1)
    

