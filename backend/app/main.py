from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import time
import logging 
from typing import Dict, Any

from .models import OptimizacionRequest, OptimizacionResponse, ErrorResponse
from .optimizer import OptimizadorPortafolio

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear instancia de FastAPI
app = FastAPI(
    title="Microservicio de Optimización de Portafolio de Inversiones",
    description="API para optimizar la selección de inversiones usando programación dinámica",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia global del optimizador
optimizador = OptimizadorPortafolio()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Maneja errores de validación de Pydantic"""
    logger.error(f"Error de validación: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Error de validación de datos",
            "detalles": str(exc.errors()),
            "tipo": "VALIDATION_ERROR"
        }
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """Maneja errores de validación de Pydantic en modelos"""
    logger.error(f"Error de validación Pydantic: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Error de validación de modelo",
            "detalles": str(exc.errors()),
            "tipo": "MODEL_VALIDATION_ERROR"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Maneja errores generales no capturados"""
    logger.error(f"Error no manejado: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "detalles": "Ha ocurrido un error inesperado",
            "tipo": "INTERNAL_ERROR"
        }
    )


@app.get("/")
async def root():
    """Endpoint raíz con información del servicio"""
    return {
        "mensaje": "Microservicio de Optimización de Portafolio de Inversiones",
        "version": "1.0.0",
        "endpoints": {
            "optimizar": "/optimizar",
            "documentacion": "/docs",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud del servicio"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "portfolio-optimizer"
    }


@app.post("/optimizar", response_model=OptimizacionResponse)
async def optimizar_portafolio(request: OptimizacionRequest):
    """
    Optimiza la selección de inversiones para maximizar la ganancia
    sin exceder la capacidad presupuestaria.
    
    Utiliza programación dinámica para resolver el problema de la mochila.
    
    Args:
        request: Datos de entrada con capacidad y lista de objetos
        
    Returns:
        OptimizacionResponse: Resultado de la optimización
        
    Raises:
        HTTPException: Si hay errores en el procesamiento
    """
    try:
        logger.info(f"Iniciando optimización para capacidad: {request.capacidad}, "
                   f"objetos: {len(request.objetos)}")
        
        # Validaciones adicionales
        if request.capacidad <= 0:
            raise HTTPException(
                status_code=400,
                detail="La capacidad debe ser mayor que 0"
            )
        
        if not request.objetos:
            raise HTTPException(
                status_code=400,
                detail="Debe proporcionar al menos un objeto"
            )
        
        # Verificar que no haya nombres duplicados
        nombres = [obj.nombre for obj in request.objetos]
        if len(nombres) != len(set(nombres)):
            raise HTTPException(
                status_code=400,
                detail="Los nombres de los objetos deben ser únicos"
            )
        
        # Ejecutar optimización
        start_time = time.time()
        resultado = optimizador.optimizar(request.capacidad, request.objetos)
        execution_time = time.time() - start_time
        
        logger.info(f"Optimización completada en {execution_time:.4f}s. "
                   f"Ganancia: {resultado.ganancia_total}, "
                   f"Peso: {resultado.peso_total}")
        
        return resultado
        
    except HTTPException:
        # Re-lanzar HTTPExceptions
        raise
    except Exception as e:
        logger.error(f"Error durante la optimización: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno durante la optimización: {str(e)}"
        )


@app.post("/optimizar/detallado")
async def optimizar_portafolio_detallado(request: OptimizacionRequest):
    """
    Optimiza la selección de inversiones y proporciona un análisis detallado
    incluyendo estadísticas y eficiencias de cada objeto.
    
    Args:
        request: Datos de entrada con capacidad y lista de objetos
        
    Returns:
        Dict: Análisis detallado de la optimización
    """
    try:
        logger.info(f"Iniciando optimización detallada para capacidad: {request.capacidad}")
        
        # Ejecutar optimización con análisis detallado
        start_time = time.time()
        analisis = optimizador.obtener_analisis_detallado(request.capacidad, request.objetos)
        execution_time = time.time() - start_time
        
        # Agregar información de rendimiento
        analisis['rendimiento'] = {
            'tiempo_ejecucion_ms': round(execution_time * 1000, 2),
            'timestamp": time.time()
        }
        
        logger.info(f"Análisis detallado completado en {execution_time:.4f}s")
        
        return analisis
        
    except Exception as e:
        logger.error(f"Error durante el análisis detallado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno durante el análisis: {str(e)}"
        )


@app.get("/ejemplos")
async def obtener_ejemplos():
    """Proporciona ejemplos de uso de la API"""
    return {
        "ejemplos": {
            "caso_1": {
                "descripcion": "Máximo aprovechamiento de capacidad",
                "entrada": {
                    "capacidad": 10000,
                    "objetos": [
                        {"nombre": "Fondo_A", "peso": 2000, "ganancia": 1500},
                        {"nombre": "Fondo_B", "peso": 4000, "ganancia": 3500},
                        {"nombre": "Fondo_C", "peso": 5000, "ganancia": 4000},
                        {"nombre": "Fondo_D", "peso": 3000, "ganancia": 2500},
                        {"nombre": "Fondo_E", "peso": 1500, "ganancia": 1800}
                    ]
                },
                "salida_esperada": {
                    "seleccionados": ["Fondo_B", "Fondo_C", "Fondo_E"],
                    "ganancia_total": 9300,
                    "peso_total": 10000,
                    "capacidad_utilizada": 100.0,
                    "eficiencia": 0.93
                }
            },
            "caso_2": {
                "descripcion": "Capacidad limitada",
                "entrada": {
                    "capacidad": 8000,
                    "objetos": [
                        {"nombre": "Acción_X", "peso": 1000, "ganancia": 800},
                        {"nombre": "Acción_Y", "peso": 2500, "ganancia": 2200},
                        {"nombre": "Acción_Z", "peso": 3000, "ganancia": 2800},
                        {"nombre": "Bono_P", "peso": 4000, "ganancia": 3000},
                        {"nombre": "Bono_Q", "peso": 1500, "ganancia": 1200}
                    ]
                },
                "salida_esperada": {
                    "seleccionados": ["Acción_Y", "Acción_Z", "Bono_Q"],
                    "ganancia_total": 6200,
                    "peso_total": 7000,
                    "capacidad_utilizada": 87.5,
                    "eficiencia": 0.8857
                }
            }
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
