# Demo Script

## Prerequisites

Before running the demo, ensure you have the following installed:

- **.NET SDK 10** - Required for building and running the agent
- **Visual Studio Code** - Recommended code editor
- **Azure Developer CLI (azd)** - Required for deployment and management
- **azd AI Agent Extension** - Install with `azd extension install azure.ai.agents`
- **Windows Terminal** - Recommended terminal application
- **PowerShell 7+** - Required for running scripts

## Getting Ready

Before starting the demo, prepare your environment:

1. **Sign in to Azure** - Ensure `azd` is signed in to your corporate identity:
   ```bash
   azd auth login
   ```

2. **Open Terminal** - Open Windows Terminal and navigate to this repository directory

3. **Open Browser Session** - Open the Azure AI Foundry playground in your browser:
   ```
   https://ai.azure.com/nextgen/r/5y5SVPJlTpWb0p7o5zKQUQ,rg-ai-project-dnd-npc-agent-john-cc-dev,,ai-account-3phirl5w4q3ks,ai-project-ai-project-dnd-npc-agent-john-cc-dev/build/agents/local-tools/build?version=3
   ```

   This URL points to:
   - **Resource Group**: rg-ai-project-dnd-npc-agent-john-cc-dev
   - **AI Account**: ai-account-3phirl5w4q3ks
   - **AI Project**: ai-project-dnd-npc-agent-john-cc-dev
   - **Agent**: local-tools (version 3)

4. **Test Agent Responsiveness** - In the playground, send a test message to the agent to verify it's responsive

5. **Redeploy if Needed** - If the agent is not responding, redeploy it using:
   ```bash
   azd up
   ```
   Follow the prompts to select your subscription and resource group. Wait for the deployment to complete before proceeding with the demo.

## Generating a Synthetic Dataset

This demo shows how to create and evaluate a synthetic dataset for the D&D NPC Agent.

### Steps to Generate Synthetic Dataset

1. Open the **Playground**
2. Click **Evaluation** in the navigation
3. Click **Create New Evaluation**
4. Select **Target Agent**
5. Click **Generate Synthetic Dataset**

### Synthetic Dataset Prompt

Use the following prompt when generating the synthetic dataset:

```
This agent will role play non playable characters in dungeons and dragons sessions.

We need to ensure the agent is always asking for a character sheet from Dungeons and Dragons at the beginning of every session. If the user has not provided a character sheet, we need to remind them to do so before answering other character questions.
```

This prompt ensures the evaluation dataset tests the agent's ability to:
- Request character sheets at the start of interactions
- Enforce the requirement for character sheet information before proceeding
- Remind users to provide their character sheet if it's missing
