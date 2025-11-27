from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from models.base import GenericComponent


class BaseDistributorService(ABC):
    """Interfaz base para servicios de distribuidores"""
    
    @property
    @abstractmethod
    def distributor_name(self) -> str:
        """Nombre del distribuidor"""
        pass
    
    @abstractmethod
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
        """
        Busca componentes por palabras clave
        
        Args:
            keywords: Términos de búsqueda
            max_results: Número máximo de resultados
            offset: Offset para paginación
            filters: Filtros adicionales específicos del distribuidor
            locale_language: Código de idioma
            locale_currency: Código de moneda
            locale_site: Código de sitio
            
        Returns:
            Lista de componentes en formato genérico
        """
        pass
    
    @abstractmethod
    async def get_component_details(
        self,
        part_number: str,
        locale_language: str = "en",
        locale_currency: str = "USD",
        locale_site: str = "US"
    ) -> GenericComponent:
        """
        Obtiene detalles de un componente específico
        
        Args:
            part_number: Número de parte del distribuidor
            locale_language: Código de idioma
            locale_currency: Código de moneda
            locale_site: Código de sitio
            
        Returns:
            Componente en formato genérico
        """
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """
        Verifica si el servicio está disponible
        
        Returns:
            True si el servicio está configurado y disponible
        """
        pass
