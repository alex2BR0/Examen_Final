# Microservicio de Optimización de Portafolio de Inversiones

## Descripción

Este proyecto implementa un microservicio que resuelve el problema de optimización de portafolio de inversiones con restricción presupuestaria, utilizando el algoritmo de la mochila (Knapsack Problem) mediante programación dinámica.

## Características

- **Backend**: Microservicio REST API con algoritmo de programación dinámica
- **Frontend**: Interfaz web moderna y responsive
- **Validación**: Manejo completo de errores y validación de datos
- **Documentación**: API documentada con OpenAPI/Swagger
- **Docker**: Contenedorización completa del proyecto

## Estructura del Proyecto

```
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── optimizer.py
│   │   └── validators.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_optimizer.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Instalación y Despliegue

### Opción 1: Usando Docker (Recomendado)

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd examen-final
```

2. Ejecuta con Docker Compose:
```bash
docker-compose up --build
```

3. Accede a la aplicación:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Documentación API: http://localhost:8000/docs

### Opción 2: Instalación Manual

#### Backend

1. Navega al directorio backend:
```bash
cd backend
```

2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecuta el servidor:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

1. Navega al directorio frontend:
```bash
cd frontend
```

2. Abre `index.html` en tu navegador o usa un servidor local:
```bash
python -m http.server 3000
```

## Uso de la API

### Endpoint: POST /optimizar

**URL**: `http://localhost:8000/optimizar`

**Headers**:
```
Content-Type: application/json
```

**Ejemplo de entrada**:
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

**Ejemplo de salida**:
```json
{
  "seleccionados": ["Fondo_B", "Fondo_C", "Fondo_E"],
  "ganancia_total": 9300,
  "peso_total": 10000
}
```

## Casos de Prueba

### Caso 1: Máximo aprovechamiento de capacidad
- **Capacidad**: 10000
- **Resultado esperado**: Ganancia total de 9300 con peso total de 10000

### Caso 2: Capacidad limitada
- **Capacidad**: 8000
- **Resultado esperado**: Combinación óptima sin exceder la capacidad

### Caso 3: Proyectos de bajo costo
- **Capacidad**: 5000
- **Resultado esperado**: Selección de proyectos más rentables

## Tecnologías Utilizadas

### Backend
- **Python 3.9+**
- **FastAPI**: Framework web moderno y rápido
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

### Frontend
- **HTML5/CSS3**: Estructura y estilos
- **JavaScript ES6+**: Lógica de la interfaz
- **Chart.js**: Visualización de datos

### DevOps
- **Docker**: Contenedorización
- **Docker Compose**: Orquestación de servicios

## Algoritmo Implementado

El microservicio utiliza **programación dinámica** para resolver el problema de la mochila:

1. **Complejidad temporal**: O(n * W) donde n es el número de objetos y W es la capacidad
2. **Complejidad espacial**: O(n * W)
3. **Optimalidad**: Garantiza la solución óptima en todos los casos

## Validación de Errores

El sistema valida:
- Capacidad negativa o cero
- Datos faltantes en objetos
- Valores no numéricos
- Nombres duplicados
- Pesos o ganancias negativas

## Pruebas

Para ejecutar las pruebas:

```bash
cd backend
python -m pytest tests/
```

Las pruebas cubren:
- Casos de éxito básicos
- Casos límite (capacidad = 0, objetos vacíos)
- Manejo de errores
- Validación de datos

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

 
## Autor
Bryan Alexander Alarcón Iza 