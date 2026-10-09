import React from 'react';
import { API_URL } from '@/utils/api';

interface Ticket {
  id: number;
  customer_id: number;
  subject: string;
  status: string;
  description: string | null;
  created_at: string;
}

export default async function TicketsPage() {
  const res = await fetch(`${API_URL}/tickets`);
  const tickets: Ticket[] = await res.json();

  return (
    <div>
      <h1>Tickets</h1>
      {tickets.length === 0 ? (
        <p>No tickets available.</p>
      ) : (
        <table border={1} cellPadding={5}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer ID</th>
              <th>Subject</th>
              <th>Status</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            {tickets.map((t) => (
              <tr key={t.id}>
                <td>{t.id}</td>
                <td>{t.customer_id}</td>
                <td>{t.subject}</td>
                <td>{t.status}</td>
                <td>{new Date(t.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
