from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class DigiKeyPriceBreak(BaseModel):
    break_quantity: int = Field(alias="BreakQuantity")
    unit_price: float = Field(alias="UnitPrice")
    total_price: float = Field(alias="TotalPrice")

    class Config:
        populate_by_name = True


class DigiKeyStandardPricing(BaseModel):
    price_breaks: List[DigiKeyPriceBreak] = Field(default_factory=list, alias="PriceBreaks")

    class Config:
        populate_by_name = True


class DigiKeyParameterValue(BaseModel):
    parameter: str = Field(alias="Parameter")
    value: str = Field(alias="Value")

    class Config:
        populate_by_name = True


class DigiKeyMediaLinks(BaseModel):
    media_type: Optional[str] = Field(None, alias="MediaType")
    title: Optional[str] = Field(None, alias="Title")
    url: Optional[str] = Field(None, alias="Url")

    class Config:
        populate_by_name = True


class DigiKeyProduct(BaseModel):
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
    standard_pricing: Optional[DigiKeyStandardPricing] = Field(None, alias="StandardPricing")
    manufacturer_public_quantity: Optional[int] = Field(None, alias="ManufacturerPublicQuantity")
    parameters: List[DigiKeyParameterValue] = Field(default_factory=list, alias="Parameters")
    media_links: List[DigiKeyMediaLinks] = Field(default_factory=list, alias="MediaLinks")
    primary_datasheet: Optional[str] = Field(None, alias="PrimaryDatasheet")
    primary_photo: Optional[str] = Field(None, alias="PrimaryPhoto")
    primary_video: Optional[str] = Field(None, alias="PrimaryVideo")
    rohs_status: Optional[str] = Field(None, alias="RohsStatus")

    class Config:
        populate_by_name = True


class DigiKeyProductSearchResponse(BaseModel):
    products: List[DigiKeyProduct] = Field(default_factory=list, alias="Products")
    products_count: int = Field(default=0, alias="ProductsCount")
    exact_manufacturer_products_count: int = Field(default=0, alias="ExactManufacturerProductsCount")
    exact_digi_key_products_count: int = Field(default=0, alias="ExactDigiKeyProductsCount")

    class Config:
        populate_by_name = True


class DigiKeyManufacturerInfo(BaseModel):
    id: int = Field(alias="Id")
    name: str = Field(alias="Name")

    class Config:
        populate_by_name = True


class DigiKeyManufacturersResponse(BaseModel):
    manufacturers: List[DigiKeyManufacturerInfo] = Field(default_factory=list, alias="Manufacturers")

    class Config:
        populate_by_name = True


class DigiKeyCategoryInfo(BaseModel):
    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    parent_id: Optional[int] = Field(None, alias="ParentId")

    class Config:
        populate_by_name = True


class DigiKeyCategoriesResponse(BaseModel):
    categories: List[DigiKeyCategoryInfo] = Field(default_factory=list, alias="Categories")

    class Config:
        populate_by_name = True
