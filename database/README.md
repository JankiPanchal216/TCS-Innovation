# LibraAI Database Architecture

This directory contains the PostgreSQL database schema, migrations, seed data, and documentation for the LibraAI platform.

## Architecture Principles

1. **PostgreSQL as the Source of Truth**: The database stores both standard relational data and AI vector embeddings (`pgvector`), ensuring data consistency and avoiding dual-write problems with separate vector stores.
2. **AI Extensibility**: Designed to track AI model usage, store generated learning paths, track document ingestion for RAG, and maintain semantic embeddings.
3. **Analytics Ready**: Includes materialized/standard views for librarian analytics (book popularity, utilization, subject demand, overdue summaries).
4. **Relational Integrity**: Enforces strict constraints using Foreign Keys, Checks, and well-defined Enums/VARCHAR states.

## Management Scripts

To interact easily with your local PostgreSQL, use the provided scripts.
You can configure your local DB connection via the `.env` file.

1. **Copy `.env.example` to `.env`** and update it with your local postgres credentials.
2. **Initialize Database (`init_db.ps1`)**: Applies all migrations sequentially and then runs `seed.sql`.
   ```powershell
   .\init_db.ps1
   ```
3. **Export Database (`export_db.ps1`)**: Dumps the schema and data for backups.
   ```powershell
   .\export_db.ps1
   ```

## Directory Structure

- `migrations/`: Contains idempotent `.sql` files executed in numerical order.
  - `001_extensions.sql`: pgvector and uuid-ossp
  - `002_core_users.sql` -> `012_indexes.sql`: Schema definitions
- `seed.sql`: Generated synthetic data for testing.
- `queries.sql`: Example SQL queries (keyword search, semantic search, hybrid, analytics).
- `er_diagram.mermaid`: Visual representation of relationships.

## Notes on pgvector Indexes

Currently, the schema does not enforce a specific vector dimension on the `books.embedding` column. This allows you to use `768` (e.g., local models) or `1536` (e.g., OpenAI) without altering the table structure.
Once you finalize your model, you can uncomment and adjust the index creation in `012_indexes.sql`:
```sql
CREATE INDEX idx_books_embedding ON books USING hnsw (embedding vector_l2_ops);
```
