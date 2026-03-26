#!/usr/bin/env python3
"""
Product Inventory MCP Server
TM Forum TMF637-compliant Product Inventory Management API as an MCP server
"""

import json
import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP
import mcp.types as types
from pydantic import AnyUrl
from sample_data import SAMPLE_PRODUCTS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Instructions for the MCP server
INSTRUCTIONS = """
This is a TM Forum Product Inventory Management API (TMF637) MCP server.
It provides access to product inventory data following the TMF637 specification.

Available tools:
- get_product_by_id: Retrieve a product by its unique identifier
- list_products: List and filter products by status, name, with pagination
- get_products_by_customer: Find all products associated with a specific customer

All products follow TMF637 standard with proper structure including:
- Product characteristics
- Pricing information
- Product terms
- Related parties
- Service references
"""

class ProductInventoryMCPServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8000, path: str = "/mcp"):
        self.host = host
        self.port = port
        self.path = path
        self.server = None
        
    async def list_resources(self) -> list[types.Resource]:
        """List available product resources"""
        return [
            types.Resource(
                uri=AnyUrl(f"product://inventory/{product_id}"),
                name=f"Product: {product['name']}",
                description=f"Product {product_id} - Status: {product.get('status', 'unknown')}",
                mimeType="application/json",
            )
            for product_id, product in SAMPLE_PRODUCTS.items()
        ]
    
    async def read_resource(self, uri: AnyUrl) -> str:
        """Read a specific product resource"""
        if uri.scheme != "product":
            raise ValueError(f"Unsupported URI scheme: {uri.scheme}")
        
        product_id = uri.path
        if product_id is not None:
            product_id = product_id.lstrip("/")
            if product_id in SAMPLE_PRODUCTS:
                return json.dumps(SAMPLE_PRODUCTS[product_id], indent=2)
        
        raise ValueError(f"Product not found: {product_id}")
    
    async def list_tools(self) -> list[types.Tool]:
        """List available tools"""
        logger.info("Listing Product Inventory tools")
        
        return [
            types.Tool(
                name="get_product_by_id",
                description="Retrieve a product by its ID. Returns complete product details including characteristics, pricing, terms, and related parties.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "The unique identifier of the product (e.g., 'g265-tf85', 'prod-001')"
                        },
                        "fields": {
                            "type": "string",
                            "description": "Optional comma-separated list of fields to include in response (e.g., 'id,name,status')"
                        }
                    },
                    "required": ["product_id"]
                }
            ),
            types.Tool(
                name="list_products",
                description="List or find product objects with optional filtering. Supports filtering by status, name, and pagination.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "description": "Filter by product status",
                            "enum": ["active", "created", "suspended"]
                        },
                        "name": {
                            "type": "string",
                            "description": "Filter by product name (partial match, case-insensitive)"
                        },
                        "fields": {
                            "type": "string",
                            "description": "Comma-separated list of fields to include (e.g., 'id,name,status')"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return"
                        },
                        "offset": {
                            "type": "integer",
                            "description": "Number of results to skip for pagination",
                            "default": 0
                        }
                    }
                }
            ),
            types.Tool(
                name="get_products_by_customer",
                description="Find all products associated with a specific customer name. Searches through related parties.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "customer_name": {
                            "type": "string",
                            "description": "Customer name to search for (e.g., 'Jean', 'Sarah Johnson')"
                        }
                    },
                    "required": ["customer_name"]
                }
            )
        ]
    
    async def call_tool(self, name: str, arguments: dict | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Execute a tool"""
        logger.info(f"Calling tool: {name} with arguments: {arguments}")
        
        if arguments is None:
            arguments = {}
        
        if name == "get_product_by_id":
            product_id = arguments.get("product_id")
            fields = arguments.get("fields")
            
            if product_id not in SAMPLE_PRODUCTS:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"Product with id '{product_id}' not found",
                        "available_ids": list(SAMPLE_PRODUCTS.keys())
                    }, indent=2)
                )]
            
            product = SAMPLE_PRODUCTS[product_id].copy()
            
            # Handle field selection
            if fields:
                field_list = [f.strip() for f in fields.split(',')]
                filtered_product = {k: v for k, v in product.items() if k in field_list}
                product = filtered_product
            
            return [types.TextContent(
                type="text",
                text=json.dumps(product, indent=2)
            )]
        
        elif name == "list_products":
            status = arguments.get("status")
            name_filter = arguments.get("name")
            fields = arguments.get("fields")
            limit = arguments.get("limit")
            offset = arguments.get("offset", 0)
            
            products = list(SAMPLE_PRODUCTS.values())
            
            # Apply filters
            if status:
                products = [p for p in products if p.get('status') == status]
            
            if name_filter:
                products = [p for p in products if name_filter.lower() in p.get('name', '').lower()]
            
            # Apply pagination
            if offset:
                products = products[offset:]
            
            if limit:
                products = products[:limit]
            
            # Apply field selection
            if fields:
                field_list = [f.strip() for f in fields.split(',')]
                filtered_products = []
                for product in products:
                    filtered_product = {k: v for k, v in product.items() if k in field_list}
                    filtered_products.append(filtered_product)
                products = filtered_products
            
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "count": len(products),
                    "products": products
                }, indent=2)
            )]
        
        elif name == "get_products_by_customer":
            customer_name = arguments.get("customer_name")
            
            matching_products = []
            for product in SAMPLE_PRODUCTS.values():
                # Check in relatedParty
                related_parties = product.get("relatedParty", [])
                for party in related_parties:
                    party_info = party.get("partyOrPartyRole", {})
                    if customer_name.lower() in party_info.get("name", "").lower():
                        matching_products.append(product)
                        break
                
                # Also check in product name
                if customer_name.lower() in product.get("name", "").lower():
                    if product not in matching_products:
                        matching_products.append(product)
            
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "customer": customer_name,
                    "count": len(matching_products),
                    "products": matching_products
                }, indent=2)
            )]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    def start(self, transport: str = "sse"):
        """Start the MCP server"""
        logger.info(f"Starting Product Inventory MCP Server on {self.host}:{self.port}{self.path}")
        
        self.server = FastMCP(
            name="product-inventory",
            instructions=INSTRUCTIONS,
            host=self.host,
            port=self.port,
            sse_path=self.path,
            streamable_http_path=self.path,
        )
        
        # Register handlers
        self.server._mcp_server.list_resources()(self.list_resources)
        self.server._mcp_server.read_resource()(self.read_resource)
        self.server._mcp_server.list_tools()(self.list_tools)
        self.server._mcp_server.call_tool()(self.call_tool)
        
        # Run the server
        self.server.run(transport=transport)


def main():
    """Main entry point"""
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description="Product Inventory MCP Server")
    parser.add_argument("--host", type=str, default=os.getenv("HOST", "0.0.0.0"), help="Host to bind to")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")), help="Port to bind to")
    parser.add_argument("--path", type=str, default=os.getenv("MCP_PATH", "/mcp"), help="MCP endpoint path")
    parser.add_argument("--transport", type=str, default=os.getenv("TRANSPORT", "sse"), choices=["stdio", "sse"], help="Transport type")
    
    args = parser.parse_args()
    
    server = ProductInventoryMCPServer(
        host=args.host,
        port=args.port,
        path=args.path
    )
    
    server.start(transport=args.transport)


if __name__ == "__main__":
    main()

# Made with Bob