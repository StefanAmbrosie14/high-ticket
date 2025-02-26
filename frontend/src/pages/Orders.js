import React, { useEffect, useState } from "react";
import axios from "axios";

function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/orders/")
      .then(response => {
        setOrders(response.data);
        setLoading(false);
      })
      .catch(error => {
        setError("Failed to load orders");
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading orders...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Orders</h1>
      <ul>
        {orders.map(order => (
          <li key={order.id}>
            Order #{order.id} - {order.total_amount} USD - {order.user_email}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Orders;
