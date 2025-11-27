import asyncio
from typing import List, Optional, Dict, Any
from time import time
from services.base_service import BaseDistributorService
from services.digikey_service import DigiKeyService
from models.base import (
    GenericComponent,
    ComponentSearchResponse,
    DistributorEnum
)
from config import Settings


class ComponentAggregatorService:
    """Servicio que agrega búsquedas de múltiples distribuidores"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self._services: Dict[str, BaseDistributorService] = {}
        self._initialize_services()
    
    def _initialize_services(self):
        """Inicializa los servicios de distribuidores disponibles"""
        # DigiKey
        if self.settings.digikey_client_id and self.settings.digikey_client_secret:
            self._services[DistributorEnum.DIGIKEY] = DigiKeyService(self.settings)
        
        # Aquí se pueden agregar más distribuidores
        # if self.settings.mouser_api_key:
        #     self._services[DistributorEnum.MOUSER] = MouserService(self.settings)
        # if self.settings.farnell_api_key:
        #     self._services[DistributorEnum.FARNELL] = FarnellService(self.settings)
    
    def get_available_distributors(self) -> List[str]:
        """Retorna lista de distribuidores disponibles"""
        return list(self._services.keys())
    
    async def search_components(
        self,
        keywords: str,
        distributors: Optional[List[DistributorEnum]] = None,
        max_results: int = 50,
        offset: int = 0,
        filters: Optional[Dict[str, Any]] = None,
        locale_language: str = "en",
        locale_currency: str = "USD",
        locale_site: str = "US"
    ) -> ComponentSearchResponse:
        """
        Busca componentes en uno o múltiples distribuidores
        
        Args:
            keywords: Palabras clave de búsqueda
            distributors: Lista de distribuidores específicos o None para todos
            max_results: Número máximo de resultados por distribuidor
            offset: Offset para paginación
            filters: Filtros adicionales
            locale_language: Código de idioma
            locale_currency: Código de moneda
            locale_site: Código de sitio
            
        Returns:
            ComponentSearchResponse con componentes agregados
        """
        start_time = time()
        
        # Determinar qué servicios usar
        if distributors:
            services_to_use = {
                dist: service 
                for dist, service in self._services.items() 
                if dist in distributors
            }
        else:
            services_to_use = self._services
        
        if not services_to_use:
            return ComponentSearchResponse(
                components=[],
                total_count=0,
                distributors_searched=[],
                search_time_ms=0
            )
        
        # Ejecutar búsquedas en paralelo
        tasks = []
        for distributor_name, service in services_to_use.items():
            task = self._safe_search(
                service,
                keywords,
                max_results,
                offset,
                filters,
                locale_language,
                locale_currency,
                locale_site
            )
            tasks.append((distributor_name, task))
        
        # Esperar todas las búsquedas
        results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        # Consolidar resultados
        all_components = []
        distributors_searched = []
        
        for (distributor_name, _), result in zip(tasks, results):
            if isinstance(result, Exception):
                # Log error pero continuar con otros distribuidores
                print(f"Error searching {distributor_name}: {str(result)}")
                continue
            
            if result:
                all_components.extend(result)
                distributors_searched.append(distributor_name)
        
        end_time = time()
        search_time_ms = (end_time - start_time) * 1000
        
        return ComponentSearchResponse(
            components=all_components,
            total_count=len(all_components),
            distributors_searched=distributors_searched,
            search_time_ms=search_time_ms
        )
    
    async def _safe_search(
        self,
        service: BaseDistributorService,
        keywords: str,
        max_results: int,
        offset: int,
        filters: Optional[Dict[str, Any]],
        locale_language: str,
        locale_currency: str,
        locale_site: str
    ) -> List[GenericComponent]:
        """Ejecuta búsqueda en un servicio con manejo de errores"""
        try:
            if not await service.is_available():
                return []
            
            return await service.search_components(
                keywords=keywords,
                max_results=max_results,
                offset=offset,
                filters=filters,
                locale_language=locale_language,
                locale_currency=locale_currency,
                locale_site=locale_site
            )
        except Exception as e:
            print(f"Error in {service.distributor_name}: {str(e)}")
            return []
    
    async def get_component_details(
        self,
        distributor: DistributorEnum,
        part_number: str,
        locale_language: str = "en",
        locale_currency: str = "USD",
        locale_site: str = "US"
    ) -> Optional[GenericComponent]:
        """
        Obtiene detalles de un componente específico de un distribuidor
        
        Args:
            distributor: Distribuidor del que obtener el componente
            part_number: Número de parte del distribuidor
            locale_language: Código de idioma
            locale_currency: Código de moneda
            locale_site: Código de sitio
            
        Returns:
            Componente o None si no se encuentra
        """
        service = self._services.get(distributor)
        if not service:
            return None
        
        try:
            return await service.get_component_details(
                part_number=part_number,
                locale_language=locale_language,
                locale_currency=locale_currency,
                locale_site=locale_site
            )
        except Exception as e:
            print(f"Error getting component details from {distributor}: {str(e)}")
            return None
    
    async def compare_component_across_distributors(
        self,
        manufacturer_part_number: str,
        distributors: Optional[List[DistributorEnum]] = None,
        locale_language: str = "en",
        locale_currency: str = "USD",
        locale_site: str = "US"
    ) -> List[GenericComponent]:
        """
        Busca el mismo componente en múltiples distribuidores para comparar
        
        Args:
            manufacturer_part_number: Número de parte del fabricante
            distributors: Lista de distribuidores o None para todos
            locale_language: Código de idioma
            locale_currency: Código de moneda
            locale_site: Código de sitio
            
        Returns:
            Lista de componentes del mismo fabricante en diferentes distribuidores
        """
        search_response = await self.search_components(
            keywords=manufacturer_part_number,
            distributors=distributors,
            max_results=10,
            locale_language=locale_language,
            locale_currency=locale_currency,
            locale_site=locale_site
        )
        
        # Filtrar solo los que coincidan exactamente con el número de parte
        matching_components = [
            comp for comp in search_response.components
            if comp.manufacturer_part_number.lower() == manufacturer_part_number.lower()
        ]
        
        return matching_components
