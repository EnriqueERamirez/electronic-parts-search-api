from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List
from models.base import (
    ComponentSearchRequest,
    ComponentSearchResponse,
    GenericComponent,
    DistributorEnum
)
from services.aggregator_service import ComponentAggregatorService
from config import get_settings, Settings


router = APIRouter(prefix="/components", tags=["Components"])


def get_aggregator_service(settings: Settings = Depends(get_settings)) -> ComponentAggregatorService:
    """Dependencia para obtener el servicio agregador"""
    return ComponentAggregatorService(settings)


@router.get("/distributors", response_model=List[str])
async def get_available_distributors(
    service: ComponentAggregatorService = Depends(get_aggregator_service)
):
    """
    Obtiene la lista de distribuidores disponibles
    
    Returns:
        Lista de nombres de distribuidores configurados
    """
    return service.get_available_distributors()


@router.post("/search", response_model=ComponentSearchResponse)
async def search_components(
    request: ComponentSearchRequest,
    service: ComponentAggregatorService = Depends(get_aggregator_service)
):
    """
    Busca componentes electrónicos en uno o múltiples distribuidores
    
    Args:
        request: Parámetros de búsqueda
        - keywords: Palabras clave (requerido)
        - distributors: Lista de distribuidores específicos o null para buscar en todos
        - max_results: Número máximo de resultados por distribuidor (default: 50)
        - offset: Offset para paginación (default: 0)
        - filters: Filtros adicionales específicos del distribuidor
        - locale_language: Código de idioma (default: "en")
        - locale_currency: Código de moneda (default: "USD")
        - locale_site: Código de sitio (default: "US")
    
    Returns:
        Respuesta con componentes encontrados y metadata
        
    Example:
        ```json
        {
            "keywords": "STM32F103",
            "distributors": ["digikey", "mouser"],
            "max_results": 20
        }
        ```
        
        Para buscar en todos los distribuidores, omite o deja null el campo "distributors":
        ```json
        {
            "keywords": "STM32F103",
            "max_results": 20
        }
        ```
    """
    try:
        return await service.search_components(
            keywords=request.keywords,
            distributors=request.distributors,
            max_results=request.max_results,
            offset=request.offset,
            filters=request.filters,
            locale_language=request.locale_language,
            locale_currency=request.locale_currency,
            locale_site=request.locale_site
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching components: {str(e)}"
        )


@router.get("/search", response_model=ComponentSearchResponse)
async def search_components_get(
    keywords: str = Query(..., description="Palabras clave para buscar"),
    distributors: Optional[str] = Query(
        None,
        description="Distribuidores separados por coma (ej: 'digikey,mouser') o vacío para todos"
    ),
    max_results: int = Query(50, ge=1, le=100, description="Máximo de resultados por distribuidor"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    locale_language: str = Query("en", description="Código de idioma"),
    locale_currency: str = Query("USD", description="Código de moneda"),
    locale_site: str = Query("US", description="Código de sitio"),
    service: ComponentAggregatorService = Depends(get_aggregator_service)
):
    """
    Busca componentes usando query parameters (método GET)
    
    Args:
        keywords: Palabras clave de búsqueda
        distributors: Distribuidores separados por coma o vacío para todos
        max_results: Número máximo de resultados
        offset: Offset para paginación
        locale_language: Código de idioma
        locale_currency: Código de moneda
        locale_site: Código de sitio
    
    Returns:
        Respuesta con componentes encontrados
        
    Example:
        GET /components/search?keywords=STM32F103&distributors=digikey,mouser&max_results=20
        GET /components/search?keywords=resistor+10k  (busca en todos los distribuidores)
    """
    try:
        # Parsear distribuidores
        distributor_list = None
        if distributors:
            distributor_list = [
                DistributorEnum(d.strip().lower()) 
                for d in distributors.split(",")
                if d.strip()
            ]
        
        return await service.search_components(
            keywords=keywords,
            distributors=distributor_list,
            max_results=max_results,
            offset=offset,
            locale_language=locale_language,
            locale_currency=locale_currency,
            locale_site=locale_site
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid distributor name: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching components: {str(e)}"
        )


@router.get("/{distributor}/{part_number}", response_model=GenericComponent)
async def get_component_details(
    distributor: DistributorEnum,
    part_number: str,
    locale_language: str = Query("en", description="Código de idioma"),
    locale_currency: str = Query("USD", description="Código de moneda"),
    locale_site: str = Query("US", description="Código de sitio"),
    service: ComponentAggregatorService = Depends(get_aggregator_service)
):
    """
    Obtiene detalles de un componente específico de un distribuidor
    
    Args:
        distributor: Nombre del distribuidor (digikey, mouser, farnell)
        part_number: Número de parte del distribuidor
        locale_language: Código de idioma
        locale_currency: Código de moneda
        locale_site: Código de sitio
    
    Returns:
        Detalles del componente en formato genérico
        
    Example:
        GET /components/digikey/296-6501-1-ND
    """
    try:
        component = await service.get_component_details(
            distributor=distributor,
            part_number=part_number,
            locale_language=locale_language,
            locale_currency=locale_currency,
            locale_site=locale_site
        )
        
        if not component:
            raise HTTPException(
                status_code=404,
                detail=f"Component not found in {distributor}"
            )
        
        return component
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching component details: {str(e)}"
        )


@router.get("/compare/{manufacturer_part_number}", response_model=List[GenericComponent])
async def compare_component_across_distributors(
    manufacturer_part_number: str,
    distributors: Optional[str] = Query(
        None,
        description="Distribuidores a comparar, separados por coma"
    ),
    locale_language: str = Query("en", description="Código de idioma"),
    locale_currency: str = Query("USD", description="Código de moneda"),
    locale_site: str = Query("US", description="Código de sitio"),
    service: ComponentAggregatorService = Depends(get_aggregator_service)
):
    """
    Compara el mismo componente (por número de parte del fabricante) en diferentes distribuidores
    
    Args:
        manufacturer_part_number: Número de parte del fabricante
        distributors: Distribuidores a comparar (opcional, por defecto todos)
        locale_language: Código de idioma
        locale_currency: Código de moneda
        locale_site: Código de sitio
    
    Returns:
        Lista de componentes del mismo fabricante en diferentes distribuidores
        
    Example:
        GET /components/compare/STM32F103C8T6
        GET /components/compare/STM32F103C8T6?distributors=digikey,mouser
    """
    try:
        # Parsear distribuidores
        distributor_list = None
        if distributors:
            distributor_list = [
                DistributorEnum(d.strip().lower()) 
                for d in distributors.split(",")
                if d.strip()
            ]
        
        components = await service.compare_component_across_distributors(
            manufacturer_part_number=manufacturer_part_number,
            distributors=distributor_list,
            locale_language=locale_language,
            locale_currency=locale_currency,
            locale_site=locale_site
        )
        
        if not components:
            raise HTTPException(
                status_code=404,
                detail=f"Component {manufacturer_part_number} not found in any distributor"
            )
        
        return components
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid distributor name: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error comparing components: {str(e)}"
        )
