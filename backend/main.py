from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import (
    health, merchants, orders, public_orders, payment,
    public_payments, test, test_jobs, admin, refunds, jobs,
    webhooks, webhook_logs
)

app = FastAPI(title="Payment Gateway API", version="1.0.0")

@app.on_event("startup")
def startup_db():
    Base.metadata.create_all(bind=engine)

# Allow CORS for merchant site + checkout page
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # dashboard if any
        "http://localhost:3001",  # checkout page
        "http://localhost:49674", # serve merchant-site (dynamic port)
        "*",  # allow all for testing/demo purposes
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(merchants.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(public_orders.router, prefix="/api/v1")
app.include_router(payment.router, prefix="/api/v1")
app.include_router(public_payments.router, prefix="/api/v1")
app.include_router(test.router, prefix="/api/v1")
app.include_router(test_jobs.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(refunds.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
app.include_router(webhooks.router, prefix="/api/v1")
app.include_router(webhook_logs.router, prefix="/api/v1")