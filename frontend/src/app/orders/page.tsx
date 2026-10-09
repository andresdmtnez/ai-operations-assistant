import React from 'react';
import { API_URL } from '@/utils/api';

interface Order {
  id: number;
  customer_id: number;
  status: string;
  total_amount: number;
  created_at: string;
}

export default async function OrdersPage() {
  const res = await fetch(`${API_URL}/orders`);
  const orders: Order[] = await res.json();
  return (
    <div>
      <h1>Orders</h1>
      {orders.length === 0 ? (
        <p>No orders available.</p>
      ) : (
        <table border={1} cellPadding={5}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer ID</th>
              <th>Status</th>
              <th>Total</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((o) => (
              <tr key={o.id}>
                <td>{o.id}</td>
                <td>{o.customer_id}</td>
                <td>{o.status}</td>
                <td>{o.total_amount}</td>
                <td>{new Date(o.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
