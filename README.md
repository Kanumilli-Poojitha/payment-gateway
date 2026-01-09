Payment Gateway – Multi-Method Processing with Hosted Checkout

A fully containerized payment gateway system inspired by Razorpay/Stripe, supporting merchant onboarding, order management, UPI & Card payments, and a hosted checkout page.
Built to demonstrate real-world fintech concepts like authentication, validation, payment state machines, and end-to-end transaction flows.

Features:

* Merchant authentication using API Key & Secret
* Order creation and management APIs
* Multi-method payment processing:
    * UPI (with VPA validation)
    * Card payments (Luhn validation, network detection, expiry  checks)
* Deterministic test mode for automated evaluation
* Hosted Checkout Page for customer payments
* Merchant Dashboard with transactions & analytics
* Fully Dockerized – run everything with one command

## Documentation

All project documentation is available under:

backend/docs/

Includes:
- API documentation
- System architecture
- Database schema
- Screenshots of dashboard and checkout flows


🏗️ System Architecture:

┌──────────────┐
│  Dashboard   │  (Port 3000)
└──────┬───────┘
       │
       │ Authenticated APIs
       ▼
┌──────────────┐
│   API        │  FastAPI (Port 8000)
│              │
│  Orders      │
│  Payments    │
│  Merchants   │
│  Public APIs │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ PostgreSQL   │  (Port 5432)
└──────────────┘

┌──────────────┐
│ Checkout     │  (Port 3001)
│ Hosted Page  │
└──────────────┘

📁 Project Structure:

payment-gateway/
├── docker-compose.yml
├── README.md
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
├── frontend/
│   ├── Dockerfile
│   └── src/
└── checkout-page/
    ├── Dockerfile
    └── src/

🐳 Docker Setup (One-Command Run):
Start all services

docker-compose up -d

Services & Ports:

| Service   | URL / Port                                     |
| --------- | ---------------------------------------------- |
| API       | [http://localhost:8000](http://localhost:8000) |
| Dashboard | [http://localhost:3000](http://localhost:3000) |
| Checkout  | [http://localhost:3001](http://localhost:3001) |
| Database  | localhost:5432                                 |


All services start automatically with correct dependency ordering.

🔐 Test Merchant (Auto-Seeded):

A test merchant is automatically created on startup.

| Field       | Value                                  |
| ----------- | -------------------------------------- |
| Merchant ID | `550e8400-e29b-41d4-a716-446655440000` |
| Email       | `test@example.com`                     |
| API Key     | `key_test_abc123`                      |
| API Secret  | `secret_test_xyz789`                   |

--------------------------------------------------------------

❤️ Health Check:
GET /health

{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-01-09T04:30:00Z"
}

📦 Orders API:
Create Order
POST /api/v1/orders


Headers

X-Api-Key: key_test_abc123
X-Api-Secret: secret_test_xyz789


Body

{
  "amount": 50000,
  "currency": "INR",
  "receipt": "receipt_001",
  "notes": {
    "customer": "John Doe"
  }
}

Get Order
GET /api/v1/orders/{order_id}

----------------------------------------------------------------

💳 Payments API
Create Payment (UPI)
{
  "order_id": "order_xxxxxxxxxxxxxxxx",
  "method": "upi",
  "vpa": "user@paytm"
}

Create Payment (Card)
{
  "order_id": "order_xxxxxxxxxxxxxxxx",
  "method": "card",
  "card": {
    "number": "4111111111111111",
    "expiry_month": "12",
    "expiry_year": "2026",
    "cvv": "123",
    "holder_name": "John Doe"
  }
}


Payment State Flow

processing → success / failed

🌐 Public Checkout APIs (No Auth)

Used by the hosted checkout page.

GET /api/v1/orders/public/{order_id}

POST /api/v1/payments/public

GET /api/v1/payments/{payment_id}

🧪 Test Mode (Required for Evaluation):

Configured via environment variables:

TEST_MODE=true
TEST_PAYMENT_SUCCESS=true
TEST_PROCESSING_DELAY=1000


Ensures deterministic outcomes
Overrides random success/failure
Used by automated evaluators

🖥️ Merchant Dashboard (Port 3000):
Pages:

/login
/dashboard
/dashboard/transactions

Features:

View API credentials
Total transactions
Total successful amount
Success rate
Real-time data from database
All required data-test-id attributes are implemented.

🧾 Hosted Checkout Page (Port 3001):
URL Format
http://localhost:3001/checkout?order_id=order_xxx

Flow:

Fetch order details
Select payment method (UPI / Card)
Submit payment
Show processing state
Poll payment status
Display success or failure

Fully compliant with required HTML structure and data-test-ids.

🗄️ Database Design:

Tables-

merchants
orders
payments
Indexes

orders.merchant_id
payments.order_id
payments.status

Sensitive card data is never stored.

📄 Environment Configuration:

See .env.example for all required variables:

Database connection

Test merchant credentials

Payment simulation

Test mode overrides

✅ Submission Checklist

✔ Dockerized setup

✔ Auto-seeded test merchant

✔ Correct ID formats (order_, pay_)

✔ Authentication enforced

✔ Payment validations implemented

✔ Dashboard & checkout fully functional

✔ README instructions complete

🏁 Final Notes

This project demonstrates:

Real-world payment gateway architecture

Secure handling of financial flows

End-to-end system design

Production-ready Docker deployment

video demo:

https://youtu.be/bYjgakEEmzs