INSERT INTO customers (name, email)
SELECT
    'Customer ' || i,
    'customer' || i || '@example.com'
FROM generate_series(1, 100) AS s(i);

INSERT INTO orders (customer_id, status, total_amount)
SELECT
    ((i - 1) % 100) + 1,
    CASE
        WHEN i % 4 = 0 THEN 'cancelled'
        WHEN i % 3 = 0 THEN 'shipped'
        WHEN i % 2 = 0 THEN 'processing'
        ELSE 'pending'
    END,
    ROUND((10 + random() * 990)::numeric, 2)
FROM generate_series(1, 500) AS s(i);

INSERT INTO tickets (customer_id, subject, status, description)
SELECT
    ((i - 1) % 100) + 1,
    'Support ticket ' || i,
    CASE
        WHEN i % 3 = 0 THEN 'closed'
        WHEN i % 2 = 0 THEN 'in_progress'
        ELSE 'open'
    END,
    'Example support ticket generated for the development environment.'
FROM generate_series(1, 100) AS s(i);
