

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

### Show the local workbench

http://127.0.0.1:8087/

### Local tool

!! In the Foundry sandbox

1. Ask `throw a dice 8 with +2 modifier`.
1. Outline that it called a local tool and didn't ask for approval.
1. Move over to the traces tab.
1. Outline the tool call, and the additional span.
1. Show the code for the tool and additional telemetry.

### Memory

1. in a new session ask `what are my favourite voices?`, it returns a response saying it doesn't know.
1. add `My favorite NPC voice is a slow Scottish accent. I use that voice for ancient dwarven blacksmiths.`
1. create a new conversation.
1. ask again `what are my favourite voices?`, it should return the previous thing, despite the new conversation.
1. walk through the memory code.