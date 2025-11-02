from fastapi import FastAPI
from fastapi.routing import APIRoute
from src.routes import scraper_route, user_route, alert_route, scrap_and_notify_route

app = FastAPI(title="Price Tracker API")

app.include_router(scraper_route.router, prefix="/api/scraper", tags=["Scraper"])
app.include_router(user_route.router, prefix="/api/user", tags=["User"])
app.include_router(alert_route.router, prefix="/api/alert", tags=["Alert"])
app.include_router(scrap_and_notify_route.router, prefix="/api/scrap-and-notify", tags=["Scraper & Notifier"])
# app.include_router(graph_routes.router, prefix="/api/graph", tags=["Graphs"])

@app.get("/")
def root():
    return {"message": "Price Tracker API is live..."}

import pprint

@app.on_event("startup")
def list_routes():
    routes = [route.path for route in app.routes if isinstance(route, APIRoute)]
    pprint.pp(routes)


# @app.get("/about")
# def read_about():
#     return {"message": "About page"}

# @app.get("/contact")
# def read_contact():
#     return {"message": "Contact page"}

# @app.get("/products/{product_id}")
# def read_product(product_id: int):
#     return {"message": f"Product {product_id}"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# from pydantic import BaseModel
# class Product(BaseModel):
#     id: int
#     name: str
#     price: float

# @app.post("/products")
# def create_product(product: Product):
#     return {"message": f"Product {product.name} created"}

# @app.put("/products/{product_id}")
# def update_product(product_id: int, product: Product):
#     return {"message": f"Product {product.name} updated"}

# @app.delete("/products/{product_id}")
# def delete_product(product_id: int):
#     return {"message": f"Product {product_id} deleted"}

# @app.get("/products")
# def get_products():
#     return {"message": "Products fetched"}

# @app.get("/products/{product_id}")
# def get_product(product_id: int):
#     return {"message": f"Product {product_id} fetched"}