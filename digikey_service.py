import httpx
from typing import Optional, List, Dict, Any
from app.core.config import Settings
from app.services.auth import DigiKeyAuthService
from app.models.digikey import (
    ProductSearchResponse,
    Product,
    GenericProductResponse,
    ManufacturersResponse,
    CategoriesResponse
)


class DigiKeyService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = (
            settings.digikey_sandbox_url if settings.digikey_use_sandbox 
            else settings.digikey_api_url
        )
        self.api_version = "v4"
        self.auth_service = DigiKeyAuthService(
            client_id=settings.digikey_client_id,
            client_secret=settings.digikey_client_secret,
            api_url=self.base_url
        )

    async def _get_headers(
        self,
        locale_language: str = "en",
        locale_currency: str = "USD",
        locale_site: str = "US"
    ) -> Dict[str, str]:
        token = await self.auth_service.get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "X-DIGIKEY-Client-Id": self.settings.digikey_client_id,
            "X-DIGIKEY-Locale-Language": locale_language,
            "X-DIGIKEY-Locale-Currency": locale_currency,
            "X-DIGIKEY-Locale-Site": locale_site,
            "Content-Type": "application/json"
        }

    async def search_keyword(
        self,
        keywords: str,
        record_count: int = 50,
        record_start_pos: int = 0,
        filters: Optional[Dict[str, Any]] = None,
        sort: Optional[Dict[str, str]] = None,
        locale_language: str = "en",
        locale_currency: str = "USD",
        locale_site: str = "US"
    ) -> ProductSearchResponse:
        url = f"{self.base_url}/products/{self.api_version}/search/keyword"
        
        headers = await self._get_headers(locale_language, locale_currency, locale_site)
        
        payload = {
            "Keywords": keywords,
            "RecordCount": record_count,
            "RecordStartPosition": record_start_pos
        }
        
        if filters:
            payload["FilterOptionsRequest"] = filters
        
        if sort:
            payload["SortOptions"] = sort

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return ProductSearchResponse(**data)

    async def get_product_details(
        self,
        product_number: str,
        locale_language: str = "en",
        locale_currency: str = "USD",
        locale_site: str = "US"
    ) -> Product:
        url = f"{self.base_url}/products/{self.api_version}/search/{product_number}/productdetails"
        
        headers = await self._get_headers(locale_language, locale_currency, locale_site)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return Product(**data)

    async def get_manufacturers(
        self,
        locale_language: str = "en",
        locale_site: str = "US"
    ) -> ManufacturersResponse:
        url = f"{self.base_url}/products/{self.api_version}/search/manufacturers"
        
        headers = await self._get_headers(locale_language, "USD", locale_site)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return ManufacturersResponse(**data)

    async def get_categories(
        self,
        locale_language: str = "en",
        locale_site: str = "US"
    ) -> CategoriesResponse:
        url = f"{self.base_url}/products/{self.api_version}/search/categories"
        
        headers = await self._get_headers(locale_language, "USD", locale_site)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return CategoriesResponse(**data)

    async def get_category_by_id(
        self,
        category_id: int,
        locale_language: str = "en",
        locale_site: str = "US"
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/products/{self.api_version}/search/categories/{category_id}"
        
        headers = await self._get_headers(locale_language, "USD", locale_site)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

    async def get_product_pricing(
        self,
        product_number: str,
        locale_language: str = "en",
        locale_currency: str = "USD",
        locale_site: str = "US"
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/products/{self.api_version}/search/{product_number}/pricing"
        
        headers = await self._get_headers(locale_language, locale_currency, locale_site)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

    def convert_to_generic_product(self, product: Product) -> GenericProductResponse:
        parameters = {}
        for param in product.parameters:
            parameters[param.parameter] = param.value

        unit_price = None
        if product.standard_pricing and product.standard_pricing.price_breaks:
            unit_price = product.standard_pricing.price_breaks[0].unit_price

        return GenericProductResponse(
            distributor="DigiKey",
            part_number=product.digi_key_part_number,
            manufacturer=product.manufacturer or "",
            manufacturer_part_number=product.manufacturer_part_number,
            description=product.description or "",
            quantity_available=product.quantity_available,
            unit_price=unit_price,
            datasheet_url=product.primary_datasheet,
            product_url=f"https://www.digikey.com/product-detail/en/-/{product.digi_key_part_number}",
            parameters=parameters,
            raw_data=product.model_dump(by_alias=True)
        )
