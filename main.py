from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from typing import Optional, List
import json
import asyncio
from sample_data import SAMPLE_PRODUCTS

app = FastAPI(
    title="Product Inventory API",
    description="TM Forum Product Inventory Management API - GET Operations Only",
    version="5.0.0",
    servers=[
        {
            "url": "https://tm-product-inventory.27jid12fsm9n.us-south.codeengine.appdomain.cloud",
            "description": "Production server"
        }
    ]
)


@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Product Inventory API",
        "version": "5.0.0",
        "operations": {
            "GET /product/{id}": "Retrieve a product by ID",
            "GET /product": "List or find product objects"
        }
    }


@app.get("/product/{product_id}")
def get_product_by_id(
    product_id: str,
    fields: Optional[str] = Query(None, description="Comma-separated list of fields to include")
):
    """
    Retrieves a Product by ID
    
    This operation retrieves a Product entity. Attribute selection is enabled 
    for all first level attributes.
    
    **Usage:**
    - GET /product/g265-tf85
    - GET /product/g265-tf86?fields=id,name,status
    """
    if product_id not in SAMPLE_PRODUCTS:
        raise HTTPException(status_code=404, detail=f"Product with id '{product_id}' not found")
    
    product = SAMPLE_PRODUCTS[product_id].copy()
    
    # Handle field selection if specified
    if fields:
        field_list = [f.strip() for f in fields.split(',')]
        filtered_product = {}
        for field in field_list:
            if field in product:
                filtered_product[field] = product[field]
        return filtered_product
    
    return product


@app.get("/product")
def list_products(
    fields: Optional[str] = Query(None, description="Comma-separated list of fields to include"),
    status: Optional[str] = Query(None, description="Filter by product status"),
    name: Optional[str] = Query(None, description="Filter by product name (partial match)"),
    limit: Optional[int] = Query(None, description="Maximum number of results to return"),
    offset: Optional[int] = Query(0, description="Number of results to skip")
):
    """
    List or find Product objects
    
    This operation lists Product entities. Attribute selection is enabled 
    for all first level attributes. Filtering is available.
    
    **Usage:**
    - GET /product
    - GET /product?status=created
    - GET /product?fields=id,name,status
    - GET /product?status=suspended&limit=10
    """
    products = list(SAMPLE_PRODUCTS.values())
    
    # Apply filters
    if status:
        products = [p for p in products if p.get('status') == status]
    
    if name:
        products = [p for p in products if name.lower() in p.get('name', '').lower()]
    
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
            filtered_product = {}
            for field in field_list:
                if field in product:
                    filtered_product[field] = product[field]
            filtered_products.append(filtered_product)
        return filtered_products
    
    return products


@app.get("/sse")
async def sse_endpoint(request: Request):
    """
    Server-Sent Events endpoint for MCP protocol
    Implements MCP over SSE transport for Context Forge integration
    """
    async def event_generator():
        try:
            # Send MCP initialization response
            init_response = {
                "jsonrpc": "2.0",
                "id": 1,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {
                            "listChanged": False
                        }
                    },
                    "serverInfo": {
                        "name": "product-inventory",
                        "version": "5.0.0"
                    }
                }
            }
            yield f"data: {json.dumps(init_response)}\n\n"
            
            # Send tools list
            tools_response = {
                "jsonrpc": "2.0",
                "method": "notifications/tools/list_changed",
                "params": {}
            }
            yield f"data: {json.dumps(tools_response)}\n\n"
            
            # Keep connection alive with ping
            while True:
                if await request.is_disconnected():
                    break
                
                # Send ping every 15 seconds
                ping = {
                    "jsonrpc": "2.0",
                    "method": "notifications/ping",
                    "params": {}
                }
                yield f"data: {json.dumps(ping)}\n\n"
                await asyncio.sleep(15)
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            error_msg = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            yield f"data: {json.dumps(error_msg)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*"
        }
    )


@app.post("/sse")
async def sse_post_endpoint(request: Request):
    """
    Handle MCP protocol messages via POST
    Context Forge sends initialization and tool requests here
    """
    try:
        body = await request.json()
        
        # Handle initialize request
        if body.get("method") == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": body.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "product-inventory",
                        "version": "5.0.0"
                    }
                }
            }
        
        # Handle tools/list request
        elif body.get("method") == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": body.get("id"),
                "result": {
                    "tools": [
                        {
                            "name": "get_product_by_id",
                            "description": "Retrieve a product by its ID",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "product_id": {"type": "string"},
                                    "fields": {"type": "string"}
                                },
                                "required": ["product_id"]
                            }
                        },
                        {
                            "name": "list_products",
                            "description": "List products with filtering",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "status": {"type": "string"},
                                    "name": {"type": "string"},
                                    "limit": {"type": "integer"}
                                }
                            }
                        }
                    ]
                }
            }
        
        # Handle tools/call request
        elif body.get("method") == "tools/call":
            tool_name = body.get("params", {}).get("name")
            arguments = body.get("params", {}).get("arguments", {})
            
            if tool_name == "get_product_by_id":
                product_id = arguments.get("product_id")
                if product_id in SAMPLE_PRODUCTS:
                    return {
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(SAMPLE_PRODUCTS[product_id], indent=2)
                                }
                            ]
                        }
                    }
            elif tool_name == "list_products":
                products = list(SAMPLE_PRODUCTS.values())
                status = arguments.get("status")
                if status:
                    products = [p for p in products if p.get("status") == status]
                return {
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(products, indent=2)
                            }
                        ]
                    }
                }
        
        return {
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "error": {
                "code": -32601,
                "message": "Method not found"
            }
        }
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }


@app.get("/mcp/tools")
async def list_mcp_tools():
    """
    List available MCP tools for Context Forge
    """
    return {
        "tools": [
            {
                "name": "get_product_by_id",
                "description": "Retrieve a product by its ID. Returns complete product details including characteristics, pricing, terms, and related parties.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "The unique identifier of the product (e.g., 'g265-tf85', 'prod-001')"
                        },
                        "fields": {
                            "type": "string",
                            "description": "Optional comma-separated list of fields to include in response"
                        }
                    },
                    "required": ["product_id"]
                }
            },
            {
                "name": "list_products",
                "description": "List or find product objects with optional filtering. Supports filtering by status, name, and pagination.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "description": "Filter by product status",
                            "enum": ["active", "created", "suspended"]
                        },
                        "name": {
                            "type": "string",
                            "description": "Filter by product name (partial match)"
                        },
                        "fields": {
                            "type": "string",
                            "description": "Comma-separated list of fields to include"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return"
                        },
                        "offset": {
                            "type": "integer",
                            "description": "Number of results to skip for pagination"
                        }
                    }
                }
            },
            {
                "name": "get_products_by_customer",
                "description": "Find all products associated with a specific customer name.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "customer_name": {
                            "type": "string",
                            "description": "Customer name to search for"
                        }
                    },
                    "required": ["customer_name"]
                }
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Made with Bob
