import './globals.css';
import Link from 'next/link';

export const metadata = {
  title: 'AI Operations Assistant',
  description: 'Demo portfolio application',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav style={{ padding: '1rem', background: '#f0f0f0' }}>
          <Link href="/" style={{ marginRight: '1rem' }}>Home</Link>
          <Link href="/dashboard" style={{ marginRight: '1rem' }}>Dashboard</Link>
          <Link href="/orders" style={{ marginRight: '1rem' }}>Orders</Link>
          <Link href="/tickets" style={{ marginRight: '1rem' }}>Tickets</Link>
          <Link href="/chat" style={{ marginRight: '1rem' }}>Chat</Link>
        </nav>
        <main style={{ padding: '1rem' }}>{children}</main>
      </body>
    </html>
  );
}
