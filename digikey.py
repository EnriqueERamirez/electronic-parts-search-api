from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class PriceBreak(BaseModel):
    break_quantity: int = Field(alias="BreakQuantity")
    unit_price: float = Field(alias="UnitPrice")
    total_price: float = Field(alias="TotalPrice")

    class Config:
        populate_by_name = True


class StandardPricing(BaseModel):
    price_breaks: List[PriceBreak] = Field(default_factory=list, alias="PriceBreaks")

    class Config:
        populate_by_name = True


class ParameterValue(BaseModel):
    parameter: str = Field(alias="Parameter")
    value: str = Field(alias="Value")

    class Config:
        populate_by_name = True


class MediaLinks(BaseModel):
    media_type: Optional[str] = Field(None, alias="MediaType")
    title: Optional[str] = Field(None, alias="Title")
    url: Optional[str] = Field(None, alias="Url")

    class Config:
        populate_by_name = True


class Product(BaseModel):
    digi_key_part_number: str = Field(alias="DigiKeyPartNumber")
    manufacturer_part_number: str = Field(alias="ManufacturerPartNumber")
    manufacturer: Optional[str] = Field(None, alias="Manufacturer")
    description: Optional[str] = Field(None, alias="Description")
    detailed_description: Optional[str] = Field(None, alias="DetailedDescription")
    quantity_available: int = Field(default=0, alias="QuantityAvailable")
    minimum_order_quantity: int = Field(default=1, alias="MinimumOrderQuantity")
    packaging: Optional[str] = Field(None, alias="Packaging")
    series: Optional[str] = Field(None, alias="Series")
    product_status: Optional[str] = Field(None, alias="ProductStatus")
    unit_price: Optional[float] = Field(None, alias="UnitPrice")
    standard_pricing: Optional[StandardPricing] = Field(None, alias="StandardPricing")
    manufacturer_public_quantity: Optional[int] = Field(None, alias="ManufacturerPublicQuantity")
    parameters: List[ParameterValue] = Field(default_factory=list, alias="Parameters")
    media_links: List[MediaLinks] = Field(default_factory=list, alias="MediaLinks")
    primary_datasheet: Optional[str] = Field(None, alias="PrimaryDatasheet")
    primary_photo: Optional[str] = Field(None, alias="PrimaryPhoto")
    primary_video: Optional[str] = Field(None, alias="PrimaryVideo")
    rohs_status: Optional[str] = Field(None, alias="RohsStatus")

    class Config:
        populate_by_name = True


class ProductSearchResponse(BaseModel):
    products: List[Product] = Field(default_factory=list, alias="Products")
    products_count: int = Field(default=0, alias="ProductsCount")
    exact_manufacturer_products_count: int = Field(default=0, alias="ExactManufacturerProductsCount")
    exact_digi_key_products_count: int = Field(default=0, alias="ExactDigiKeyProductsCount")

    class Config:
        populate_by_name = True


class ManufacturerInfo(BaseModel):
    id: int = Field(alias="Id")
    name: str = Field(alias="Name")

    class Config:
        populate_by_name = True


class ManufacturersResponse(BaseModel):
    manufacturers: List[ManufacturerInfo] = Field(default_factory=list, alias="Manufacturers")

    class Config:
        populate_by_name = True


class CategoryInfo(BaseModel):
    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    parent_id: Optional[int] = Field(None, alias="ParentId")

    class Config:
        populate_by_name = True


class CategoriesResponse(BaseModel):
    categories: List[CategoryInfo] = Field(default_factory=list, alias="Categories")

    class Config:
        populate_by_name = True


class SearchRequest(BaseModel):
    keywords: str
    record_count: int = Field(default=50, ge=1, le=50)
    record_start_pos: int = Field(default=0, ge=0)
    filters: Optional[Dict[str, Any]] = None
    sort: Optional[Dict[str, str]] = None


class GenericProductResponse(BaseModel):
    distributor: str
    part_number: str
    manufacturer: str
    manufacturer_part_number: str
    description: str
    quantity_available: int
    unit_price: Optional[float]
    datasheet_url: Optional[str]
    product_url: Optional[str]
    parameters: Dict[str, str]
    raw_data: Dict[str, Any]
