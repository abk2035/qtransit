-- SQL seed (minimal) for QTransit RBAC
-- Run this only if you prefer raw SQL seeding. The Python seeder is recommended

-- Note: Adapt schema names if your DB has a different schema.

INSERT INTO companies (name, slug, country, currency, is_active) VALUES ('TestCo', 'testco', 'FR', 'EUR', true) ON CONFLICT DO NOTHING;

-- permissions and roles will be created by the Python seeder to ensure password hashing and associations
