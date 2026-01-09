// src/pages/Checkout.jsx
import { useEffect, useState } from "react";
import axios from "axios";
import { useSearchParams, useNavigate } from "react-router-dom";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const STATUS = {
  IDLE: "idle",
  PROCESSING: "processing",
  SUCCESS: "success",
  FAILED: "failed",
};

export default function Checkout() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const orderId = searchParams.get("order_id");

  const [order, setOrder] = useState(null);
  const [method, setMethod] = useState("");
  const [status, setStatus] = useState(STATUS.IDLE);
  const [paymentId, setPaymentId] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  // -------------------------------------------------
  // STEP 1 — Fetch PUBLIC order ✅
  // -------------------------------------------------
  useEffect(() => {
    if (!orderId) return;

    axios
      .get(`${API_BASE}/orders/public/${orderId}`)
      .then((res) => setOrder(res.data))
      .catch(() => setStatus(STATUS.FAILED));
  }, [orderId]);

  // -------------------------------------------------
  // STEP 3 — Poll PUBLIC payment status ✅
  // -------------------------------------------------
  useEffect(() => {
    if (!paymentId || status !== STATUS.PROCESSING) return;

    const interval = setInterval(() => {
      axios
        .get(`${API_BASE}/payments/public/${paymentId}`)
        .then((res) => {
          if (res.data.status === "success") {
            setStatus(STATUS.SUCCESS);
            clearInterval(interval);
            navigate("/success");
          }

          if (res.data.status === "failed") {
            setErrorMessage(
              res.data.error_description || "Payment failed"
            );
            setStatus(STATUS.FAILED);
            clearInterval(interval);
            navigate("/failure");
          }
        })
        .catch(() => {
          setStatus(STATUS.FAILED);
          clearInterval(interval);
          navigate("/failure");
        });
    }, 2000);

    return () => clearInterval(interval);
  }, [paymentId, status, navigate]);

  // -------------------------------------------------
  // STEP 2 — Create PUBLIC payment ✅
  // -------------------------------------------------
  const createPayment = (payload) => {
    setStatus(STATUS.PROCESSING);
    setErrorMessage("");

    axios
      .post(`${API_BASE}/payments/public`, payload)
      .then((res) => {
        setPaymentId(res.data.id);
      })
      .catch((err) => {
        setErrorMessage(
          err.response?.data?.error?.description || "Payment failed"
        );
        setStatus(STATUS.FAILED);
        navigate("/failure");
      });
  };

  if (!order) return <div>Loading...</div>;

  return (
    <div data-test-id="checkout-container">
      {/* Order Summary */}
      <div data-test-id="order-summary">
        <h2>Complete Payment</h2>

        <div>
          <span>Amount: </span>
          <span data-test-id="order-amount">
            ₹{(order.amount / 100).toFixed(2)}
          </span>
        </div>

        <div>
          <span>Order ID: </span>
          <span data-test-id="order-id">{order.id}</span>
        </div>
      </div>

      {/* Payment Method Selection */}
      {status === STATUS.IDLE && (
        <>
          <div data-test-id="payment-methods">
            <button onClick={() => setMethod("upi")}>UPI</button>
            <button onClick={() => setMethod("card")}>Card</button>
          </div>

          {/* UPI */}
          {method === "upi" && (
            <form
              onSubmit={(e) => {
                e.preventDefault();
                createPayment({
                  order_id: order.id,
                  method: "upi",
                  vpa: e.target.vpa.value,
                });
              }}
            >
              <input
                name="vpa"
                placeholder="username@bank"
                required
              />
              <button type="submit">Pay</button>
            </form>
          )}

          {/* Card */}
          {method === "card" && (
            <form
              onSubmit={(e) => {
                e.preventDefault();
                createPayment({
                  order_id: order.id,
                  method: "card",
                  card: {
                    number: e.target.cardNumber.value,
                    expiry_month: 12,
                    expiry_year: 2030,
                    cvv: "123",
                  },
                });
              }}
            >
              <input
                name="cardNumber"
                placeholder="4111111111111111"
                required
              />
              <button type="submit">Pay</button>
            </form>
          )}
        </>
      )}

      {/* Processing */}
      {status === STATUS.PROCESSING && (
        <div data-test-id="processing-state">
          <span>Processing payment...</span>
        </div>
      )}

      {/* Error */}
      {status === STATUS.FAILED && (
        <div data-test-id="error-state">
          {errorMessage || "Something went wrong"}
        </div>
      )}
    </div>
  );
}