from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Dict, Any
from services.digikey_service import DigiKeyService
from models.digikey import (
    DigiKeyManufacturersResponse,
    DigiKeyCategoriesResponse
)
from config import get_settings, Settings


router = APIRouter(prefix="/digikey", tags=["DigiKey Advanced"])


def get_digikey_service(settings: Settings = Depends(get_settings)) -> DigiKeyService:
    """Dependencia para obtener el servicio DigiKey"""
    return DigiKeyService(settings)


@router.get("/manufacturers", response_model=DigiKeyManufacturersResponse)
async def get_manufacturers(
    locale_language: str = Query("en", description="Código de idioma"),
    locale_site: str = Query("US", description="Código de sitio"),
    service: DigiKeyService = Depends(get_digikey_service)
):
    """
    Obtiene la lista de fabricantes disponibles en DigiKey
    
    Args:
        locale_language: Código de idioma
        locale_site: Código de sitio
    
    Returns:
        Lista de fabricantes con IDs y nombres
    """
    try:
        if not await service.is_available():
            raise HTTPException(
                status_code=503,
                detail="DigiKey service is not configured"
            )
        
        return await service.get_manufacturers(
            locale_language=locale_language,
            locale_site=locale_site
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching manufacturers: {str(e)}"
        )


@router.get("/categories", response_model=DigiKeyCategoriesResponse)
async def get_categories(
    locale_language: str = Query("en", description="Código de idioma"),
    locale_site: str = Query("US", description="Código de sitio"),
    service: DigiKeyService = Depends(get_digikey_service)
):
    """
    Obtiene la lista de categorías de productos en DigiKey
    
    Args:
        locale_language: Código de idioma
        locale_site: Código de sitio
    
    Returns:
        Lista de categorías con IDs, nombres y padres
    """
    try:
        if not await service.is_available():
            raise HTTPException(
                status_code=503,
                detail="DigiKey service is not configured"
            )
        
        return await service.get_categories(
            locale_language=locale_language,
            locale_site=locale_site
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching categories: {str(e)}"
        )


@router.get("/categories/{category_id}", response_model=Dict[str, Any])
async def get_category_by_id(
    category_id: int,
    locale_language: str = Query("en", description="Código de idioma"),
    locale_site: str = Query("US", description="Código de sitio"),
    service: DigiKeyService = Depends(get_digikey_service)
):
    """
    Obtiene detalles de una categoría específica
    
    Args:
        category_id: ID de la categoría
        locale_language: Código de idioma
        locale_site: Código de sitio
    
    Returns:
        Detalles de la categoría
    """
    try:
        if not await service.is_available():
            raise HTTPException(
                status_code=503,
                detail="DigiKey service is not configured"
            )
        
        return await service.get_category_by_id(
            category_id=category_id,
            locale_language=locale_language,
            locale_site=locale_site
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching category: {str(e)}"
        )
