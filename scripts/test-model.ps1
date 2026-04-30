$token = az account get-access-token `
    --resource "https://ai.azure.com" `
    --query accessToken -o tsv

$body = @{
    model = "gpt-4o-mini"
    input = "Say hello from the Responses API"
} | ConvertTo-Json -Depth 5

curl -X POST `
  "https://ai-account-3phirl5w4q3ks.services.ai.azure.com/api/projects/ai-project-ai-project-dnd-npc-agent-john-cc-dev/openai/v1/responses" `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d $body
