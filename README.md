# Product Inventory API - GET Operations

A dummy API implementation based on TM Forum Product Inventory Management API specification, implementing **GET operations only** for retrieving product information.

## Overview

This API follows the TM Forum Uniform Contract for API operations:

| Operation on Entities | Uniform API Operation | Description |
|----------------------|----------------------|-------------|
| Query Entities | GET Resource | GET must be used to retrieve a representation of a resource |

## Features

- ✅ **GET /product/{id}** - Retrieve a product by ID
- ✅ **GET /product** - List or find product objects with filtering
- ✅ Field selection support
- ✅ Filtering by status, name
- ✅ Pagination support (limit, offset)
- ✅ Automatic API documentation (FastAPI/Swagger)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Get Product by ID

**Endpoint:** `GET /product/{id}`

**Description:** Retrieves a Product entity by its identifier.

**Examples:**

```bash
# Get product by ID
curl http://localhost:8000/product/g265-tf85

# Get product with field selection
curl http://localhost:8000/product/g265-tf85?fields=id,name,status
```

**Sample Response:**
```json
{
  "id": "g265-tf85",
  "href": "https://host:port/productInventory/v5/product/g265-tf85",
  "description": "This product is an Product Specification instance",
  "isBundle": false,
  "isCustomerVisible": false,
  "name": "Voice Over IP Basic instance for Jean",
  "creationDate": "2021-04-12T23:59:59.52Z",
  "status": "created",
  "@type": "Product"
}
```

### 2. List Products

**Endpoint:** `GET /product`

**Description:** Lists Product entities with optional filtering and pagination.

**Query Parameters:**
- `fields` - Comma-separated list of fields to include
- `status` - Filter by product status
- `name` - Filter by product name (partial match)
- `limit` - Maximum number of results
- `offset` - Number of results to skip

**Examples:**

```bash
# Get all products
curl http://localhost:8000/product

# Filter by status
curl http://localhost:8000/product?status=created

# Field selection
curl http://localhost:8000/product?fields=id,name,status

# Pagination
curl http://localhost:8000/product?limit=10&offset=0

# Combined filters
curl http://localhost:8000/product?status=created&fields=id,name
```

**Sample Response:**
```json
[
  {
    "id": "g265-tf85",
    "name": "Voice Over IP Basic instance for Jean",
    "status": "created",
    "@type": "Product"
  },
  {
    "id": "g265-tf86",
    "name": "Voice Over IP Basic instance for Jean",
    "status": "created",
    "@type": "Product"
  }
]
```

## Sample Data

The API includes **6 sample products** following the TMF637 Product Inventory Management API v5.0.0 standard:

### Available Products

1. **g265-tf85** - Product Specification instance (VoIP Basic) - status: `created`
2. **g265-tf86** - Product Offering instance (VoIP Basic) - status: `created`
3. **9ffg-ze56-ed51** - Bundle Plan - status: `suspended`
4. **7412** - Premium Internet Service - status: `suspended`
5. **prod-001** - Mobile Data Plan Premium - status: `active`
6. **prod-002** - Fiber Internet 1Gbps - status: `active`

### TM Forum Standard Compliance

All sample data follows TMF637 specification with:

✅ **Correct attribute naming and structure** per TMF637 specification
✅ **Proper use of @type, @referredType fields** for type identification
✅ **Standard reference objects:**
- ProductOfferingRef
- ProductSpecificationRef
- ServiceRef
- PlaceRef
- PartyRef

✅ **Correct ProductCharacteristic types:**
- BooleanCharacteristic
- StringCharacteristic
- ObjectCharacteristic

✅ **Proper ProductPrice structure** with taxIncludedAmount and taxRate
✅ **ProductTerm** with duration and validFor periods
✅ **RelatedParty** with role-based associations

The sample data matches the exact format shown in the TM Forum documentation examples and supports all GET operations defined in the API (filtering by status, name, field selection, pagination).

## MCP Server (Model Context Protocol)

This repository includes an **MCP server** implementation that allows AI agents to interact with the Product Inventory API through the Model Context Protocol.

### Running the MCP Server

```bash
# Install dependencies including MCP SDK
pip install -r requirements.txt

# Run the MCP server
python mcp_server.py
```

### MCP Tools Available

The MCP server provides three tools:

1. **get_product_by_id** - Retrieve a product by its unique identifier
   - Parameters: `product_id` (required), `fields` (optional)
   - Example: Get product "g265-tf85" with all details

2. **list_products** - List and filter products
   - Parameters: `status`, `name`, `fields`, `limit`, `offset` (all optional)
   - Example: List all active products

3. **get_products_by_customer** - Find products by customer name
   - Parameters: `customer_name` (required)
   - Example: Find all products for customer "Jean"

### Using with Context Forge

To use this MCP server with IBM Context Forge:

1. **Copy the repository** to your Context Forge MCP servers directory
2. **Add to Context Forge configuration** using `mcp-config.json`
3. **Or import via OpenAPI**: Use the OpenAPI spec at:
   ```
   https://tm-product-inventory.27jid12fsm9n.us-south.codeengine.appdomain.cloud/openapi.json
   ```

### MCP Configuration

The `mcp-config.json` file contains the server configuration:
- Server name: `product-inventory`
- Command: `python mcp_server.py`
- Category: Product Data
- Authentication: None (open access)

## Project Structure

```
.
├── main.py              # FastAPI application with GET endpoints
├── mcp_server.py        # MCP server implementation
├── mcp-config.json      # MCP server configuration
├── sample_data.py       # Sample product data (TMF637 compliant)
├── models.py            # Pydantic models for validation
├── requirements.txt     # Python dependencies (FastAPI + MCP)
└── README.md           # This file
```

## TM Forum Compliance

This implementation follows the TM Forum Product Inventory Management API specification:
- Uniform API operations for querying entities
- Standard resource structure
- Field selection support
- Filtering capabilities
- Proper HTTP status codes

## Notes

- This is a **dummy API** for testing and development purposes
- Only **GET operations** are implemented (Query Entities)
- Data is stored in memory (no database)
- The API returns static sample data from `sample_data.py`

## For AI Agent Integration

This API can be used as a tool for AI agents to:
- Query product information by ID
- List and filter products
- Retrieve specific product attributes using field selection
- Test product inventory workflows

The API follows REST principles and returns JSON responses that are easy to parse and process.