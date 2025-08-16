# Documentación de la API - Microservicio de Optimización de Portafolio

## Información General

- **Base URL**: `http://localhost:8000`
- **Versión**: 1.0.0
- **Formato de respuesta**: JSON
- **Autenticación**: No requerida
  
## Endpoints

### 1. Información del Servicio

#### GET /
Obtiene información básica del servicio.

**Respuesta:**
```json
{
  "mensaje": "Microservicio de Optimización de Portafolio de Inversiones",
  "version": "1.0.0",
  "endpoints": {
    "optimizar": "/optimizar",
    "documentacion": "/docs",
    "health": "/health"
  }
}
```

### 2. Verificación de Salud

#### GET /health
Verifica el estado del servicio.

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": 1703123456.789,
  "service": "portfolio-optimizer"
}
```

### 3. Optimización de Portafolio

#### POST /optimizar
Optimiza la selección de inversiones para maximizar la ganancia sin exceder la capacidad presupuestaria.

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "capacidad": 10000,
  "objetos": [
    {
      "nombre": "Fondo_A",
      "peso": 2000,
      "ganancia": 1500
    },
    {
      "nombre": "Fondo_B",
      "peso": 4000,
      "ganancia": 3500
    }
  ]
}
```

**Respuesta:**
```json
{
  "seleccionados": ["Fondo_B"],
  "ganancia_total": 3500,
  "peso_total": 4000,
  "capacidad_utilizada": 40.0,
  "eficiencia": 0.875
}
```

### 4. Optimización Detallada

#### POST /optimizar/detallado
Proporciona un análisis detallado de la optimización incluyendo estadísticas y eficiencias.

**Headers:**
```
Content-Type: application/json
```

**Body:** (Mismo formato que `/optimizar`)

**Respuesta:**
```json
{
  "resultado_optimizacion": {
    "seleccionados": ["Fondo_B", "Fondo_C", "Fondo_E"],
    "ganancia_total": 9300,
    "peso_total": 10000,
    "capacidad_utilizada": 100.0,
    "eficiencia": 0.93
  },
  "estadisticas": {
    "total_objetos_disponibles": 5,
    "objetos_seleccionados": 3,
    "porcentaje_seleccion": 60.0,
    "ganancia_total_disponible": 13300,
    "ganancia_obtenida": 9300,
    "porcentaje_ganancia_obtenida": 69.92,
    "peso_total_disponible": 14000,
    "peso_utilizado": 10000,
    "porcentaje_peso_utilizado": 71.43
  },
  "eficiencias_objetos": [
    {
      "nombre": "Fondo_E",
      "eficiencia": 1.2,
      "ganancia": 1800,
      "peso": 1500
    },
    {
      "nombre": "Fondo_B",
      "eficiencia": 0.875,
      "ganancia": 3500,
      "peso": 4000
    }
  ],
  "rendimiento": {
    "tiempo_ejecucion_ms": 15.23,
    "timestamp": 1703123456.789
  }
}
```

### 5. Ejemplos de Uso

#### GET /ejemplos
Proporciona ejemplos de casos de uso de la API.

**Respuesta:**
```json
{
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
    }
  }
}
```

## Códigos de Error

### 400 Bad Request
```json
{
  "error": "Error de validación de datos",
  "detalles": "La capacidad debe ser mayor que 0",
  "tipo": "VALIDATION_ERROR"
}
```

### 422 Unprocessable Entity
```json
{
  "error": "Error de validación de modelo",
  "detalles": [
    {
      "loc": ["body", "objetos", 0, "peso"],
      "msg": "El peso debe ser mayor que 0",
      "type": "value_error"
    }
  ],
  "tipo": "MODEL_VALIDATION_ERROR"
}
```

### 500 Internal Server Error
```json
{
  "error": "Error interno del servidor",
  "detalles": "Ha ocurrido un error inesperado",
  "tipo": "INTERNAL_ERROR"
}
```

## Validaciones

### Capacidad
- Debe ser un número entero positivo
- Máximo: 10,000,000
- Mínimo: 1

### Objetos
- Debe contener al menos un objeto
- Máximo: 1000 objetos

### Nombre del Objeto
- No puede estar vacío
- Máximo: 50 caracteres
- Debe ser único entre todos los objetos

### Peso (Costo)
- Debe ser un número entero positivo
- Máximo: 1,000,000
- Mínimo: 1

### Ganancia
- Debe ser un número entero no negativo
- Máximo: 1,000,000
- Mínimo: 0

## Casos de Prueba

### Caso 1: Máximo aprovechamiento de capacidad
**Entrada:**
```json
{
  "capacidad": 10000,
  "objetos": [
    {"nombre": "Fondo_A", "peso": 2000, "ganancia": 1500},
    {"nombre": "Fondo_B", "peso": 4000, "ganancia": 3500},
    {"nombre": "Fondo_C", "peso": 5000, "ganancia": 4000},
    {"nombre": "Fondo_D", "peso": 3000, "ganancia": 2500},
    {"nombre": "Fondo_E", "peso": 1500, "ganancia": 1800}
  ]
}
```

**Salida esperada:**
```json
{
  "seleccionados": ["Fondo_B", "Fondo_C", "Fondo_E"],
  "ganancia_total": 9300,
  "peso_total": 10000,
  "capacidad_utilizada": 100.0,
  "eficiencia": 0.93
}
```

### Caso 2: Capacidad limitada
**Entrada:**
```json
{
  "capacidad": 8000,
  "objetos": [
    {"nombre": "Acción_X", "peso": 1000, "ganancia": 800},
    {"nombre": "Acción_Y", "peso": 2500, "ganancia": 2200},
    {"nombre": "Acción_Z", "peso": 3000, "ganancia": 2800},
    {"nombre": "Bono_P", "peso": 4000, "ganancia": 3000},
    {"nombre": "Bono_Q", "peso": 1500, "ganancia": 1200}
  ]
}
```

**Salida esperada:**
```json
{
  "seleccionados": ["Acción_Y", "Acción_Z", "Bono_Q"],
  "ganancia_total": 6200,
  "peso_total": 7000,
  "capacidad_utilizada": 87.5,
  "eficiencia": 0.8857
}
```

### Caso 3: Proyectos de bajo costo, alta rentabilidad
**Entrada:**
```json
{
  "capacidad": 5000,
  "objetos": [
    {"nombre": "Cripto_1", "peso": 500, "ganancia": 700},
    {"nombre": "Cripto_2", "peso": 800, "ganancia": 1000},
    {"nombre": "ETF_1", "peso": 1500, "ganancia": 1300},
    {"nombre": "ETF_2", "peso": 2000, "ganancia": 1800},
    {"nombre": "NFT_Alpha", "peso": 3000, "ganancia": 2500}
  ]
}
```

**Salida esperada:**
```json
{
  "seleccionados": ["Cripto_1", "Cripto_2", "ETF_2", "ETF_1"],
  "ganancia_total": 4800,
  "peso_total": 5000,
  "capacidad_utilizada": 100.0,
  "eficiencia": 0.96
}
```

## Límites y Rendimiento

### Límites de la API
- **Tamaño máximo de request**: 10MB
- **Tiempo máximo de respuesta**: 30 segundos
- **Máximo de objetos por request**: 1000
- **Máximo de requests por minuto**: 100

### Rendimiento
- **Tiempo promedio de respuesta**: < 100ms
- **Uso de memoria**: < 100MB por request
- **Algoritmo**: Programación dinámica O(n*W)

## Documentación Interactiva

La API incluye documentación interactiva generada automáticamente:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Ejemplos de Uso con cURL

### Optimización básica
```bash
curl -X POST "http://localhost:8000/optimizar" \
  -H "Content-Type: application/json" \
  -d '{
    "capacidad": 10000,
    "objetos": [
      {"nombre": "Fondo_A", "peso": 2000, "ganancia": 1500},
      {"nombre": "Fondo_B", "peso": 4000, "ganancia": 3500},
      {"nombre": "Fondo_C", "peso": 5000, "ganancia": 4000}
    ]
  }'
```

### Optimización detallada
```bash
curl -X POST "http://localhost:8000/optimizar/detallado" \
  -H "Content-Type: application/json" \
  -d '{
    "capacidad": 10000,
    "objetos": [
      {"nombre": "Fondo_A", "peso": 2000, "ganancia": 1500},
      {"nombre": "Fondo_B", "peso": 4000, "ganancia": 3500},
      {"nombre": "Fondo_C", "peso": 5000, "ganancia": 4000}
    ]
  }'
```

### Verificar salud del servicio
```bash
curl -X GET "http://localhost:8000/health"
```

## Notas de Implementación

### Algoritmo Utilizado
El microservicio utiliza **programación dinámica** para resolver el problema de la mochila (Knapsack Problem):

- **Complejidad temporal**: O(n * W) donde n es el número de objetos y W es la capacidad
- **Complejidad espacial**: O(n * W)
- **Optimalidad**: Garantiza la solución óptima en todos los casos

### Validaciones Implementadas
1. **Validación de tipos**: Todos los campos deben tener el tipo correcto
2. **Validación de rangos**: Los valores deben estar dentro de los límites permitidos
3. **Validación de unicidad**: Los nombres de los objetos deben ser únicos
4. **Validación de consistencia**: Los datos deben ser consistentes entre sí

### Manejo de Errores
- **Errores de validación**: Se devuelven con código 422 y detalles específicos
- **Errores de servidor**: Se devuelven con código 500 y mensaje genérico
- **Errores de cliente**: Se devuelven con código 400 y explicación del problema

### Logging
El servicio registra:
- Todas las solicitudes de optimización
- Errores y excepciones
- Tiempos de respuesta
- Estadísticas de uso
