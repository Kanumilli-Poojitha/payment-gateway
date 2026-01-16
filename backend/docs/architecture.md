
---

# 📄 `docs/architecture.md`

```md
# System Architecture

This payment gateway follows an async-first, event-driven architecture inspired by real-world fintech systems.

------------------------------------------------------------

## 🧱 Core Components

### 1. API Gateway (FastAPI)
Port: 8000

Responsibilities:
• Merchant authentication
• Order management
• Payment initiation
• Refund initiation
• Public checkout APIs
• Webhook configuration
• Admin metrics

------------------------------------------------------------

### 2. PostgreSQL Database
Port: 5432

Stores:
• Merchants
• Orders
• Payments
• Refunds
• Webhooks
• Webhook logs

------------------------------------------------------------

### 3. Redis (Job Queue)
Port: 6379

Queues:
• Payment processing queue
• Refund processing queue
• Webhook delivery queue
• Dead-letter queue (DLQ)

------------------------------------------------------------

### 4. Worker Services

#### Payment Worker
• Processes payment jobs
• Updates payment status
• Triggers webhook events

#### Refund Worker
• Processes pending refunds
• Updates refund status
• Triggers refund webhooks

#### Webhook Worker
• Delivers webhook events
• Signs payloads using HMAC
• Retries failed deliveries
• Sends failed events to DLQ

------------------------------------------------------------

### 5. Frontend Applications

#### Merchant Dashboard (3000)
• Transaction analytics
• Webhook logs
• API credentials

#### Hosted Checkout Page (3001)
• Payment UI
• Order fetch
• Payment polling

#### Embeddable JS SDK
• Lightweight checkout integration
• Public order & payment creation

------------------------------------------------------------

## 🔁 Async Flow Example (Payment)

1. Client creates payment
2. API stores payment as `processing`
3. Payment job enqueued in Redis
4. Payment worker processes job
5. Payment status updated
6. Webhook event created
7. Webhook worker delivers event

------------------------------------------------------------

## 🔐 Security Design

• API key + secret authentication
• Idempotency keys
• No sensitive card storage
• HMAC-signed webhooks
• Retry + DLQ handling

------------------------------------------------------------

## 📈 Scalability Considerations

• Stateless API
• Horizontally scalable workers
• Queue-based async processing
• Independent webhook delivery

------------------------------------------------------------

This architecture closely mirrors real payment gateways such as Stripe and Razorpay.
