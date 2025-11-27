import httpx
from typing import Optional, List, Dict, Any
from services.base_service import BaseDistributorService
from services.auth.digikey_auth import DigiKeyAuthService
from models.base import GenericComponent, PriceBreak, ComponentParameter
from models.digikey import (
    DigiKeyProduct,
    DigiKeyProductSearchResponse,
    DigiKeyManufacturersResponse,
    DigiKeyCategoriesResponse
)
from config import Settings


class DigiKeyService(BaseDistributorService):
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

    @property
    def distributor_name(self) -> str:
        return "DigiKey"

    async def is_available(self) -> bool:
        """Verifica si el servicio DigiKey está configurado"""
        return bool(
            self.settings.digikey_client_id and 
            self.settings.digikey_client_secret
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

    async def search_components(
        self,
        keywords: str,
        max_results: int = 50,
        offset: int = 0,
        filters: Optional[Dict[str, Any]] = None,
        locale_language: str = "en",
        locale_currency: str = "USD",
        locale_site: str = "US"
    ) -> List[GenericComponent]:
        """Busca componentes en DigiKey"""
        url = f"{self.base_url}/products/{self.api_version}/search/keyword"
        
        headers = await self._get_headers(locale_language, locale_currency, locale_site)
        
        payload = {
            "Keywords": keywords,
            "RecordCount": min(max_results, 50),  # DigiKey max is 50
            "RecordStartPosition": offset
        }
        
        if filters:
            payload["FilterOptionsRequest"] = filters

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            search_response = DigiKeyProductSearchResponse(**data)
            
            return [
                self._convert_to_generic(product) 
                for product in search_response.products
            ]

    async def get_component_details(
        self,
        part_number: str,
        locale_language: str = "en",
        locale_currency: str = "USD",
        locale_site: str = "US"
    ) -> GenericComponent:
        """Obtiene detalles de un componente específico"""
        url = f"{self.base_url}/products/{self.api_version}/search/{part_number}/productdetails"
        
        headers = await self._get_headers(locale_language, locale_currency, locale_site)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            product = DigiKeyProduct(**data)
            return self._convert_to_generic(product)

    async def get_manufacturers(
        self,
        locale_language: str = "en",
        locale_site: str = "US"
    ) -> DigiKeyManufacturersResponse:
        """Obtiene lista de fabricantes"""
        url = f"{self.base_url}/products/{self.api_version}/search/manufacturers"
        headers = await self._get_headers(locale_language, "USD", locale_site)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return DigiKeyManufacturersResponse(**data)

    async def get_categories(
        self,
        locale_language: str = "en",
        locale_site: str = "US"
    ) -> DigiKeyCategoriesResponse:
        """Obtiene lista de categorías"""
        url = f"{self.base_url}/products/{self.api_version}/search/categories"
        headers = await self._get_headers(locale_language, "USD", locale_site)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return DigiKeyCategoriesResponse(**data)

    async def get_category_by_id(
        self,
        category_id: int,
        locale_language: str = "en",
        locale_site: str = "US"
    ) -> Dict[str, Any]:
        """Obtiene detalles de una categoría específica"""
        url = f"{self.base_url}/products/{self.api_version}/search/categories/{category_id}"
        headers = await self._get_headers(locale_language, "USD", locale_site)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

    def _convert_to_generic(self, product: DigiKeyProduct) -> GenericComponent:
        """Convierte un producto DigiKey al formato genérico"""
        
        # Convertir price breaks
        price_breaks = []
        if product.standard_pricing and product.standard_pricing.price_breaks:
            price_breaks = [
                PriceBreak(
                    quantity=pb.break_quantity,
                    unit_price=pb.unit_price,
                    total_price=pb.total_price
                )
                for pb in product.standard_pricing.price_breaks
            ]
        
        # Convertir parámetros
        parameters = [
            ComponentParameter(
                name=param.parameter,
                value=param.value
            )
            for param in product.parameters
        ]
        
        # Obtener precio unitario
        unit_price = None
        if price_breaks:
            unit_price = price_breaks[0].unit_price
        elif product.unit_price:
            unit_price = product.unit_price
        
        return GenericComponent(
            distributor="DigiKey",
            distributor_part_number=product.digi_key_part_number,
            manufacturer=product.manufacturer or "",
            manufacturer_part_number=product.manufacturer_part_number,
            description=product.description or "",
            detailed_description=product.detailed_description,
            quantity_available=product.quantity_available,
            minimum_order_quantity=product.minimum_order_quantity,
            unit_price=unit_price,
            price_breaks=price_breaks,
            datasheet_url=product.primary_datasheet,
            product_url=f"https://www.digikey.com/product-detail/en/-/{product.digi_key_part_number}",
            image_url=product.primary_photo,
            parameters=parameters,
            packaging=product.packaging,
            series=product.series,
            product_status=product.product_status,
            rohs_status=product.rohs_status,
            raw_data=product.model_dump(by_alias=True)
        )
