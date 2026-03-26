"""
Sample data for TM Forum Product Inventory API (TMF637)
Contains example products following TMF637 Product Inventory Management specification v5.0.0
"""

SAMPLE_PRODUCTS = {
    "g265-tf85": {
        "id": "g265-tf85",
        "href": "https://host:port/productInventory/v5/product/g265-tf85",
        "description": "This product is an Product Specification instance",
        "isBundle": False,
        "isCustomerVisible": False,
        "name": "Voice Over IP Basic instance for Jean",
        "creationDate": "2021-04-12T23:59:59.52Z",
        "status": "created",
        "@type": "Product",
        "productCharacteristic": [
            {
                "@type": "BooleanCharacteristic",
                "id": "Char1",
                "name": "FixedIP",
                "valueType": "boolean",
                "value": False
            },
            {
                "@type": "ObjectCharacteristic",
                "id": "Char5",
                "name": "FiberSpeed",
                "valueType": "object",
                "value": {
                    "@type": "Speed",
                    "volume": 90,
                    "unit": "Mbps"
                }
            }
        ],
        "place": [
            {
                "role": "installationAddress",
                "place": {
                    "id": "9912",
                    "href": "https://host:port/geographicAddressManagement/v5/geographicAddress/9912",
                    "@referredType": "GeographicAddress",
                    "@type": "PlaceRef"
                },
                "@type": "RelatedPlaceRefOrValue"
            }
        ],
        "realizingService": [
            {
                "id": "7854",
                "href": "https://host:port/serviceInventory/v5/service/7854",
                "@referredType": "Service",
                "@type": "ServiceRef"
            }
        ],
        "productSpecification": {
            "id": "PS-101",
            "href": "https://host:port/productCatalogManagement/v5/productSpecification/PS-101",
            "@referredType": "ProductSpecification",
            "@type": "ProductSpecificationRef",
            "version": "1"
        },
        "relatedParty": [
            {
                "role": "User",
                "partyOrPartyRole": {
                    "id": "45hj-999",
                    "href": "https://host:port/partyManagement/v5/individual/45hj-999",
                    "name": "Louise",
                    "@type": "PartyRef",
                    "@referredType": "Individual"
                },
                "@type": "RelatedPartyOrPartyRole"
            }
        ]
    },
    "g265-tf86": {
        "id": "g265-tf86",
        "href": "https://host:port/productInventory/v5/product/g265-tf86",
        "description": "This product is an Product Offering instance",
        "isBundle": False,
        "isCustomerVisible": True,
        "name": "Voice Over IP Basic instance for Jean",
        "creationDate": "2021-04-12T23:59:59.52Z",
        "status": "created",
        "@type": "Product",
        "productOffering": {
            "id": "PO-101-1",
            "href": "https://host:port/productCatalogManagement/v5/productOffering/PO-101-1",
            "name": "Voice Over IP Basic",
            "@type": "ProductOfferingRef",
            "@referredType": "ProductOffering"
        },
        "productRelationship": [
            {
                "id": "g265-tf85",
                "href": "https://host:port/productInventory/v5/product/g265-tf85",
                "@type": "ProductRelationship",
                "relationshipType": "sells"
            }
        ],
        "productPrice": [
            {
                "@type": "ProductPrice",
                "productOfferingPrice": {
                    "id": "POP1",
                    "name": "Fiber recurring fee",
                    "href": "https://host:port/productCatalogManagement/v5/productOfferingPrice/POP1",
                    "@referredType": "ProductOfferingPrice",
                    "@type": "ProductOfferingPriceRef"
                },
                "recurringChargePeriod": "month",
                "price": {
                    "@type": "Price",
                    "taxIncludedAmount": {
                        "unit": "EUR",
                        "value": 29.99
                    },
                    "taxRate": 15
                },
                "priceType": "recurring"
            }
        ],
        "productTerm": [
            {
                "@type": "ProductTerm",
                "description": "Fiber standard commitment",
                "duration": {
                    "amount": 12,
                    "units": "month"
                },
                "validFor": {
                    "startDateTime": "2021-04-12T23:59:59.52Z",
                    "endDateTime": "2022-04-11T00:00:00.52Z"
                },
                "name": "12months commitment"
            }
        ],
        "relatedParty": [
            {
                "role": "owner",
                "partyOrPartyRole": {
                    "id": "45hj-8888",
                    "href": "https://host:port/partyManagement/v5/individual/45hj-8888",
                    "name": "Jean",
                    "@type": "PartyRef",
                    "@referredType": "Individual"
                },
                "@type": "RelatedPartyOrPartyRole"
            }
        ]
    },
    "9ffg-ze56-ed51": {
        "id": "9ffg-ze56-ed51",
        "href": "https://host:port/productInventory/v5/product/9ffg-ze56-ed51",
        "status": "suspended",
        "orderDate": "2019-04-11T14:52:21.823Z",
        "productOffering": {
            "id": "sxcv-fg65",
            "href": "https://host:port/productCatalogManagement/v5/productOffering/sxcv-fg65",
            "@type": "ProductOfferingRef",
            "@referredType": "ProductOffering",
            "name": "TMF 35 Bundle Plan"
        },
        "@type": "Product",
        "name": "TMF 35 Bundle Plan instance",
        "isBundle": True,
        "isCustomerVisible": True,
        "description": "Bundle product offering instance"
    },
    "7412": {
        "id": "7412",
        "href": "https://host:port/productInventory/v5/product/7412",
        "status": "suspended",
        "orderDate": "2019-04-18T14:21:31.325Z",
        "productOffering": {
            "id": "po-8965",
            "href": "https://host:port/productCatalogManagement/v5/productOffering/po-8965",
            "@type": "ProductOfferingRef",
            "@referredType": "ProductOffering",
            "name": "Premium Internet Service"
        },
        "@type": "Product",
        "name": "Premium Internet Service instance",
        "isBundle": False,
        "isCustomerVisible": True,
        "description": "High-speed internet product instance",
        "creationDate": "2019-04-18T14:21:31.325Z"
    },
    "prod-001": {
        "id": "prod-001",
        "href": "https://host:port/productInventory/v5/product/prod-001",
        "description": "Mobile phone service with data plan",
        "isBundle": False,
        "isCustomerVisible": True,
        "name": "Mobile Data Plan Premium",
        "creationDate": "2023-06-15T10:30:00.00Z",
        "orderDate": "2023-06-14T16:45:00.00Z",
        "status": "active",
        "@type": "Product",
        "productCharacteristic": [
            {
                "@type": "StringCharacteristic",
                "id": "char-mobile-001",
                "name": "phoneNumber",
                "valueType": "string",
                "value": "+1-555-0123"
            },
            {
                "@type": "StringCharacteristic",
                "id": "char-mobile-002",
                "name": "dataAllowance",
                "valueType": "string",
                "value": "50GB"
            },
            {
                "@type": "BooleanCharacteristic",
                "id": "char-mobile-003",
                "name": "internationalRoaming",
                "valueType": "boolean",
                "value": True
            }
        ],
        "productOffering": {
            "id": "offer-mobile-premium",
            "href": "https://host:port/productCatalogManagement/v5/productOffering/offer-mobile-premium",
            "name": "Mobile Premium Plan",
            "@type": "ProductOfferingRef",
            "@referredType": "ProductOffering"
        },
        "productPrice": [
            {
                "@type": "ProductPrice",
                "productOfferingPrice": {
                    "id": "price-mobile-001",
                    "name": "Monthly subscription",
                    "href": "https://host:port/productCatalogManagement/v5/productOfferingPrice/price-mobile-001",
                    "@referredType": "ProductOfferingPrice",
                    "@type": "ProductOfferingPriceRef"
                },
                "recurringChargePeriod": "month",
                "price": {
                    "@type": "Price",
                    "taxIncludedAmount": {
                        "unit": "USD",
                        "value": 65.00
                    },
                    "taxRate": 13
                },
                "priceType": "recurring"
            }
        ],
        "relatedParty": [
            {
                "role": "customer",
                "partyOrPartyRole": {
                    "id": "cust-001",
                    "href": "https://host:port/partyManagement/v5/individual/cust-001",
                    "name": "Sarah Johnson",
                    "@type": "PartyRef",
                    "@referredType": "Individual"
                },
                "@type": "RelatedPartyOrPartyRole"
            }
        ]
    },
    "prod-002": {
        "id": "prod-002",
        "href": "https://host:port/productInventory/v5/product/prod-002",
        "description": "Fiber optic internet connection",
        "isBundle": False,
        "isCustomerVisible": True,
        "name": "Fiber Internet 1Gbps",
        "creationDate": "2023-08-20T09:15:00.00Z",
        "orderDate": "2023-08-19T14:30:00.00Z",
        "status": "active",
        "@type": "Product",
        "productCharacteristic": [
            {
                "@type": "ObjectCharacteristic",
                "id": "char-fiber-001",
                "name": "downloadSpeed",
                "valueType": "object",
                "value": {
                    "@type": "Speed",
                    "volume": 1000,
                    "unit": "Mbps"
                }
            },
            {
                "@type": "ObjectCharacteristic",
                "id": "char-fiber-002",
                "name": "uploadSpeed",
                "valueType": "object",
                "value": {
                    "@type": "Speed",
                    "volume": 1000,
                    "unit": "Mbps"
                }
            },
            {
                "@type": "BooleanCharacteristic",
                "id": "char-fiber-003",
                "name": "staticIP",
                "valueType": "boolean",
                "value": True
            }
        ],
        "place": [
            {
                "role": "installationAddress",
                "place": {
                    "id": "addr-5678",
                    "href": "https://host:port/geographicAddressManagement/v5/geographicAddress/addr-5678",
                    "@referredType": "GeographicAddress",
                    "@type": "PlaceRef"
                },
                "@type": "RelatedPlaceRefOrValue"
            }
        ],
        "realizingService": [
            {
                "id": "svc-fiber-001",
                "href": "https://host:port/serviceInventory/v5/service/svc-fiber-001",
                "@referredType": "Service",
                "@type": "ServiceRef"
            }
        ],
        "productSpecification": {
            "id": "spec-fiber-1g",
            "href": "https://host:port/productCatalogManagement/v5/productSpecification/spec-fiber-1g",
            "@referredType": "ProductSpecification",
            "@type": "ProductSpecificationRef",
            "version": "2.0"
        },
        "productOffering": {
            "id": "offer-fiber-1g",
            "href": "https://host:port/productCatalogManagement/v5/productOffering/offer-fiber-1g",
            "name": "Fiber 1Gbps Plan",
            "@type": "ProductOfferingRef",
            "@referredType": "ProductOffering"
        },
        "productPrice": [
            {
                "@type": "ProductPrice",
                "productOfferingPrice": {
                    "id": "price-fiber-monthly",
                    "name": "Monthly subscription",
                    "href": "https://host:port/productCatalogManagement/v5/productOfferingPrice/price-fiber-monthly",
                    "@referredType": "ProductOfferingPrice",
                    "@type": "ProductOfferingPriceRef"
                },
                "recurringChargePeriod": "month",
                "price": {
                    "@type": "Price",
                    "taxIncludedAmount": {
                        "unit": "USD",
                        "value": 79.99
                    },
                    "taxRate": 13
                },
                "priceType": "recurring"
            },
            {
                "@type": "ProductPrice",
                "productOfferingPrice": {
                    "id": "price-fiber-install",
                    "name": "Installation fee",
                    "href": "https://host:port/productCatalogManagement/v5/productOfferingPrice/price-fiber-install",
                    "@referredType": "ProductOfferingPrice",
                    "@type": "ProductOfferingPriceRef"
                },
                "price": {
                    "@type": "Price",
                    "taxIncludedAmount": {
                        "unit": "USD",
                        "value": 99.00
                    },
                    "taxRate": 13
                },
                "priceType": "oneTime"
            }
        ],
        "productTerm": [
            {
                "@type": "ProductTerm",
                "description": "24 month commitment period",
                "duration": {
                    "amount": 24,
                    "units": "month"
                },
                "validFor": {
                    "startDateTime": "2023-08-20T00:00:00.00Z",
                    "endDateTime": "2025-08-20T00:00:00.00Z"
                },
                "name": "24 months commitment"
            }
        ],
        "relatedParty": [
            {
                "role": "customer",
                "partyOrPartyRole": {
                    "id": "cust-002",
                    "href": "https://host:port/partyManagement/v5/individual/cust-002",
                    "name": "Michael Chen",
                    "@type": "PartyRef",
                    "@referredType": "Individual"
                },
                "@type": "RelatedPartyOrPartyRole"
            }
        ]
    }
}

# Made with Bob