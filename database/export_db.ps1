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

$dateStamp = Get-Date -Format "yyyyMMdd_HHmmss"
$exportFile = "libraai_backup_$dateStamp.sql"

Write-Host "Exporting database to $exportFile..."

# Dump schema and data
pg_dump -F p -f $exportFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "Database successfully exported to $exportFile"
} else {
    Write-Error "Failed to export database."
    exit 1
}
