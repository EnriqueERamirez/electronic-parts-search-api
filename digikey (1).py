from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, Dict, Any, List
from app.models.digikey import (
    ProductSearchResponse,
    Product,
    SearchRequest,
    GenericProductResponse,
    ManufacturersResponse,
    CategoriesResponse
)
from app.services import DigiKeyService
from app.core.config import get_settings, Settings


router = APIRouter(prefix="/digikey", tags=["DigiKey"])


def get_digikey_service(settings: Settings = Depends(get_settings)) -> DigiKeyService:
    return DigiKeyService(settings)


@router.post("/search", response_model=ProductSearchResponse)
async def search_products(
    request: SearchRequest,
    locale_language: str = Query("en", description="Language code (en, ja, de, fr, etc.)"),
    locale_currency: str = Query("USD", description="Currency code (USD, EUR, GBP, etc.)"),
    locale_site: str = Query("US", description="Site code (US, JP, UK, etc.)"),
    service: DigiKeyService = Depends(get_digikey_service)
):
    try:
        return await service.search_keyword(
            keywords=request.keywords,
            record_count=request.record_count,
            record_start_pos=request.record_start_pos,
            filters=request.filters,
            sort=request.sort,
            locale_language=locale_language,
            locale_currency=locale_currency,
            locale_site=locale_site
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching products: {str(e)}")


@router.post("/search/generic", response_model=List[GenericProductResponse])
async def search_products_generic(
    request: SearchRequest,
    locale_language: str = Query("en", description="Language code"),
    locale_currency: str = Query("USD", description="Currency code"),
    locale_site: str = Query("US", description="Site code"),
    service: DigiKeyService = Depends(get_digikey_service)
):
    try:
        result = await service.search_keyword(
            keywords=request.keywords,
            record_count=request.record_count,
            record_start_pos=request.record_start_pos,
            filters=request.filters,
            sort=request.sort,
            locale_language=locale_language,
            locale_currency=locale_currency,
            locale_site=locale_site
        )
        
        return [service.convert_to_generic_product(p) for p in result.products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching products: {str(e)}")


@router.get("/product/{product_number}", response_model=Product)
async def get_product_details(
    product_number: str,
    locale_language: str = Query("en", description="Language code"),
    locale_currency: str = Query("USD", description="Currency code"),
    locale_site: str = Query("US", description="Site code"),
    service: DigiKeyService = Depends(get_digikey_service)
):
    try:
        return await service.get_product_details(
            product_number=product_number,
            locale_language=locale_language,
            locale_currency=locale_currency,
            locale_site=locale_site
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Product not found")
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")


@router.get("/product/{product_number}/generic", response_model=GenericProductResponse)
async def get_product_details_generic(
    product_number: str,
    locale_language: str = Query("en", description="Language code"),
    locale_currency: str = Query("USD", description="Currency code"),
    locale_site: str = Query("US", description="Site code"),
    service: DigiKeyService = Depends(get_digikey_service)
):
    try:
        product = await service.get_product_details(
            product_number=product_number,
            locale_language=locale_language,
            locale_currency=locale_currency,
            locale_site=locale_site
        )
        return service.convert_to_generic_product(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")


@router.get("/manufacturers", response_model=ManufacturersResponse)
async def get_manufacturers(
    locale_language: str = Query("en", description="Language code"),
    locale_site: str = Query("US", description="Site code"),
    service: DigiKeyService = Depends(get_digikey_service)
):
    try:
        return await service.get_manufacturers(
            locale_language=locale_language,
            locale_site=locale_site
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching manufacturers: {str(e)}")


@router.get("/categories", response_model=CategoriesResponse)
async def get_categories(
    locale_language: str = Query("en", description="Language code"),
    locale_site: str = Query("US", description="Site code"),
    service: DigiKeyService = Depends(get_digikey_service)
):
    try:
        return await service.get_categories(
            locale_language=locale_language,
            locale_site=locale_site
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")


@router.get("/categories/{category_id}")
async def get_category_by_id(
    category_id: int,
    locale_language: str = Query("en", description="Language code"),
    locale_site: str = Query("US", description="Site code"),
    service: DigiKeyService = Depends(get_digikey_service)
):
    try:
        return await service.get_category_by_id(
            category_id=category_id,
            locale_language=locale_language,
            locale_site=locale_site
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching category: {str(e)}")


@router.get("/product/{product_number}/pricing")
async def get_product_pricing(
    product_number: str,
    locale_language: str = Query("en", description="Language code"),
    locale_currency: str = Query("USD", description="Currency code"),
    locale_site: str = Query("US", description="Site code"),
    service: DigiKeyService = Depends(get_digikey_service)
):
    try:
        return await service.get_product_pricing(
            product_number=product_number,
            locale_language=locale_language,
            locale_currency=locale_currency,
            locale_site=locale_site
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pricing: {str(e)}")
