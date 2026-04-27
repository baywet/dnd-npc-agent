# Contributing

## Code Formatting

Before committing any changes, run **dotnet format** to ensure consistent code style:

```bash
dotnet format
```

Copilot will run `dotnet format` before creating any commit to ensure all code adheres to the project's formatting standards.

## Commit Messages

When instructed to commit changes, Copilot will use **conventional commits** for commit messages. This ensures consistent, semantic commit messages that are easy to parse and understand.

Conventional commit format:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Common types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring without changing functionality
- `test`: Adding or updating tests
- `chore`: Build, dependencies, or tooling changes

**Example:**
```
feat(agent): add support for multi-turn conversations

Implemented conversation history tracking to allow agents
to maintain context across multiple interactions.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

When you ask Copilot to commit your changes, it will:
1. Run `dotnet format` to format all code
2. Automatically analyze the diff to determine the appropriate type and scope
3. Generate a descriptive conventional commit message
