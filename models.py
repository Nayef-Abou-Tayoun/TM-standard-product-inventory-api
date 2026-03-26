from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class Price(BaseModel):
    type: str = Field(alias="@type", default="Price")
    taxIncludedAmount: dict
    taxRate: float


class ProductOfferingPriceRef(BaseModel):
    id: str
    name: str
    href: str
    referredType: str = Field(alias="@referredType")
    type: str = Field(alias="@type")


class ProductPrice(BaseModel):
    type: str = Field(alias="@type")
    productOfferingPrice: ProductOfferingPriceRef
    recurringChargePeriod: Optional[str] = None
    price: Price
    priceType: str


class ProductTerm(BaseModel):
    type: str = Field(alias="@type")
    description: str
    duration: dict
    validFor: dict
    name: str


class PlaceRef(BaseModel):
    id: str
    href: str
    referredType: str = Field(alias="@referredType")
    type: str = Field(alias="@type")


class RelatedPlaceRefOrValue(BaseModel):
    role: str
    place: PlaceRef
    type: str = Field(alias="@type")


class ServiceRef(BaseModel):
    id: str
    href: str
    referredType: str = Field(alias="@referredType")
    type: str = Field(alias="@type")


class ProductSpecificationRef(BaseModel):
    id: str
    href: str
    referredType: str = Field(alias="@referredType")
    type: str = Field(alias="@type")
    version: str


class ProductOfferingRef(BaseModel):
    id: str
    href: str
    name: str
    type: str = Field(alias="@type")
    referredType: str = Field(alias="@referredType")


class PartyRef(BaseModel):
    id: str
    href: str
    name: str
    type: str = Field(alias="@type")
    referredType: str = Field(alias="@referredType")


class RelatedPartyOrPartyRole(BaseModel):
    role: str
    partyOrPartyRole: PartyRef
    type: str = Field(alias="@type")


class ProductCharacteristic(BaseModel):
    type: str = Field(alias="@type")
    id: str
    name: str
    valueType: str
    value: Any


class ProductRelationship(BaseModel):
    id: str
    href: str
    type: str = Field(alias="@type")
    relationshipType: str


class Product(BaseModel):
    id: Optional[str] = None
    href: Optional[str] = None
    description: Optional[str] = None
    isBundle: Optional[bool] = False
    isCustomerVisible: Optional[bool] = False
    name: str
    creationDate: Optional[str] = None
    orderDate: Optional[str] = None
    status: str
    type: str = Field(alias="@type")
    productCharacteristic: Optional[List[ProductCharacteristic]] = None
    place: Optional[List[RelatedPlaceRefOrValue]] = None
    realizingService: Optional[List[ServiceRef]] = None
    productSpecification: Optional[ProductSpecificationRef] = None
    productOffering: Optional[ProductOfferingRef] = None
    productRelationship: Optional[List[ProductRelationship]] = None
    productPrice: Optional[List[ProductPrice]] = None
    productTerm: Optional[List[ProductTerm]] = None
    relatedParty: Optional[List[RelatedPartyOrPartyRole]] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Voice Over IP Basic instance",
                "status": "created",
                "@type": "Product"
            }
        }


class ProductCreate(BaseModel):
    description: Optional[str] = None
    isBundle: Optional[bool] = False
    isCustomerVisible: Optional[bool] = False
    name: str
    status: str
    type: str = Field(alias="@type")
    productCharacteristic: Optional[List[ProductCharacteristic]] = None
    place: Optional[List[RelatedPlaceRefOrValue]] = None
    realizingService: Optional[List[ServiceRef]] = None
    productSpecification: Optional[ProductSpecificationRef] = None
    productOffering: Optional[ProductOfferingRef] = None
    productRelationship: Optional[List[ProductRelationship]] = None
    productPrice: Optional[List[ProductPrice]] = None
    productTerm: Optional[List[ProductTerm]] = None
    relatedParty: Optional[List[RelatedPartyOrPartyRole]] = None

    class Config:
        populate_by_name = True

# Made with Bob
