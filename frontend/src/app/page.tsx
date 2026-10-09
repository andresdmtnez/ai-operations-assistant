import Link from 'next/link';

export default function Home() {
  return (
    <div>
      <h1>AI Operations Assistant</h1>
      <p>Welcome to the demo application. Use the navigation above to explore.</p>
      <ul>
        <li>
          <Link href="/dashboard">Dashboard</Link>
        </li>
        <li>
          <Link href="/orders">Orders</Link>
        </li>
        <li>
          <Link href="/tickets">Tickets</Link>
        </li>
        <li>
          <Link href="/chat">Chat (placeholder)</Link>
        </li>
      </ul>
    </div>
  );
}
