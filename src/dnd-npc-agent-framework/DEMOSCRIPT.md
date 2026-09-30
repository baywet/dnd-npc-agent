

## Getting ready

1. Run

   ```shell
   # deploy the agent on foundry
   azd up
   # start the agent locally
   azd ai agent run
   # clear the memories
   curl -i -X DELETE "http://localhost:8088/debug/memory"
   ```

1. Open A browser tab to [the local workbench](http://127.0.0.1:8087/).
1. Open a browser tab to the Foundry workbench.

## Demos

### Local tool

!! In the Foundry sandbox

1. Ask `throw a dice 8 with +2 modifier`.
1. Outline that it called a local tool and didn't ask for approval.
1. Move over to the traces tab.
1. Outline the tool call, and the additional span.
1. Show the code for the agent definition to set the stage.
1. Show the code for the tool and additional telemetry.

### MCP demo

!! In the local workbench

1. Ask `what's the armor class for a standard goblin?`.
1. Outline the approval requests, explain why they are important.
1. Approve the permissions. Show the result.
1. Outline the source citation link.
1. Show the code, and the setting approval for the tools, as well as selecting the approved tools.

### Skill demo

!! In the local workbench

1. Ask `impersonate a standard goblin`.
1. Ask `you're following a path back to your lair when you suddenly encounter heavily armed adventurers, what do you do?`
1. Outline the skill card, the approval requests, and the whole workflow being followed.
1. Outline that MCP is great to get external abilities, tools strictly defined behaviour, and skills for loosely defined behaviour.

### Memory

!! In the local workbench

1. in a new session ask `what are my favourite voices?`, it returns a response saying it doesn't know.
1. add `My favorite NPC voice is a slow Scottish accent. I use that voice for ancient dwarven blacksmiths.`
1. create a new conversation.
1. ask again `what are my favourite voices?`, it should return the previous thing, despite the new conversation.
1. walk through the memory code.