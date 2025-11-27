from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import components, digikey_advanced
from config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    API para búsqueda y comparación de componentes electrónicos en múltiples distribuidores.
    
    ## Características
    
    * **Búsqueda unificada**: Busca componentes en múltiples distribuidores con una sola consulta
    * **Comparación de precios**: Compara el mismo componente en diferentes distribuidores
    * **Formato genérico**: Respuestas normalizadas independientes del distribuidor
    * **Búsqueda flexible**: Busca en todos los distribuidores o selecciona específicos
    
    ## Distribuidores soportados
    
    * DigiKey
    * Mouser (próximamente)
    * Farnell (próximamente)
    
    ## Uso básico
    
    ### Buscar en todos los distribuidores
    ```
    POST /components/search
    {
        "keywords": "STM32F103",
        "max_results": 20
    }
    ```
    
    ### Buscar en distribuidores específicos
    ```
    POST /components/search
    {
        "keywords": "STM32F103",
        "distributors": ["digikey", "mouser"],
        "max_results": 20
    }
    ```
    
    ### Comparar precios
    ```
    GET /components/compare/STM32F103C8T6
    ```
    """
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(components.router)
app.include_router(digikey_advanced.router)


@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "endpoints": {
            "search": "/components/search",
            "compare": "/components/compare/{manufacturer_part_number}",
            "details": "/components/{distributor}/{part_number}",
            "distributors": "/components/distributors",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
