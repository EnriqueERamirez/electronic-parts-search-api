from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class DistributorEnum(str, Enum):
    DIGIKEY = "digikey"
    MOUSER = "mouser"
    FARNELL = "farnell"


class PriceBreak(BaseModel):
    quantity: int
    unit_price: float
    total_price: float


class ComponentParameter(BaseModel):
    name: str
    value: str
    unit: Optional[str] = None


class GenericComponent(BaseModel):
    """Modelo genérico para componentes de cualquier distribuidor"""
    distributor: str
    distributor_part_number: str
    manufacturer: str
    manufacturer_part_number: str
    description: str
    detailed_description: Optional[str] = None
    quantity_available: int
    minimum_order_quantity: int = 1
    unit_price: Optional[float] = None
    price_breaks: List[PriceBreak] = Field(default_factory=list)
    datasheet_url: Optional[str] = None
    product_url: Optional[str] = None
    image_url: Optional[str] = None
    parameters: List[ComponentParameter] = Field(default_factory=list)
    packaging: Optional[str] = None
    series: Optional[str] = None
    product_status: Optional[str] = None
    rohs_status: Optional[str] = None
    lifecycle_status: Optional[str] = None
    raw_data: Dict[str, Any] = Field(default_factory=dict)


class ComponentSearchRequest(BaseModel):
    """Request para búsqueda de componentes"""
    keywords: str = Field(..., description="Palabras clave para buscar")
    distributors: Optional[List[DistributorEnum]] = Field(
        None, 
        description="Lista de distribuidores a buscar. Si es None, busca en todos"
    )
    max_results: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    filters: Optional[Dict[str, Any]] = Field(
        None,
        description="Filtros específicos del distribuidor"
    )
    locale_language: str = Field(default="en")
    locale_currency: str = Field(default="USD")
    locale_site: str = Field(default="US")


class ComponentSearchResponse(BaseModel):
    """Respuesta de búsqueda de componentes"""
    components: List[GenericComponent]
    total_count: int
    distributors_searched: List[str]
    search_time_ms: Optional[float] = None


class DistributorAvailability(BaseModel):
    """Disponibilidad de un componente en diferentes distribuidores"""
    manufacturer_part_number: str
    distributors: List[GenericComponent]
