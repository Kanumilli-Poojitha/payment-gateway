# Payment Gateway API Documentation

Base URL:
http://localhost:8000/api/v1

All responses are JSON.
Timestamps are in ISO 8601 UTC format.

------------------------------------------------------------

## 🔐 Authentication (Merchant APIs)

Merchant APIs require:

Headers:
X-Api-Key: <merchant_api_key>
X-Api-Secret: <merchant_api_secret>

------------------------------------------------------------

## ❤️ Health Check

GET /health

Response:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-01-11T10:30:00Z"
}

📦 Orders API (Merchant)
Create Order

POST /orders

Headers:
X-Api-Key
X-Api-Secret

Body:
{
  "amount": 50000,
  "currency": "INR",
  "receipt": "receipt_001",
  "notes": {
    "customer": "John Doe"
  }
}
Response:

{
  "id": "order_qcu6hxPZ6BH3Rpil",
  "merchant_id": "mrc_B5WdkeyRYYro0v2N",
  "amount": 50000,
  "currency": "INR",
  "status": "created",
  "receipt": "receipt_001",
  "notes": {
    "customer": "John Doe"
  },
  "created_at": "2026-01-16T11:01:02.771058Z",
  "updated_at": "2026-01-16T11:01:02.771058Z"
}

Get Order

GET /orders/{order_id}
Headers:
order id
X-Api-Key
X-Api-Secret

Response:
{
  "id": "order_h9iUGFnHYKsoDLxM",
  "merchant_id": "mrc_sHuqktTIDTdkJBPK",
  "amount": 50000,
  "currency": "INR",
  "status": "created",
  "receipt": "receipt_001",
  "notes": {
    "customer": "John Doe"
  },
  "created_at": "2026-01-15T04:59:53.028378Z",
  "updated_at": "2026-01-15T04:59:53.028378Z"
}


🌐 Public Orders API (Checkout / SDK)
Create Public Order

POST /orders/public

Body:

{
  "amount": 50000,
  "currency": "INR",
  "receipt": "receipt_001",
  "notes": {
    "customer": "John Doe"
  }
}

Response:
{
  "id": "order_22hJz371jXdn3yaw",
  "merchant_id": "mrc_sHuqktTIDTdkJBPK",
  "amount": 50000,
  "currency": "INR",
  "status": "created",
  "receipt": "receipt_001",
  "notes": {
    "customer": "John Doe"
  },
  "created_at": "2026-01-15T05:01:56.279536Z",
  "updated_at": "2026-01-15T05:01:56.279536Z"
}

Get Public Order

GET /orders/public/{order_id}

Response:
{
  "id": "order_22hJz371jXdn3yaw",
  "merchant_id": "mrc_sHuqktTIDTdkJBPK",
  "amount": 50000,
  "currency": "INR",
  "status": "created",
  "receipt": "receipt_001",
  "notes": {
    "customer": "John Doe"
  },
  "created_at": "2026-01-15T05:01:56.279536Z",
  "updated_at": "2026-01-15T05:01:56.279536Z"
}

💳 Payments API (Merchant)
Create Payment

POST /payments

Headers:
X-Api-Key
X-Api-Secret

Idempotency-Key (optional)

Body (UPI):

{
  "order_id": "order_Vd6vWaawG8vpqJOR",
  "method": "card",
  "card_number": "4111111111111111",
  "expiry_month": 12,
  "expiry_year": 2026,
  "cvv": "123"
}

{
  "order_id": "order_xxx",
  "method": "upi",
  "vpa": "user@upi"
}
	
Response:
{
  "id": "pay_8ZcxseV6Ggfe9rze",
  "order_id": "order_22hJz371jXdn3yaw",
  "merchant_id": "mrc_sHuqktTIDTdkJBPK",
  "amount": 50000,
  "currency": "INR",
  "method": "upi",
  "status": "CREATED",
  "error_code": null,
  "error_description": null,
  "created_at": "2026-01-15T05:08:17.841529Z",
  "updated_at": "2026-01-15T05:08:17.841529Z"
}

Body (Card):

{
  "order_id": "order_xxx",
  "method": "card",
  "card": {
    "number": "4111111111111111",
    "expiry_month": "12",
    "expiry_year": "2026",
    "cvv": "123"
  }
}
Response:
{
  "id": "pay_MgjRE9qGrrOaSDKp",
  "order_id": "order_22hJz371jXdn3yaw",
  "merchant_id": "mrc_sHuqktTIDTdkJBPK",
  "amount": 50000,
  "currency": "INR",
  "method": "card",
  "status": "CREATED",
  "error_code": null,
  "error_description": null,
  "created_at": "2026-01-15T05:07:21.076708Z",
  "updated_at": "2026-01-15T05:07:21.076708Z"
}

🌍 Public Payments API (Checkout / SDK)
Create Payment

POST /payments/public

Idempotency-Key

{
    "order_id": "order_xxx",
    "amount": 500,
    "currency": "INR",
    "method": "upi",
    "vpa": "test@upi"
  }

POST
/api/v1/payments/{payment_id}/capture
Capture Payment

Headers:
payment id
X-Api-Key
X-Api-Secret
Idempotency-Key (optional)

Response:
{
  "id": "pay_8ZcxseV6Ggfe9rze",
  "order_id": "order_22hJz371jXdn3yaw",
  "merchant_id": "mrc_sHuqktTIDTdkJBPK",
  "amount": 50000,
  "currency": "INR",
  "method": "upi",
  "status": "PROCESSING",
  "error_code": null,
  "error_description": null,
  "created_at": "2026-01-15T05:08:17.841529Z",
  "updated_at": "2026-01-15T05:09:49.920543Z"
}

card:
	
Response body
Download
{
  "id": "pay_9GTQmNHR7S5tQQfN",
  "order_id": "order_3pMpUCIEV1kVHR6h",
  "merchant_id": "mrc_2AY0nMbdoQerM4ks",
  "amount": 50000,
  "currency": "INR",
  "method": "card",
  "status": "SUCCESS",
  "captured": true,
  "error_code": null,
  "error_description": null,
  "created_at": "2026-01-16T05:29:45.392600Z",
  "updated_at": "2026-01-16T05:31:31.707673Z"
}

Get Payment Status

GET /payments/public/{payment_id}

🔁 Refunds API
Create Refund

POST /refunds

Headers:
X-Api-Key
X-Api-Secret

Body:

{
  "payment_id": "pay_xxx",
  "amount": 50000,
  "reason": "Customer request"
}


	
Response:
{
  "id": "refund_UxiGQETHPTDgMtGO",
  "payment_id": "pay_8ZcxseV6Ggfe9rze",
  "merchant_id": "mrc_sHuqktTIDTdkJBPK",
  "amount": 1500,
  "status": "pending",
  "reason": null,
  "error_code": null,
  "error_description": null,
  "created_at": "2026-01-15T05:27:53.372053Z",
  "updated_at": "2026-01-15T05:27:53.372053Z"
}

POST
/api/v1/test/jobs/enqueue
Enqueue Test Job

no parameters
Response:
{
  "status": "queued",
  "payment_id": "pay_5VhlmyYt3jlpADJZ",
  "queue": "gateway_jobs"
}

Get Refund Status

GET /refunds/{refund_id}

Headers:
refund_id
X-Api-Key
X-Api-Secret
	
Response:
{
  "id": "refund_UxiGQETHPTDgMtGO",
  "payment_id": "pay_8ZcxseV6Ggfe9rze",
  "merchant_id": "mrc_sHuqktTIDTdkJBPK",
  "amount": 1500,
  "status": "PROCESSED",
  "reason": null,
  "error_code": null,
  "error_description": null,
  "created_at": "2026-01-15T05:27:53.372053Z",
  "updated_at": "2026-01-15T05:27:53.543223Z"
}

🌐 Webhooks

Events:
• payment.success
• payment.failed
• refund.processed
• refund.failed

Headers:
X-Signature: HMAC_SHA256(payload)

📊 Admin / Metrics

GET
/api/v1/admin/stats

Headers:
X-Api-Key
X-Api-Secret

Response:
{
  "payments": {
    "total": 2,
    "success": 0,
    "failed": 1,
    "processing": 0,
    "success_rate_pct": 0,
    "failure_rate_pct": 50
  },
  "webhooks": {
    "total": 0,
    "failed": 0,
    "retries": 0,
    "success_rate_pct": 0
  },
  "latency_sec": {
    "avg": 0,
    "min": 0,
    "max": 0,
    "p50": 0,
    "p95": 0
  }
}

Returns:
• Payment success rate
• Refund stats
• Webhook delivery stats
• Latency percentiles

webhooks


POST
/api/v1/webhooks
Register Webhook

Headers:
url
X-Api-Key
X-Api-Secret

Response:
{
  "id": "7f91a7a2-2204-4a89-ac3b-e6a75058fbf4",
  "url": "https://webhook.site/abcd-1234",
  "secret": "455be43ec4cd144f242a503e1eb909b9"
}

GET
/api/v1/webhooks
List Webhooks

Headers:
X-Api-Key
X-Api-Secret

Response:
[
  {
    "active": true,
    "merchant_id": "mrc_S7EgRDMxxHN3LLTm",
    "id": "7f91a7a2-2204-4a89-ac3b-e6a75058fbf4",
    "updated_at": "2026-01-16T05:52:17.299365+00:00",
    "url": "https://webhook.site/abcd-1234",
    "secret": "455be43ec4cd144f242a503e1eb909b9",
    "created_at": "2026-01-16T05:52:17.299365+00:00"
  }
]

webhook-logs


GET
/api/v1/webhook-logs
List Webhook Logs

Headers:
X-Api-Key
X-Api-Secret

Response:
[
  {
    "id": "7a0bfbc3-1a30-4ac6-bbcb-e49908d3f26e",
    "webhook_id": "7f91a7a2-2204-4a89-ac3b-e6a75058fbf4",
    "event_type": "payment.captured",
    "status": "success",
    "attempts": 1,
    "response_code": "200",
    "response_body": "test-mode-success",
    "created_at": "2026-01-16T05:55:54.481844Z",
    "updated_at": "2026-01-16T05:55:54.496375Z"
  },
  {
    "id": "5d11f38f-5343-42e1-95f3-008322ff2347",
    "webhook_id": "7f91a7a2-2204-4a89-ac3b-e6a75058fbf4",
    "event_type": "payment.success",
    "status": "success",
    "attempts": 1,
    "response_code": "200",
    "response_body": "test-mode-success",
    "created_at": "2026-01-16T05:54:27.689287Z",
    "updated_at": "2026-01-16T05:54:27.711855Z"
  }
]

POST
/api/v1/webhook-logs/{log_id}/retry
Retry Webhook

Headers:
log_id
X-Api-Key
X-Api-Secret

Response:
{
  "message": "Webhook retry queued"
}