$token = az account get-access-token `
    --resource "https://ai.azure.com" `
    --query accessToken -o tsv

$body = @{
    model = "gpt-4.1-mini"
    input = "Say hello from the Responses API"
} | ConvertTo-Json -Depth 5

curl -X POST `
  "https://ai-account-maqq3xk3jj6ze.services.ai.azure.com/api/projects/ai-project-dnd-npc-agent-north-central-dev/openai/v1/responses" `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d $body
