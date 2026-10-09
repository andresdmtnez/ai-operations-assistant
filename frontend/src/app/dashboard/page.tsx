import React from 'react';
import { API_URL } from '@/utils/api';

export default async function DashboardPage() {
  // Fetch counts concurrently
  const [customersRes, ordersRes, ticketsRes] = await Promise.all([
    fetch(`${API_URL}/customers`),
    fetch(`${API_URL}/orders`),
    fetch(`${API_URL}/tickets`),
  ]);

  const customers = await customersRes.json();
  const orders = await ordersRes.json();
  const tickets = await ticketsRes.json();

  return (
    <div>
      <h1>Dashboard</h1>
      <ul>
        <li>Customers: {customers.length}</li>
        <li>Orders: {orders.length}</li>
        <li>Tickets: {tickets.length}</li>
      </ul>
    </div>
  );
}
