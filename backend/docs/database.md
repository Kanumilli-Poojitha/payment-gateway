# Database Schema Documentation

Database: PostgreSQL

------------------------------------------------------------

## merchants

Stores merchant accounts.

Columns:
• id (PK)
• name
• email (unique)
• api_key (unique)
• api_secret
• created_at
• updated_at

------------------------------------------------------------

## orders

Represents payment orders.

Columns:
• id (PK)
• merchant_id (FK → merchants.id)
• amount
• currency
• status (created → paid / failed)
• receipt
• notes (JSON)
• created_at
• updated_at

Indexes:
• idx_orders_merchant_id

------------------------------------------------------------

## payments

Stores payment attempts.

Columns:
• id (PK)
• order_id (FK → orders.id)
• merchant_id (FK → merchants.id)
• amount
• currency
• method (upi / card)
• status (processing → success / failed)
• vpa
• card_network
• card_last4
• error_code
• error_description
• idempotency_key
• created_at
• updated_at

Indexes:
• idx_payments_order_id
• idx_payments_status

------------------------------------------------------------

## refunds

Represents refund requests.

Columns:
• id (PK)
• payment_id (FK → payments.id)
• merchant_id (FK → merchants.id)
• amount
• status (pending → processed / failed)
• reason
• error_code
• error_description
• created_at
• updated_at

Indexes:
• idx_refunds_payment_id
• idx_refunds_status

------------------------------------------------------------

## webhooks

Stores merchant webhook endpoints.

Columns:
• id (PK)
• merchant_id (FK → merchants.id)
• url
• secret
• active
• created_at
• updated_at

------------------------------------------------------------

## webhook_logs

Logs each webhook delivery attempt.

Columns:
• id (PK)
• webhook_id (FK → webhooks.id)
• event_type
• payload (JSON)
• status (success / failed)
• response_code
• response_body
• attempts
• created_at

------------------------------------------------------------

## Design Notes

• No raw card data is stored
• All timestamps are server-generated
• Indexes added for high-volume queries
• Designed for async processing and auditability