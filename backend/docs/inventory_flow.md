# Library Inventory Flow

1. **Librarian Uploads CSV**: `POST /api/library/inventory/upload`
2. **Batch Created**: A record is created in `inventory_import_batches` with `status='processing'`.
3. **Row Parsing**: Each row is cleaned and standardized.
4. **Identity Resolution**: The system attempts to map the row to an existing book in the catalog via ISBN13, ISBN10, Google Book ID, or Title+Author.
5. **Inventory Upsert**: If a match is found, the `inventory` table is updated (or inserted) with the new `total_copies` and `available_copies`. `inventory_source` is set to `csv`.
6. **Errors**: If no match is found, the row is skipped and logged in `inventory_import_errors` as `unresolved`.
7. **Completion**: The batch `status` is marked as `completed` (or `completed_with_errors`).

*Note*: Embeddings are NOT regenerated during inventory updates as semantic content has not changed.
