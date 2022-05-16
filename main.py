from fastapi import FastAPI
from routers.users_router import user_router
from routers.orders_router import order_router


app = FastAPI()

app.include_router(user_router)
app.include_router(order_router)
