$ErrorActionPreference = 'Stop'

# Load .env variables if the file exists
if (Test-Path ".env") {
    Write-Host "Loading environment variables from .env"
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^\s*([^#]+?)\s*=\s*(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
} else {
    Write-Host "Warning: .env file not found. Ensure PGUSER, PGPASSWORD, PGDATABASE, etc. are set."
}

# Array of migration scripts in order
$migrations = @(
    "migrations\001_extensions.sql",
    "migrations\002_core_users.sql",
    "migrations\003_academic.sql",
    "migrations\004_catalog.sql",
    "migrations\005_inventory.sql",
    "migrations\006_borrowing.sql",
    "migrations\007_interactions.sql",
    "migrations\008_recommendations.sql",
    "migrations\009_ai.sql",
    "migrations\010_documents.sql",
    "migrations\011_analytics.sql",
    "migrations\012_indexes.sql"
)

Write-Host "Applying migrations..."

foreach ($migration in $migrations) {
    if (Test-Path $migration) {
        Write-Host "Running $migration"
        psql -v ON_ERROR_STOP=1 -f $migration
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to run $migration"
            exit 1
        }
    } else {
        Write-Error "Migration file not found: $migration"
        exit 1
    }
}

Write-Host "Migrations applied successfully."

# Run seed script
$seedFile = "seed.sql"
if (Test-Path $seedFile) {
    Write-Host "Running seed script: $seedFile"
    psql -v ON_ERROR_STOP=1 -f $seedFile
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to run $seedFile"
        exit 1
    }
    Write-Host "Database seeded successfully."
} else {
    Write-Host "Warning: Seed file not found at $seedFile"
}

Write-Host "Database initialization complete."
