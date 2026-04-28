# Debugging Guide

## Prerequisites

Before debugging, ensure you have the following installed:

- **.NET 10** - Required for building and debugging the application

## Debugging Instructions

### 401 Unauthorized Error When Talking to the Agent

If you encounter a **401 error status code** when first talking to the agent, the service principal lacks the necessary permissions.

**Resolution:**

1. Find the service principal name by looking in the **top right corner of the playground**
2. Assign the **Azure AI User** role to the service principal at the **parent resource group level**
3. **Restart the chat session** by pressing **Ctrl+F5** to refresh the token with the new permissions

After restarting, the agent should communicate successfully with the updated role assignment.
