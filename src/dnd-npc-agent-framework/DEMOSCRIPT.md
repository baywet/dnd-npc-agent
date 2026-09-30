

## Getting ready

1. Run

   ```shell
   # start the agent locally
   azd ai agent run
   # clear the memories
   curl -i -X DELETE "http://localhost:8088/debug/memory"
   ```

## Demos

### Show the local workbench

http://127.0.0.1:8087/

### Memory

1. in a new session ask `what are my favourite voices?`, it returns a response saying it doesn't know.
1. add `My favorite NPC voice is a slow Scottish accent. I use that voice for ancient dwarven blacksmiths.`
1. create a new conversation.
1. ask again `what are my favourite voices?`, it should return the previous thing, despite the new conversation.
1. walk through the memory code.