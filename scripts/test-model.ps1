# Load environment variables from a .env file by walking up from the given
# directory (defaults to this script's directory), mirroring the DotNetEnv
# `Env.TraversePath().Load()` behavior used by the .NET projects in this repo.
function Import-DotEnv {
    param(
        [string] $StartDirectory = $PSScriptRoot
    )
    $dir = $StartDirectory
    while ($dir) {
        $envPath = Join-Path $dir ".env"
        if (Test-Path $envPath) {
            foreach ($line in Get-Content -LiteralPath $envPath) {
                $trimmed = $line.Trim()
                if (-not $trimmed -or $trimmed.StartsWith("#")) { continue }
                $eq = $trimmed.IndexOf("=")
                if ($eq -lt 1) { continue }
                $key = $trimmed.Substring(0, $eq).Trim()
                $value = $trimmed.Substring($eq + 1).Trim()
                if ($value.Length -ge 2) {
                    $first = $value[0]; $last = $value[$value.Length - 1]
                    if (($first -eq '"' -and $last -eq '"') -or ($first -eq "'" -and $last -eq "'")) {
                        $value = $value.Substring(1, $value.Length - 2)
                    }
                }
                if (-not [Environment]::GetEnvironmentVariable($key)) {
                    [Environment]::SetEnvironmentVariable($key, $value)
                }
            }
            return $envPath
        }
        $parent = Split-Path -Parent $dir
        if ($parent -eq $dir) { break }
        $dir = $parent
    }
    return $null
}

$azureDir = Join-Path $PSScriptRoot "..\.azure"
if (Test-Path $azureDir) {
    foreach ($sub in Get-ChildItem -LiteralPath $azureDir -Directory) {
        Import-DotEnv -StartDirectory $sub.FullName | Out-Null
    }
}

Import-DotEnv | Out-Null

$endpoint = $env:FOUNDRY_PROJECT_ENDPOINT
$model = $env:AZURE_AI_MODEL_DEPLOYMENT_NAME

if (-not $endpoint) {
    throw "FOUNDRY_PROJECT_ENDPOINT is not set. Define it in the .env file at the repo root."
}
if (-not $model) {
    throw "AZURE_AI_MODEL_DEPLOYMENT_NAME is not set. Define it in the .env file at the repo root."
}

$url = "$($endpoint.TrimEnd('/'))/openai/v1/responses"

$token = az account get-access-token `
    --resource "https://ai.azure.com" `
    --query accessToken -o tsv

$body = @{
    model = $model
    input = "Say hello from the Responses API"
} | ConvertTo-Json -Depth 5

curl -X POST `
  $url `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d $body
