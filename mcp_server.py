#!/usr/bin/env python3
"""
MCP Server for TM Forum Product Inventory API
Provides tools to query product inventory following TMF637 specification
"""

import asyncio
import json
from typing import Any, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
from sample_data import SAMPLE_PRODUCTS

# Create MCP server instance
app = Server("product-inventory")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for product inventory operations"""
    return [
        Tool(
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
        Tool(
            name="list_products",
            description="List or find product objects with optional filtering. Supports filtering by status, name, and pagination.",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filter by product status (e.g., 'active', 'created', 'suspended')",
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
                },
                "required": []
            }
        ),
        Tool(
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


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "get_product_by_id":
        product_id = arguments.get("product_id")
        fields = arguments.get("fields")
        
        if product_id not in SAMPLE_PRODUCTS:
            return [TextContent(
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
        
        return [TextContent(
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
        
        return [TextContent(
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
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "customer": customer_name,
                "count": len(matching_products),
                "products": matching_products
            }, indent=2)
        )]
    
    else:
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown tool: {name}"}, indent=2)
        )]


async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob