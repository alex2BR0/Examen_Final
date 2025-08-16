from pydantic import BaseModel, Field, validator
from typing import List
import re 


class Objeto(BaseModel):
    """Modelo para representar un objeto de inversión"""
    nombre: str = Field(..., description="Nombre del proyecto o inversión")
    peso: int = Field(..., gt=0, description="Costo o peso del proyecto")
    ganancia: int = Field(..., ge=0, description="Ganancia esperada del proyecto")

    @validator('nombre')
    def validar_nombre(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        if len(v) > 50:
            raise ValueError('El nombre no puede exceder 50 caracteres')
        return v.strip()

    @validator('peso')
    def validar_peso(cls, v):
        if v <= 0:
            raise ValueError('El peso debe ser mayor que 0')
        if v > 1000000:
            raise ValueError('El peso no puede exceder 1,000,000')
        return v

    @validator('ganancia')
    def validar_ganancia(cls, v):
        if v < 0:
            raise ValueError('La ganancia no puede ser negativa')
        if v > 1000000:
            raise ValueError('La ganancia no puede exceder 1,000,000')
        return v


class OptimizacionRequest(BaseModel):
    """Modelo para la solicitud de optimización"""
    capacidad: int = Field(..., gt=0, description="Capacidad total del presupuesto")
    objetos: List[Objeto] = Field(..., min_items=1, description="Lista de objetos disponibles")

    @validator('capacidad')
    def validar_capacidad(cls, v):
        if v <= 0:
            raise ValueError('La capacidad debe ser mayor que 0')
        if v > 10000000:
            raise ValueError('La capacidad no puede exceder 10,000,000')
        return v

    @validator('objetos')
    def validar_objetos(cls, v):
        if not v:
            raise ValueError('Debe proporcionar al menos un objeto')
        
        # Verificar nombres únicos
        nombres = [obj.nombre for obj in v]
        if len(nombres) != len(set(nombres)):
            raise ValueError('Los nombres de los objetos deben ser únicos')
        
        return v


class OptimizacionResponse(BaseModel):
    """Modelo para la respuesta de optimización"""
    seleccionados: List[str] = Field(..., description="Nombres de los objetos seleccionados")
    ganancia_total: int = Field(..., ge=0, description="Ganancia total de los objetos seleccionados")
    peso_total: int = Field(..., ge=0, description="Peso total de los objetos seleccionados")
    capacidad_utilizada: float = Field(..., description="Porcentaje de capacidad utilizada")
    eficiencia: float = Field(..., description="Ratio ganancia/peso de la selección")


class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    error: str = Field(..., description="Descripción del error")
    detalles: str = Field(..., description="Detalles adicionales del error")
