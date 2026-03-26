from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
from sample_data import SAMPLE_PRODUCTS

app = FastAPI(
    title="Product Inventory API",
    description="TM Forum Product Inventory Management API - GET Operations Only",
    version="5.0.0"
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Made with Bob
